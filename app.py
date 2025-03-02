'''
Reed midterm project
https://www.pythonguis.com/tutorials/pyqt-signals-slots-events/

'''


import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QDial,
    QComboBox, QLabel, QCheckBox, QRadioButton, QButtonGroup
)

class SynthControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        # === Main Layout ===
        main_layout = QVBoxLayout()

        # === Dials Layout (Carrier & Modulator Side by Side) ===
        dial_layout = QHBoxLayout()

        # Carrier Frequency Dial
        self.carrier_dial = QDial()
        self.carrier_dial.setMinimum(100)
        self.carrier_dial.setMaximum(2000)
        self.carrier_dial.setValue(500)
        self.carrier_dial.setNotchesVisible(True)
        self.carrier_dial.valueChanged.connect(self.update_carrier_label)

        self.carrier_label = QLabel("Carrier Freq: 500 Hz")
        carrier_layout = QVBoxLayout()
        carrier_layout.addWidget(self.carrier_dial)
        carrier_layout.addWidget(self.carrier_label)
        dial_layout.addLayout(carrier_layout)

        # Modulator Frequency Dial
        self.modulator_dial = QDial()
        self.modulator_dial.setMinimum(10)
        self.modulator_dial.setMaximum(1000)
        self.modulator_dial.setValue(50)
        self.modulator_dial.setNotchesVisible(True)
        self.modulator_dial.valueChanged.connect(self.update_modulator_label)

        self.modulator_label = QLabel("Modulator Freq: 50 Hz")
        modulator_layout = QVBoxLayout()
        modulator_layout.addWidget(self.modulator_dial)
        modulator_layout.addWidget(self.modulator_label)
        dial_layout.addLayout(modulator_layout)

        main_layout.addLayout(dial_layout)  # Add dials to main layout

        # === Note Length Dial ===
        self.length_dial = QDial()
        self.length_dial.setMinimum(50)   # 50ms
        self.length_dial.setMaximum(2000) # 2000ms (2s)
        self.length_dial.setValue(500)
        self.length_dial.setNotchesVisible(True)
        self.length_dial.valueChanged.connect(self.update_length_label)

        self.length_label = QLabel("Length 500 ms")
        length_layout = QVBoxLayout()
        length_layout.addWidget(self.length_dial)
        length_layout.addWidget(self.length_label)
        main_layout.addLayout(length_layout)

        # === Modulation Index Dial (Visible Only for FM) ===
        self.index_dial = QDial()
        self.index_dial.setMinimum(1)
        self.index_dial.setMaximum(10)
        self.index_dial.setValue(2)
        self.index_dial.setNotchesVisible(True)
        self.index_dial.valueChanged.connect(self.update_index_label)

        self.index_label = QLabel("Mod Index: 2")
        index_layout = QVBoxLayout()
        index_layout.addWidget(self.index_dial)
        index_layout.addWidget(self.index_label)
        main_layout.addLayout(index_layout)

        # === Dropdown Menu for Waveform Selection ===
        self.dropdown = QComboBox()
        self.dropdown.addItems(["Sine", "Square", "Sawtooth", "Triangle"])
        self.dropdown.currentIndexChanged.connect(self.dropdown_changed)

        main_layout.addWidget(QLabel("Waveform:"))
        main_layout.addWidget(self.dropdown)

        # === Toggle Switch for AM/FM Selection ===
        self.am_radio = QRadioButton("AM Synthesis")
        self.fm_radio = QRadioButton("FM Synthesis")
        self.fm_radio.setChecked(True)  # Default to FM

        self.synthesis_mode = QButtonGroup()
        self.synthesis_mode.addButton(self.am_radio)
        self.synthesis_mode.addButton(self.fm_radio)

        self.am_radio.toggled.connect(self.synthesis_mode_changed)
        self.fm_radio.toggled.connect(self.synthesis_mode_changed)

        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.am_radio)
        mode_layout.addWidget(self.fm_radio)
        main_layout.addLayout(mode_layout)

        # === Enable/Disable Modulation Toggle ===
        self.toggle_modulation = QCheckBox("Enable Modulation")
        self.toggle_modulation.setChecked(True)
        self.toggle_modulation.toggled.connect(self.toggle_changed)
        main_layout.addWidget(self.toggle_modulation)

        # === Set Layout ===
        self.setLayout(main_layout)

        # Initially show/hide modulation index dial
        self.synthesis_mode_changed()

    def update_carrier_label(self, value):
        self.carrier_label.setText(f"Carrier {value} Hz")

    def update_modulator_label(self, value):
        self.modulator_label.setText(f"Modulator {value} Hz")

    def update_length_label(self, value):
        self.length_label.setText(f"{value} ms")

    def update_index_label(self, value):
        self.index_label.setText(f"Mod Index: {value}")

    def dropdown_changed(self, index):
        waveform = self.dropdown.currentText()
        print(f"Selected waveform: {waveform}")

    def synthesis_mode_changed(self):
        mode = "AM" if self.am_radio.isChecked() else "FM"
        print(f"Synthesis Mode: {mode}")

        # Show Modulation Index Dial only if FM is selected
        self.index_dial.setVisible(self.fm_radio.isChecked())
        self.index_label.setVisible(self.fm_radio.isChecked())

    def toggle_changed(self, checked):
        print(f"Modulation Enabled: {checked}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SynthControlPanel()
    window.setWindowTitle("Synth Control Panel")
    window.show()
    sys.exit(app.exec_())








