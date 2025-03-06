import numpy as np



def adsr_envelope(x, a=0.1, d=0.1, s=0.7, r=0.2, sampling_rate=44100):
    n = len(x)
    attack_samples = int(a * sampling_rate)
    decay_samples = int(d * sampling_rate)
    release_samples = int(r * sampling_rate)
    sustain_samples = n - (attack_samples + decay_samples + release_samples)
    if sustain_samples < 0:
        raise ValueError("Invalid")
    if attack_samples > 0:
        attack = np.linspace(0, 1, attack_samples)
    else:
        attack = np.array([])
    if s is False:
        decay = np.linspace(1, 0, decay_samples)
        sustain = np.array([])
        release = np.array([])
    else:
        decay = np.linspace(1, s, decay_samples)
        sustain = np.full(sustain_samples, s)
        release = np.linspace(s, 0, release_samples)
    envelope = np.concatenate([attack, decay, sustain, release])
    envelope = np.resize(envelope, n)
    modulated_sound = x * envelope
    return modulated_sound, envelope
duration = 2
frequency = 440
sampling_rate = 44100
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
input_signal = np.sin(2 * np.pi * frequency * t)
enveloped_signal, envelope = adsr_envelope(input_signal, a=0.1, d=0.2, s=0.6, r=0.3)

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
