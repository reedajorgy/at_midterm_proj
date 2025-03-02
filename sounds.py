'''
backend sounds
'''

from IPython.display import Audio, display
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss


from IPython.display import Audio, display
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss



# Constants
SR = 44100  # Sample Rate

def am_synthesis(cf, mf, sr=SR, d=1.0):
    """
    Generates an Amplitude Modulated (AM) signal.

    Parameters:
        cf (float): Carrier frequency in Hz
        mf (float): Modulator frequency in Hz
        sr (int): Sample rate (default: 44100 Hz)
        d (float): Duration in seconds

    Returns:
        np.ndarray: Generated AM signal
    """
    t = np.linspace(0, d, int(sr * d), endpoint=False)
    carrier = np.sin(2 * np.pi * cf * t)
    modulator = np.sin(2 * np.pi * mf * t)
    return (1 + modulator) * carrier

def fm_synthesis(cf, mf, index=1.0, sr=SR, d=1.0):
    """
    Generates a Frequency Modulated (FM) signal.

    Parameters:
        cf (float): Carrier frequency in Hz
        mf (float): Modulator frequency in Hz
        index (float): Modulation index (controls depth)
        sr (int): Sample rate (default: 44100 Hz)
        d (float): Duration in seconds

    Returns:
        np.ndarray: Generated FM signal
    """
    t = np.linspace(0, d, int(sr * d), endpoint=False)
    iphase = 2 * np.pi * cf * t + index * np.sin(2 * np.pi * mf * t)
    return np.sin(iphase)


