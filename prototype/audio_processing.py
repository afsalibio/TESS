import numpy as np
from scipy.signal import butter, lfilter

def normalize(data):
    """Normalize audio data to range [-1, 1]."""
    max_val = np.max(np.abs(data))
    return data / max_val if max_val > 0 else data

def bandpass_filter(data, lowcut, highcut, samplerate):
    """Apply a bandpass filter to the audio waveform."""
    nyquist = 0.5 * samplerate
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(1, [low, high], btype="band")
    return lfilter(b, a, data)

def compress(data, threshold=0.1, ratio=4):
    """Apply dynamic range compression."""
    compressed = np.copy(data)
    compressed[data > threshold] = threshold + (data[data > threshold] - threshold) / ratio
    return compressed