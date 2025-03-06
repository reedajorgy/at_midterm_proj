# Kawaii-Ascii Synth :3

## Overview
The Synth Control Panel is a Python-based synthesizer that provides real-time MIDI-controlled sound synthesis using **FM (Frequency Modulation) and AM (Amplitude Modulation)** techniques. The user interface is built with **PyQt5**, and the audio processing is handled via **NumPy, SciPy, and SoundDevice**.

## Features
- **FM and AM synthesis** with adjustable modulation parameters
- **Waveform selection** (Sine, Square, Sawtooth, Triangle)
- **Real-time MIDI input support**
- **Adjustable Carrier and Modulator frequencies**
- **Dynamic Modulation Index control**
- **User-friendly GUI with dials and dropdowns**
- **5 Second Playback (as per the "five big booms")**
- **A premade built in ADSR!!!!**
- **Comic Sans UI with Pink and Baby Blue theme (for aesthetic appeal!)**
- **Distortion using comb filtering (Schroeder-esque)** for enhanced spatial effects

## Requirements
To run the Synth Control Panel, ensure you have the following dependencies installed:

### Install dependencies using pip:
```sh
pip install requirements.txt
```

### Additional Requirements:
- A MIDI input device (optional, but recommended)
- Python 3.7 or newer

## Usage
### 1. Run the program
```sh
python app.py
```

### 2. Select the synthesis mode
Choose between **FM Synthesis** and **AM Synthesis** using the radio buttons.
- **FM Synthesis**: Modulates the carrier frequency.
- **AM Synthesis**: Modulates the amplitude.

### 3. Adjust Parameters
- **Carrier Frequency Dial**: Controls the base frequency of the sound.
- **Modulator Frequency Dial**: Adjusts the frequency of the modulating signal.
- **Modulation Index Dial**: Adjusts the modulation depth (only visible in AM mode).
- **Waveform Selection Dropdown**: Choose between sine, square, sawtooth, or triangle waves.
- **Distortion Amount Slider**: Controls the depth of the Schroeder distortion effect.
- **Decay Control**: Adjusts how long the distortion effect persists.

### 4. Connect MIDI
- Select an available MIDI input device from the dropdown.
- Click **"Start MIDI Listener"** to begin receiving MIDI notes.

### 5. Play Notes
- The synthesizer will generate sound based on incoming MIDI note data.
- The synthesis mode and parameters will dynamically affect the sound output.

## Code Breakdown
- `midi_to_freq()`: Converts MIDI note values to frequency (Hz).
- `generate_waveform()`: Creates a waveform based on user selection.
- `generate_am()` and `generate_fm()`: Apply AM and FM synthesis, respectively.
- `play_sound()`: Generates and plays the synthesized audio.
- `update_midi_processing()`: Processes incoming MIDI data and triggers sound.
- `toggle_mod_index_visibility()`: Hides or shows the modulation index based on synthesis mode.
- `schrader_distort()`: Implements Schroeder reverb with comb filtering for natural spatial effects.

## Future Enhancements
- **MIDI Out Support** for external synth control.
- **Envelope Generator Controls** for better note shaping.
- **Effects Processing** (More Reverb, Delay, Distortion etc).
- **Waveform Visualization** in real time.

## Acknowledgments
Reed, Adam, Iris for GTMT Intro Audio Tech II Midterm

## License
This project is licensed under the MIT License.

