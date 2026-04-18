import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================
ruta = os.path.dirname(__file__)

# ==========================================
# 1. CREAR DATASET
# ==========================================
df = pd.DataFrame({
    "ID": [1, 2, 3, 4],
    "Antiguedad": [5, 3, 7, 2],
    "Kilometraje": [50000, 30000, 70000, 25000],
    "Puertas": [4, 2, 4, 2],
    "Precio": [12000, 15000, 9000, 16000]
})

ruta_dataset = os.path.join(ruta, "dataset_autos.csv")
df.to_csv(ruta_dataset, index=False)

print("=== DATASET ORIGINAL ===")
print(df)

# ==========================================
# 2. DEFINIR VARIABLES
# ==========================================
X = df[["Antiguedad", "Kilometraje", "Puertas"]]
y = df["Precio"]

# ==========================================
# 3. DIVISIÓN ENTRENAMIENTO / PRUEBA
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

print("\n=== CONJUNTO DE ENTRENAMIENTO ===")
print(X_train)
print(y_train)

print("\n=== CONJUNTO DE PRUEBA ===")
print(X_test)
print(y_test)

# ==========================================
# 4. ENTRENAR MODELO
# ==========================================
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# ==========================================
# 5. PREDICCIONES
# ==========================================
y_pred = modelo.predict(X_test)

print("\n=== PREDICCIONES ===")
print("Valores reales:", list(y_test))
print("Valores predichos:", list(y_pred))

# ==========================================
# 6. MÉTRICAS
# ==========================================
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\n=== MÉTRICAS DE DESEMPEÑO ===")
print(f"MAE: {mae:.4f}")
print(f"MSE: {mse:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R2: {r2:.4f}")

# Guardar métricas
df_metricas = pd.DataFrame({
    "Metrica": ["MAE", "MSE", "RMSE", "R2"],
    "Valor": [mae, mse, rmse, r2]
})

ruta_metricas = os.path.join(ruta, "resultados_metricas.csv")
df_metricas.to_csv(ruta_metricas, index=False)

print("\n✅ Archivo guardado: resultados_metricas.csv")

# ==========================================
# 7. GRÁFICO REAL VS PREDICHO
# ==========================================
plt.figure(figsize=(8, 5))
plt.bar(["Real"], [y_test.values[0]], label="Precio real")
plt.bar(["Predicho"], [y_pred[0]], label="Precio predicho")
plt.title("Comparación entre precio real y precio predicho")
plt.ylabel("Precio (USD)")
plt.legend()

ruta_grafico = os.path.join(ruta, "comparacion_real_vs_predicho.png")
plt.savefig(ruta_grafico, bbox_inches="tight", dpi=200)
plt.close()

print("✅ Imagen guardada: comparacion_real_vs_predicho.png")

# ==========================================
# 8. COEFICIENTES DEL MODELO
# ==========================================
print("\n=== COEFICIENTES DEL MODELO ===")
for variable, coef in zip(X.columns, modelo.coef_):
    print(f"{variable}: {coef:.4f}")
print(f"Intercepto: {modelo.intercept_:.4f}")