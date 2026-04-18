import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler, StandardScaler

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================
ruta = os.path.dirname(__file__)

# ==========================================
# 1. CREAR DATASET INICIAL
# ==========================================
df = pd.DataFrame({
    "ID": [1, 2, 3, 4],
    "Edad": [25, 45, 30, 40],
    "Ciudad": ["Madrid", "Sevilla", "Madrid", "Barcelona"],
    "Ingresos": [30000, 50000, np.nan, 40000]
})

# Guardar dataset original
ruta_original = os.path.join(ruta, "dataset_original.csv")
df.to_csv(ruta_original, index=False)

print("=== DATASET ORIGINAL ===")
print(df)

# ==========================================
# 2. IMPUTAR VALOR FALTANTE EN INGRESOS
# ==========================================
imputer = SimpleImputer(strategy="mean")
df["Ingresos"] = imputer.fit_transform(df[["Ingresos"]])

print("\n=== DESPUÉS DE IMPUTAR INGRESOS ===")
print(df)

# ==========================================
# 3. LABEL ENCODING PARA CIUDAD
# ==========================================
label_encoder = LabelEncoder()
df["Ciudad_Label"] = label_encoder.fit_transform(df["Ciudad"])

print("\n=== LABEL ENCODING ===")
print(df[["Ciudad", "Ciudad_Label"]])

# ==========================================
# 4. ONE-HOT ENCODING PARA CIUDAD
# ==========================================
one_hot = pd.get_dummies(df["Ciudad"], prefix="Ciudad")
df_onehot = pd.concat([df, one_hot], axis=1)

print("\n=== ONE-HOT ENCODING ===")
print(df_onehot)

# ==========================================
# 5. VARIABLES DUMMY PARA CIUDAD
# ==========================================
dummies = pd.get_dummies(df["Ciudad"], prefix="Ciudad", drop_first=True)
df_dummy = pd.concat([df, dummies], axis=1)

print("\n=== VARIABLES DUMMY ===")
print(df_dummy)

# ==========================================
# 6. ESCALAMIENTO DE EDAD E INGRESOS
# ==========================================
columnas_numericas = ["Edad", "Ingresos"]

# Min-Max
scaler_minmax = MinMaxScaler()
df_dummy[["Edad_MinMax", "Ingresos_MinMax"]] = scaler_minmax.fit_transform(df_dummy[columnas_numericas])

# Z-Score
scaler_zscore = StandardScaler()
df_dummy[["Edad_ZScore", "Ingresos_ZScore"]] = scaler_zscore.fit_transform(df_dummy[columnas_numericas])

print("\n=== DATASET FINAL PREPROCESADO ===")
print(df_dummy)

# ==========================================
# 7. GUARDAR DATASET PREPROCESADO
# ==========================================
ruta_preprocesado = os.path.join(ruta, "dataset_preprocesado.csv")
df_dummy.to_csv(ruta_preprocesado, index=False)

print("\n✅ Archivo guardado: dataset_preprocesado.csv")

# ==========================================
# 8. CAPTURA SIMPLE DE DATOS ESCALADOS
# ==========================================
fig, ax = plt.subplots(figsize=(10, 2))
ax.axis("off")

tabla = ax.table(
    cellText=df_dummy[[
        "Edad", "Ingresos",
        "Edad_MinMax", "Ingresos_MinMax",
        "Edad_ZScore", "Ingresos_ZScore"
    ]].round(3).values,
    colLabels=[
        "Edad", "Ingresos",
        "Edad_MinMax", "Ingresos_MinMax",
        "Edad_ZScore", "Ingresos_ZScore"
    ],
    loc="center"
)

tabla.auto_set_font_size(False)
tabla.set_fontsize(9)
tabla.scale(1.2, 1.5)

ruta_imagen = os.path.join(ruta, "captura_datos_escalados.png")
plt.savefig(ruta_imagen, bbox_inches="tight", dpi=200)
plt.close()

print("✅ Imagen guardada: captura_datos_escalados.png")