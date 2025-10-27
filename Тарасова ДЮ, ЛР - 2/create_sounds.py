import os
import wave
import math
import struct

def create_sound(filename, frequency, duration, wave_type="sine"):
    """Создает простой звуковой файл"""
    sample_rate = 44100
    frames = int(duration * sample_rate)
    
    # Создаем папку если нет
    os.makedirs('sounds', exist_ok=True)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # mono
        wav_file.setsampwidth(2)  # 2 bytes
        wav_file.setframerate(sample_rate)
        
        for i in range(frames):
            if wave_type == "sine":
                value = int(32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
            elif wave_type == "square":
                value = 32767 if math.sin(2.0 * math.pi * frequency * i / sample_rate) > 0 else -32767
            elif wave_type == "sawtooth":
                value = int(32767.0 * (2 * (i * frequency / sample_rate % 1) - 1))
            
            data = struct.pack('<h', value)
            wav_file.writeframes(data)
    
    print(f"Создан файл: {filename}")

# Создаем звуки для игры
create_sound("sounds/laser.wav", 1200, 0.2, "square")      # Резкий звук лазера
create_sound("sounds/explosion.wav", 80, 0.5, "sawtooth")  # Низкий взрыв
create_sound("sounds/life_lost.wav", 300, 0.8, "sine")     # Грустный звук
create_sound("sounds/game_over.wav", 150, 1.5, "sine")     # Драматичный финал

print("Все звуковые файлы созданы в папке sounds/")
