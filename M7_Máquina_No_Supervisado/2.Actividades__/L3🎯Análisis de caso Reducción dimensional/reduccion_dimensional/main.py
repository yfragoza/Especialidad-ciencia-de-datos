import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import make_classification
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================
ruta = os.path.dirname(__file__)
np.random.seed(42)

# ==========================================
# 1. GENERAR DATASET SIMULADO
# ==========================================
# Simulamos más de 50 columnas, como pide la actividad
X, y = make_classification(
    n_samples=300,
    n_features=60,
    n_informative=12,
    n_redundant=8,
    n_clusters_per_class=1,
    n_classes=3,
    random_state=42
)

columnas = [f"var_{i}" for i in range(1, 61)]
df = pd.DataFrame(X, columns=columnas)
df["segmento_cliente"] = y

# Introducir algunos valores nulos artificiales
for col in ["var_3", "var_10", "var_25", "var_41"]:
    idx = np.random.choice(df.index, size=10, replace=False)
    df.loc[idx, col] = np.nan

ruta_dataset = os.path.join(ruta, "survey_data.csv")
df.to_csv(ruta_dataset, index=False)

print("=== DATASET ORIGINAL ===")
print(df.head())
print("\nDimensiones:", df.shape)
print("\nValores nulos:")
print(df.isnull().sum().head(10))

# ==========================================
# 2. LIMPIEZA E IMPUTACIÓN
# ==========================================
X = df.drop(columns=["segmento_cliente"])
y = df["segmento_cliente"]

imputer = SimpleImputer(strategy="mean")
X_imputado = imputer.fit_transform(X)

# ==========================================
# 3. ESCALAMIENTO
# ==========================================
scaler = StandardScaler()
X_escalado = scaler.fit_transform(X_imputado)

print("\n✅ Datos imputados y escalados correctamente")

# ==========================================
# 4. PCA
# ==========================================
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_escalado)

df_pca = pd.DataFrame(X_pca, columns=["PCA_1", "PCA_2"])
df_pca["segmento_cliente"] = y.values

ruta_pca = os.path.join(ruta, "pca_2d.csv")
df_pca.to_csv(ruta_pca, index=False)

print("\n=== PCA ===")
print("Varianza explicada por componente:")
print(pca.explained_variance_ratio_)

# ==========================================
# 5. t-SNE
# ==========================================
tsne = TSNE(
    n_components=2,
    perplexity=30,
    learning_rate="auto",
    init="random",
    random_state=42
)
X_tsne = tsne.fit_transform(X_escalado)

df_tsne = pd.DataFrame(X_tsne, columns=["TSNE_1", "TSNE_2"])
df_tsne["segmento_cliente"] = y.values

ruta_tsne = os.path.join(ruta, "tsne_2d.csv")
df_tsne.to_csv(ruta_tsne, index=False)

print("\n=== t-SNE ===")
print(df_tsne.head())

# ==========================================
# 6. VISUALIZACIÓN PCA
# ==========================================
plt.figure(figsize=(8, 5))
for clase in sorted(df_pca["segmento_cliente"].unique()):
    subset = df_pca[df_pca["segmento_cliente"] == clase]
    plt.scatter(subset["PCA_1"], subset["PCA_2"], label=f"Grupo {clase}", alpha=0.7)

plt.title("Visualización 2D con PCA")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.legend()
plt.grid(True)

ruta_img_pca = os.path.join(ruta, "visualizacion_pca.png")
plt.savefig(ruta_img_pca, bbox_inches="tight", dpi=200)
plt.close()

print("✅ Imagen guardada: visualizacion_pca.png")

# ==========================================
# 7. VISUALIZACIÓN t-SNE
# ==========================================
plt.figure(figsize=(8, 5))
for clase in sorted(df_tsne["segmento_cliente"].unique()):
    subset = df_tsne[df_tsne["segmento_cliente"] == clase]
    plt.scatter(subset["TSNE_1"], subset["TSNE_2"], label=f"Grupo {clase}", alpha=0.7)

plt.title("Visualización 2D con t-SNE")
plt.xlabel("t-SNE 1")
plt.ylabel("t-SNE 2")
plt.legend()
plt.grid(True)

ruta_img_tsne = os.path.join(ruta, "visualizacion_tsne.png")
plt.savefig(ruta_img_tsne, bbox_inches="tight", dpi=200)
plt.close()

print("✅ Imagen guardada: visualizacion_tsne.png")

# ==========================================
# 8. CONCLUSIÓN EN CONSOLA
# ==========================================
print("\n=== REFLEXIÓN GENERAL ===")
print("PCA reduce dimensionalidad maximizando varianza global.")
print("t-SNE prioriza la separación visual local entre grupos.")
print("Para marketing, t-SNE suele ser más intuitivo visualmente, pero PCA es más interpretable y escalable.")