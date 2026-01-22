import numpy as np
import librosa

class AudioAnalyzer:
    def __init__(self):
        self.files = {
            "sine_440.wav": "backend/samples/sine_440.wav",
            "saw_440.wav": "backend/samples/saw_440.wav",
            "square_440.wav": "backend/samples/square_440.wav"
        }

    def analyze_file(self, filename, sr=22050, duration=1.0, start=0.0, fmax=5000):
        if filename not in self.files:
            raise ValueError(f"Нет аудио: {filename}")
        filepath = self.files[filename]

        # грузим моно
        signal, sr = librosa.load(filepath, sr=sr, mono=True)

        # выбираем фрагмент (чтобы слева и справа было одно и то же)
        i0 = int(start * sr)
        N = int(duration * sr)
        x = signal[i0:i0 + N]
        if len(x) < N:
            # если файл короче — дополним нулями
            x = np.pad(x, (0, N - len(x)))

        # окно (уменьшает утечку)
        w = np.hanning(N)
        xw = x * w

        # FFT реального сигнала
        X = np.fft.rfft(xw)
        freqs = np.fft.rfftfreq(N, d=1/sr)

        # амплитудная нормировка: компенсируем окно
        mag = np.abs(X) / (np.sum(w) / 2.0)

        # dB для нормального вида (относительно 1.0)
        mag_db = 20 * np.log10(mag + 1e-12)

        # режем до fmax
        mask = freqs <= fmax
        freqs = freqs[mask]
        mag_db = mag_db[mask]

        return x, freqs, mag_db, sr, filepath
