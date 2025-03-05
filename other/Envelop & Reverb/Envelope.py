import numpy as np
import sounddevice as sd
from scipy.signal import square, sawtooth, lfilter

# Constants
SR = 44100  # Sample rate

def adsr_envelope(duration, attack, decay, sustain, release):
    """Generate an ADSR envelope."""
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    env = np.zeros_like(t)
    
    attack_samples = int(attack * SR)
    decay_samples = int(decay * SR)
    release_samples = int(release * SR)
    sustain_level = sustain
    
    if attack_samples > 0:
        env[:attack_samples] = np.linspace(0, 1, attack_samples)
    if decay_samples > 0:
        env[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain_level, decay_samples)
    sustain_samples = len(t) - (attack_samples + decay_samples + release_samples)
    if sustain_samples > 0:
        env[attack_samples + decay_samples: -release_samples] = sustain_level
    if release_samples > 0:
        env[-release_samples:] = np.linspace(sustain_level, 0, release_samples)
    
    return env

def generate_waveform(waveform, frequency, duration):
    """Generate basic waveforms."""
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

def apply_reverb(signal, reverb_amount=0.3, decay=0.6):
    """Simple Schroeder Reverb Effect."""
    delay_samples = int(0.03 * SR)  # 30ms delay
    feedback = decay
    
    # Create delayed signal
    reverb_signal = np.zeros_like(signal)
    for i in range(delay_samples, len(signal)):
        reverb_signal[i] = signal[i - delay_samples] * feedback
    
    return signal * (1 - reverb_amount) + reverb_signal * reverb_amount

def play_sound(waveform, frequency, duration, attack, decay, sustain, release, reverb_amount=0.3, amplitude=1.0):
    """Generate and play a sound with ADSR envelope and Reverb."""
    audio_signal = generate_waveform(waveform, frequency, duration)
    envelope = adsr_envelope(duration, attack, decay, sustain, release)
    audio_signal *= envelope * amplitude
    
    # Apply Reverb
    audio_signal = apply_reverb(audio_signal, reverb_amount)
    
    try:
        sd.play(audio_signal, samplerate=SR, blocking=False)
    except Exception as e:
        print(f"Error playing sound")

# Example usage
if __name__ == "__main__":
    play_sound("sine", 440, 2.0, 0.1, 0.2, 0.7, 0.5, reverb_amount=0.4)
