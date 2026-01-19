import numpy as np
import librosa
from scipy.fft import fft, fftfreq


class AudioAnalyzer:
    def __init__(self):
        self.files = {
            "Песня": "backend/samples/song.wav",
            "Гитара": "backend/samples/guitar.wav",
            "Птицы": "backend/samples/birds.wav"
        }

    def analyze_file(self, filename):
        if filename not in self.files:
            raise ValueError(f"Нет аудио: {filename}")
        filepath = self.files[filename]

        signal, sr = librosa.load(filepath, sr=22050)
        N = len(signal)
        yf = fft(signal)
        freqs = fftfreq(N, 1 / sr)[:N // 2]
        amps = np.abs(yf[:N // 2])
        return signal[:5000], freqs[:2500], amps[:2500], sr, filepath  # + filepath!
