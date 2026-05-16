import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
import umap
from sklearn.metrics import silhouette_score

import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# LOAD
# =========================

df = pd.read_csv("music_vectors.csv")

feature_cols = [c for c in df.columns if c != "filename"]

X = df[feature_cols]

# =========================
# SCALE
# =========================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# =========================
# PCA BEFORE KMEANS
# =========================

# сохраняем 95% информации
pca = PCA(n_components=0.95, random_state=42)
X_pca = pca.fit_transform(X_scaled)


# =========================
# FIND BEST K
# =========================

scores = []

K_RANGE = range(2, 9)

for k in K_RANGE:
    agg = AgglomerativeClustering(
        n_clusters=k,
        metric='cosine',
        linkage='average',
    )

    labels = agg.fit_predict(X_pca)

    score = silhouette_score(X_pca, labels, metric="cosine")

    scores.append(score)

best_k = K_RANGE[np.argmax(scores)]

print("\nSilhouette scores:")

for k, s in zip(K_RANGE, scores):
    print(f"K={k}: {s:.3f}")

print(f"\nЛучшее число кластеров: {best_k}")

# =========================
# FINAL KMEANS
# =========================

agg = AgglomerativeClustering(
    n_clusters=best_k,
    metric='cosine',
    linkage='average',
)

df["cluster"] = agg.fit_predict(X_pca)

# =========================
# PLOT
# =========================
reducer = umap.UMAP(
    n_components=2,
    n_neighbors=10,
    min_dist=0.1,
    metric="cosine",
    random_state=42
)
X_umap = reducer.fit_transform(X_scaled)
df["umap_x"] = X_umap[:, 0]
df["umap_y"] = X_umap[:, 1]

plt.figure(figsize=(14, 9))

sns.scatterplot(
    data=df,
    x="umap_x",
    y="umap_y",
    hue="cluster",
    palette="viridis",
    s=120,
    alpha=0.85
)

plt.title("Music Clusters", fontsize=18)

plt.grid(alpha=0.3)

plt.savefig("music_clusters.png", dpi=300)

print("\nГрафик сохранён: music_clusters.png")

# =========================
# CLUSTER ANALYSIS
# =========================

print("\n" + "=" * 50)
print("CLUSTER ANALYSIS")
print("=" * 50)

for cluster_id in sorted(df["cluster"].unique()):

    cluster_tracks = df[df["cluster"] == cluster_id]

    print(f"\nCLUSTER #{cluster_id}")
    print(f"Tracks count: {len(cluster_tracks)}")

    sample_size = min(7, len(cluster_tracks))

    samples = cluster_tracks["filename"].sample(
        sample_size,
        random_state=42
    )

    for track in samples:
        print(f"  • {track}")