import sys
import threading
import queue
import numpy as np
import sounddevice as sd
import mido
from paddle.base.libpaddle.eager.ops.legacy import decayed_adagrad
from scipy.signal import square, sawtooth
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QDial,
    QComboBox, QLabel, QPushButton, QCheckBox, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt, QTimer

import utilities as utils


# Constants
SR = 44100  # Sample rate
midi_queue = queue.Queue()


def process_midi(msg):
    if msg.type == "note_on" and msg.velocity > 0:
        freq = utils.midi_to_freq(msg.note)
        velocity = msg.velocity / 127
        duration = 5.0
        print(f"Received MIDI: Note {msg.note}, Freq {freq:.2f} Hz, Velocity {msg.velocity}")
        midi_queue.put((freq, velocity, duration))


def midi_listener(port_name):
    with mido.open_input(port_name) as input_port:
        for msg in input_port:
            process_midi(msg)


def schrader_distort(signal, reverb_amount=0.3, decay=0.6):
    delay_times = [0.029, 0.037, 0.041, 0.053]
    gains = [decay * (0.7 ** i) for i in range(len(delay_times))]    # prevents infinite feedback
    reverb_signal = np.zeros(len(signal))
    for delay, gain in zip(delay_times, gains):    # processing each delay time seperately, making comb filt
        delay_samples = int(delay * SR)
        if delay_samples < len(signal):
            reverb_signal[delay_samples:] += np.tanh(signal[:-delay_samples] * gain)    # non linear transform
    # Smooth mixing of dry and wet signals
    wet_signal = signal * (1 - reverb_amount) + reverb_signal * reverb_amount    # where distortin magic happens
    return wet_signal


def generate_waveform(waveform, frequency, duration=1):
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    if waveform == "sine":
        return np.sin(2 * np.pi * frequency * t)
    elif waveform == "square":
        return square(2 * np.pi * frequency * t)
    elif waveform == "sawtooth":
        return sawtooth(2 * np.pi * frequency * t)
    elif waveform == "triangle":
        return sawtooth(2 * np.pi * frequency * t, width=0.5)
    else:
        raise ValueError(f"Invalid waveform type: {waveform}")


def generate_am(frequency, mod_frequency, index, duration):
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    carrier = np.sin(2 * np.pi * frequency * t)
    modulator = (1 + index * np.sin(2 * np.pi * mod_frequency * t)) / 2
    return carrier * modulator


def generate_fm(frequency, mod_frequency, index, duration):
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    modulator = index * np.sin(2 * np.pi * mod_frequency * t)
    return np.sin(2 * np.pi * (frequency + modulator) * t)


def play_sound(waveform, frequency, duration, output_device, synthesis_mode, mod_frequency, index, amplitude):

    if synthesis_mode == "AM":
        audio_signal = generate_am(frequency, mod_frequency, index, duration)
    elif synthesis_mode == "FM":
        audio_signal = generate_fm(frequency, mod_frequency, index, duration)
    else:
        audio_signal = generate_waveform(waveform, frequency, duration)
    audio_signal *= amplitude

    try:
        print(f"Sending audio to output device {output_device}")
        sd.play(audio_signal, samplerate=SR, device=output_device, blocking=False)
    except Exception as e:
        print(f"Error playing sound: {e}")

class SynthControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            background-color: pink;
            font-family: 'Comic Sans MS';
            font-size: 14px;
            color: #4B0082;
        """)

        # Main
        main_layout = QVBoxLayout()

        # Carrier
        carrier_layout = QHBoxLayout()
        self.carrier_dial = self.create_dial(100, 2000, 500, self.update_label)
        self.carrier_label = QLabel("Carrier: 500 |(°Ω°)/")
        carrier_layout.addWidget(self.carrier_label)
        carrier_layout.addWidget(self.carrier_dial)

        # Modulator
        modulator_layout = QHBoxLayout()
        self.modulator_dial = self.create_dial(10, 1000, 50, self.update_label)
        self.modulator_label = QLabel("Modulator: 50 ( ｀皿´)｡ﾐ/")
        modulator_layout.addWidget(self.modulator_label)
        modulator_layout.addWidget(self.modulator_dial)

        # index
        index_layout = QHBoxLayout()
        self.index_dial = self.create_dial(1, 10, 2, self.update_label)
        self.index_label = QLabel("Mod Index: 2 (づ｡◕‿‿◕｡)づ")
        index_layout.addWidget(self.index_label)
        index_layout.addWidget(self.index_dial)

        # dist length
        dist_length = QHBoxLayout()
        self.dist_dial = self.create_dial(1, 1000, 2, self.update_label)
        self.dist_label = QLabel("Dist Orshun ┌П┐(ಠ_ಠ): 2")
        dist_length.addWidget(self.dist_label)
        dist_length.addWidget(self.dist_dial)

        # Decay
        decay_layout = QHBoxLayout()
        self.decay_dial = self.create_dial(1, 1000, 2, self.update_label)
        self.decay_label = QLabel("DECASTYSYD ／人◕ __ ◕人＼  2")
        decay_layout.addWidget(self.decay_label)
        decay_layout.addWidget(self.decay_dial)

        # Synthesis mode
        self.fm_radio = QRadioButton("FM ꒰ ꒡⌓꒡꒱")
        self.fm_radio.setChecked(True)
        self.am_radio = QRadioButton("AM (っˆڡˆς)")
        self.synthesis_mode = QButtonGroup()
        self.synthesis_mode.addButton(self.fm_radio)
        self.synthesis_mode.addButton(self.am_radio)
        synthesis_layout = QHBoxLayout()
        synthesis_layout.addWidget(self.fm_radio)
        synthesis_layout.addWidget(self.am_radio)

        # Waveform
        self.waveform_dropdown = QComboBox()
        self.waveform_dropdown.addItems(["sine", "square", "sawtooth", "triangle"])
        self.waveform_label = QLabel("Wav ≧◡≦")
        waveform_layout = QHBoxLayout()
        waveform_layout.addWidget(self.waveform_label)
        waveform_layout.addWidget(self.waveform_dropdown)

        # MIDI
        self.midi_dropdown = QComboBox()
        self.midi_dropdown.addItems(utils.list_midi_devices())
        self.midi_button = QPushButton("Start MIDI ~(≧▽≦)/~")
        self.midi_button.clicked.connect(self.start_midi_listener)

        midi_layout = QHBoxLayout()
        midi_layout.addWidget(self.midi_dropdown)
        midi_layout.addWidget(self.midi_button)

        # layouts
        main_layout.addLayout(carrier_layout)
        main_layout.addLayout(modulator_layout)
        main_layout.addLayout(index_layout)
        main_layout.addLayout(synthesis_layout)
        main_layout.addLayout(waveform_layout)  # Added waveform selector
        main_layout.addLayout(midi_layout)
        main_layout.addLayout(dist_length)
        main_layout.addLayout(decay_layout)

        self.setLayout(main_layout)
        self.fm_radio.toggled.connect(self.toggle_mod_index_visibility)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_midi_processing)
        self.timer.start(50)

    def create_dial(self, min_val, max_val, init_val, callback):
        dial = QDial()
        dial.setMinimum(min_val)
        dial.setMaximum(max_val)
        dial.setValue(init_val)
        dial.setNotchesVisible(True)
        dial.valueChanged.connect(callback)
        return dial

    def update_label(self, value):
        sender = self.sender()
        if sender == self.carrier_dial:
            self.carrier_label.setText(f"Carrier: {value} |(°Ω°)/")
        elif sender == self.modulator_dial:
            self.modulator_label.setText(f"Modulator: {value} ( ｀皿´)｡ﾐ/")
        elif sender == self.index_dial:
            self.index_label.setText(f"Mod Index: {value} (づ｡◕‿‿◕｡)づ")
        elif sender == self.dist_dial:
            self.dist_label.setText(f"Dist Orshun ┌П┐(ಠ_ಠ) {value}")
        elif sender == self.decay_dial:
            self.decay_label.setText(f"DECASTYSYD ／人◕ __ ◕人＼ {value}")

    def toggle_mod_index_visibility(self):
        is_fm = self.fm_radio.isChecked()
        self.index_dial.setVisible(is_fm)
        self.index_label.setVisible(is_fm)

    def start_midi_listener(self):
        threading.Thread(target=midi_listener, args=(self.midi_dropdown.currentText(),), daemon=True).start()

    def update_midi_processing(self):
        if not midi_queue.empty():
            freq, velocity, duration = midi_queue.get()
            selected_waveform = self.waveform_dropdown.currentText()
            synthesis_mode = "FM" if self.fm_radio.isChecked() else "AM"

            # dials
            mod_freq = self.modulator_dial.value()
            mod_index = self.index_dial.value()
            reverb_amount = self.dist_dial.value() / 100  # Normalize (1-100 → 0-1)
            decay = self.decay_dial.value() / 100  # norm (1-100 → 0-1)

            # base
            if synthesis_mode == "AM":
                sound = generate_am(freq, mod_freq, mod_index, duration)
            elif synthesis_mode == "FM":
                sound = generate_fm(freq, mod_freq, mod_index, duration)
            else:
                sound = generate_waveform(selected_waveform, freq, duration)

            sound *= velocity  # Velocity affects volume

            processed_sound = schrader_distort(sound, reverb_amount, decay)

            # play
            try:
                print(f"Playing sound with Reverb: {reverb_amount}, Decay: {decay}, Synthesis Mode: {synthesis_mode}")
                sd.play(processed_sound, samplerate=SR, blocking=False)
            except Exception as e:
                print(f"Error playing sound: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SynthControlPanel()
    window.setWindowTitle("Kawaii-Ascii Synth (◞థ౪థ)ᴖ")
    window.show()
    sys.exit(app.exec_())