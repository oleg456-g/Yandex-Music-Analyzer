import os
import librosa
import numpy as np
import pandas as pd

def to_scalar(x):
    arr = np.asarray(x, dtype=float)
    if arr.size == 0 or not np.isfinite(arr).any():
        return 0.0
    return float(arr.reshape(-1).mean())

def extract_audio_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=22050, mono=True)

        # Темп
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo = to_scalar(tempo)

        # Спектральный центроид
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

        # Хрома
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        chroma_std = np.std(chroma, axis=1)

        # MFCC
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfcc, axis=1)
        mfcc_std = np.std(mfcc, axis=1)

        # Дополнительно полезные фичи
        rms = librosa.feature.rms(y=y)[0]
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

        features = {
            "tempo": tempo,
            "spectral_centroid_mean": float(np.mean(spectral_centroids)),
            "spectral_centroid_std": float(np.std(spectral_centroids)),
            "rms_mean": float(np.mean(rms)),
            "rms_std": float(np.std(rms)),
            "zcr_mean": float(np.mean(zcr)),
            "zcr_std": float(np.std(zcr)),
            "spectral_bandwidth_mean": float(np.mean(spectral_bandwidth)),
            "spectral_bandwidth_std": float(np.std(spectral_bandwidth)),
            "spectral_rolloff_mean": float(np.mean(spectral_rolloff)),
            "spectral_rolloff_std": float(np.std(spectral_rolloff)),
        }

        for i, val in enumerate(chroma_mean):
            features[f"chroma_mean_{i}"] = float(val)
        for i, val in enumerate(chroma_std):
            features[f"chroma_std_{i}"] = float(val)

        for i, val in enumerate(mfcc_mean):
            features[f"mfcc_mean_{i}"] = float(val)
        for i, val in enumerate(mfcc_std):
            features[f"mfcc_std_{i}"] = float(val)

        for i in range(spectral_contrast.shape[0]):
            features[f"spectral_contrast_mean_{i}"] = float(np.mean(spectral_contrast[i]))
            features[f"spectral_contrast_std_{i}"] = float(np.std(spectral_contrast[i]))

        return features

    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")
        return None

music_dir = 'yandex_music_database'
dataset = []

print("Начинаем спектральный анализ твоих MP3 файлов...")
for filename in os.listdir(music_dir):
    if filename.endswith('.mp3'):
        file_path = os.path.join(music_dir, filename)
        print(f"Анализирую трек: {filename}")
        
        features = extract_audio_features(file_path)
        if features:
            features['filename'] = filename
            dataset.append(features)


if dataset:
    df_features = pd.DataFrame(dataset)
    df_features.to_csv('music_vectors.csv', index=False, encoding='utf-8')
    print(f"\nАнализ завершен! Создан файл 'music_vectors.csv'. Успешно оцифровано треков: {len(df_features)}")
    print(df_features.head(3))
else:
    print("Не удалось извлечь фичи. Проверь, не пуста ли папка с музыкой.")