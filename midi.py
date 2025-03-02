"""
Midi Handling
"""


import numpy as np
import mido

def midi_to_freq(midi_note):
    return 440.0 * (2 ** ((midi_note - 69) / 12))

def process_midi(msg):
    # this is going to convert the MIDI to a numpy array and add to buffer
    midi_buffer = np.empty((0, 3), dtype=int)
    # global midi_buffer
    if msg.type in ["note_on", "note_off"]:
        event = np.array([[msg.note, msg.velocity, msg.time]])
        midi_buffer = np.vstack((midi_buffer, event))     # this is a vectorized aooend
        print(midi_buffer)

def midi_listener(port_name):
    with mido.open_input(port_name) as input_port:
        for msg in input_port:
            process_midi(msg)


