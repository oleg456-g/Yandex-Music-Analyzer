# 🎵 Music Recommendation System

Система анализа и кластеризации музыки на Python.
Проект скачивает любимые треки из Yandex Music, извлекает аудио-признаки, строит музыкальные векторы и группирует похожие треки.

---

## ✨ Возможности

* Скачивание лайкнутых треков из Yandex Music
* Анализ MP3 через `Librosa`
* Извлечение audio features
* Кластеризация похожей музыки
* Визуализация музыкальных кластеров через UMAP
* Основа для Spotify-like recommendation system

---

## 🛠️ Стек

* Python
* Librosa
* Scikit-learn
* UMAP
* Pandas
* Matplotlib
* Seaborn
* Yandex Music API

---

# 📁 Структура проекта

```bash
project/
│
├── analyse_music/
│   ├── analyse.py
│   └── claster_music.py
│
├── parse_music_database/
│   ├── get_api_for_yandex_music.py
│   ├── parser_music_from_yandex.py
│   └── secret.py
│
├── yandex_music_database/
│
├── music_vectors.csv
├── music_clusters.png
├── requirements.txt
└── README.md
```

---

# ⚙️ Установка

## 1. Клонирование репозитория

```bash
git clone https://github.com/oleg456-g/Yandex-Music-Analyzer.git
cd Yandex-Music-Analyzer
```

---

## 2. Создание виртуального окружения

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

---

# 🔑 Получение API токена Yandex Music

Запусти:

```bash
python parse_music_database/get_api_for_yandex_music.py
```

После авторизации токены автоматически сохранятся в:

```bash
parse_music_database/secret.py
```

---

# ⬇️ Скачивание треков

```bash
python parse_music_database/parser_music_from_yandex.py
```

Музыка загрузится в папку:

```bash
yandex_music_database/
```

---

# 🎧 Анализ музыки

```bash
python analyse_music/analyse.py
```

Из треков извлекаются:

* Tempo (BPM)
* MFCC
* Chroma
* Spectral Contrast
* RMS Energy
* Spectral Centroid
* Spectral Bandwidth
* Zero Crossing Rate

После анализа создаётся файл:

```bash
music_vectors.csv
```

---

# 🧠 Кластеризация музыки

```bash
python analyse_music/claster_music.py
```

Pipeline:

```text
MP3
 ↓
Audio Features
 ↓
StandardScaler
 ↓
PCA
 ↓
AgglomerativeClustering
 ↓
UMAP Visualization
```

---

# 📊 Результат

После запуска создаётся:

```bash
music_clusters.png
```

UMAP визуализирует музыкальные связи между треками:

* близко → похожие треки
* далеко → разные жанры / вайбы

---

# 🤖 Почему AgglomerativeClustering?

Музыка плохо кластеризуется через KMeans, потому что музыкальные данные:

* нелинейны
* редко образуют шарообразные кластеры

`AgglomerativeClustering`:

* лучше работает с cosine similarity
* лучше ловит настроение и жанры
* стабильнее на маленьких датасетах

---

# 🚀 Планы
* FAISS Vector Search
* Deep Audio Embeddings
* Spotify API
* WEB Интерфейс

---

# 💡 Идея recommendation system

```text
Track
 ↓
Vector Embedding
 ↓
Cosine Similarity
 ↓
Nearest Neighbors
 ↓
Recommendations
```

---

# 📦 Основные библиотеки

* `librosa`
* `scikit-learn`
* `umap-learn`
* `pandas`
* `matplotlib`
* `seaborn`
* `yandex-music`

Полный список:

```bash
requirements.txt
```
