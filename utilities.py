"""
Really HANDLING it
"""
import mido
import queue

SR = 44100  # Sample rate
midi_queue = queue.Queue()

def midi_to_freq(midi_note):
    return 440.0 * (2 ** ((midi_note - 69) / 12))

def list_midi_devices():
    return mido.get_input_names()

