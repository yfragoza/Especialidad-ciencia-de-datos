import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================
ruta = os.path.dirname(__file__)
np.random.seed(42)

# ==========================================
# 1. GENERAR DATASET CLÍNICO SIMULADO
# ==========================================
# Simulamos un dataset clínico con muchas variables
X, y = make_classification(
    n_samples=350,
    n_features=120,
    n_informative=20,
    n_redundant=15,
    n_classes=3,
    n_clusters_per_class=1,
    random_state=42
)

columnas = [f"variable_{i}" for i in range(1, 121)]
df = pd.DataFrame(X, columns=columnas)
df["diagnostico"] = y

ruta_dataset = os.path.join(ruta, "dataset_clinico_simulado.csv")
df.to_csv(ruta_dataset, index=False)

print("=== DATASET CLÍNICO SIMULADO ===")
print(df.head())
print("\nDimensiones del dataset:", df.shape)

# ==========================================
# 2. PREPARACIÓN DE DATOS
# ==========================================
X = df.drop(columns=["diagnostico"])
y = df["diagnostico"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("\n✅ Datos escalados con StandardScaler")

# ==========================================
# 3. APLICACIÓN DE PCA
# ==========================================
# Primero calculamos PCA completo para revisar varianza explicada
pca_full = PCA()
pca_full.fit(X_scaled)

varianza_explicada = pca_full.explained_variance_ratio_
varianza_acumulada = np.cumsum(varianza_explicada)

df_varianza = pd.DataFrame({
    "Componente": np.arange(1, len(varianza_explicada) + 1),
    "Varianza_Explicada": varianza_explicada,
    "Varianza_Acumulada": varianza_acumulada
})

ruta_varianza = os.path.join(ruta, "varianza_explicada_pca.csv")
df_varianza.to_csv(ruta_varianza, index=False)

# Elegir número óptimo de componentes:
# criterio: mantener al menos 90% de varianza explicada
n_componentes_optimo = np.argmax(varianza_acumulada >= 0.90) + 1

print("\n=== PCA ===")
print("Número óptimo de componentes para retener al menos 90% de varianza:", n_componentes_optimo)

# Scree plot
plt.figure(figsize=(10, 5))
plt.plot(range(1, len(varianza_explicada) + 1), varianza_acumulada, marker="o")
plt.axhline(y=0.90, linestyle="--", label="90% varianza")
plt.axvline(x=n_componentes_optimo, linestyle="--", label=f"{n_componentes_optimo} componentes")
plt.title("Varianza acumulada explicada por PCA")
plt.xlabel("Número de componentes")
plt.ylabel("Varianza acumulada")
plt.legend()
plt.grid(True)

ruta_scree = os.path.join(ruta, "scree_plot_pca.png")
plt.savefig(ruta_scree, bbox_inches="tight", dpi=200)
plt.close()

print("✅ Imagen guardada: scree_plot_pca.png")

# PCA en 2D para visualización
pca_2d = PCA(n_components=2)
X_pca_2d = pca_2d.fit_transform(X_scaled)

df_pca = pd.DataFrame(X_pca_2d, columns=["PCA_1", "PCA_2"])
df_pca["diagnostico"] = y.values

ruta_pca = os.path.join(ruta, "pca_componentes.csv")
df_pca.to_csv(ruta_pca, index=False)

# Visualización PCA 2D
plt.figure(figsize=(8, 5))
for clase in sorted(df_pca["diagnostico"].unique()):
    subset = df_pca[df_pca["diagnostico"] == clase]
    plt.scatter(subset["PCA_1"], subset["PCA_2"], label=f"Grupo {clase}", alpha=0.7)

plt.title("Visualización 2D con PCA")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.legend()
plt.grid(True)

ruta_img_pca = os.path.join(ruta, "visualizacion_pca_2d.png")
plt.savefig(ruta_img_pca, bbox_inches="tight", dpi=200)
plt.close()

print("✅ Imagen guardada: visualizacion_pca_2d.png")

# ==========================================
# 4. APLICACIÓN DE t-SNE
# ==========================================
tsne = TSNE(
    n_components=2,
    perplexity=30,
    learning_rate="auto",
    max_iter=1000,
    init="random",
    random_state=42
)

X_tsne = tsne.fit_transform(X_scaled)

df_tsne = pd.DataFrame(X_tsne, columns=["TSNE_1", "TSNE_2"])
df_tsne["diagnostico"] = y.values

ruta_tsne = os.path.join(ruta, "tsne_componentes.csv")
df_tsne.to_csv(ruta_tsne, index=False)

print("\n=== t-SNE ===")
print("Parámetros utilizados:")
print("perplexity = 30")
print("learning_rate = auto")
print("max_iter = 1000")

# Visualización t-SNE 2D
plt.figure(figsize=(8, 5))
for clase in sorted(df_tsne["diagnostico"].unique()):
    subset = df_tsne[df_tsne["diagnostico"] == clase]
    plt.scatter(subset["TSNE_1"], subset["TSNE_2"], label=f"Grupo {clase}", alpha=0.7)

plt.title("Visualización 2D con t-SNE")
plt.xlabel("t-SNE 1")
plt.ylabel("t-SNE 2")
plt.legend()
plt.grid(True)

ruta_img_tsne = os.path.join(ruta, "visualizacion_tsne_2d.png")
plt.savefig(ruta_img_tsne, bbox_inches="tight", dpi=200)
plt.close()

print("✅ Imagen guardada: visualizacion_tsne_2d.png")

# ==========================================
# 5. COMPARACIÓN Y CONCLUSIÓN
# ==========================================
print("\n=== ANÁLISIS COMPARATIVO ===")
print("PCA:")
print("- Técnica lineal")
print("- Útil para reducir dimensionalidad en pipelines de modelado")
print("- Permite analizar varianza explicada")
print("- Más interpretable y escalable")

print("\nt-SNE:")
print("- Técnica no lineal")
print("- Excelente para visualización de agrupamientos")
print("- No se enfoca en varianza explicada")
print("- Más costosa computacionalmente")

print("\n=== RECOMENDACIÓN FINAL ===")
print("Para visualización de clústeres: t-SNE suele mostrar mejor separación.")
print("Para incorporar reducción dimensional dentro de un pipeline predictivo: PCA es más útil.")