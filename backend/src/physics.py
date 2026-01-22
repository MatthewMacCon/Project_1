import numpy as np
import soundfile as sf
import os

# ===== НАСТРОЙКИ =====
SR = 22050          # частота дискретизации
DURATION = 2.0      # длительность в секундах
FREQ = 440          # частота сигнала (Гц)

# папка, куда сохраняем файлы
OUTPUT_DIR = "backend/samples"

# ===== СОЗДАНИЕ ПАПКИ, ЕСЛИ ЕЁ НЕТ =====
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===== ВРЕМЕННАЯ ОСЬ =====
t = np.linspace(0, DURATION, int(SR * DURATION), endpoint=False)

# ===== СИГНАЛЫ =====

# 1️⃣ Чистый синус
sine = np.sin(2 * np.pi * FREQ * t)

# 2️⃣ Меандр (square wave)
square = np.sign(np.sin(2 * np.pi * FREQ * t))

# 3️⃣ Пилообразная волна (sawtooth)
saw = 2 * (FREQ * t - np.floor(0.5 + FREQ * t))

# ===== СОХРАНЕНИЕ =====
sf.write(os.path.join(OUTPUT_DIR, "sine_440.wav"), sine, SR)
sf.write(os.path.join(OUTPUT_DIR, "square_440.wav"), square, SR)
sf.write(os.path.join(OUTPUT_DIR, "saw_440.wav"), saw, SR)

print("✅ Тестовые сигналы успешно созданы в backend/samples")