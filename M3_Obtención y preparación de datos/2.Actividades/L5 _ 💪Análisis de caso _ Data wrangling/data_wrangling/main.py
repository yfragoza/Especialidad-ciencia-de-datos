import pandas as pd
import numpy as np
import os

# ==========================================
# 0. RUTA DE TRABAJO
# ==========================================
ruta = os.path.dirname(__file__)

# ==========================================
# 1. CREAR DATASET DE EJEMPLO
# ==========================================
df_ejemplo = pd.DataFrame({
    "id": [1, 2, 3, 4, 5, 5, 6],
    "cliente": ["Ana", "Luis", "María", "Pedro", "Camila", "Camila", "Diego"],
    "edad": [25, np.nan, 30, 22, 28, 28, np.nan],
    "ciudad": ["Santiago", "Valparaíso", None, "Concepción", "Santiago", "Santiago", "La Serena"],
    "ingresos": [1200, 1500, np.nan, 1800, 2100, 2100, 1600],
    "categoria": ["Bronce", "Plata", "Oro", "Plata", "Oro", "Oro", None]
})

# Guardar CSV original
ruta_csv_original = os.path.join(ruta, "clientes_original.csv")
df_ejemplo.to_csv(ruta_csv_original, index=False)

# ==========================================
# 2. CARGA Y EXPLORACIÓN DE DATOS
# ==========================================
df = pd.read_csv(ruta_csv_original)

print("=== HEAD() ===")
print(df.head())

print("\n=== INFO() ===")
df.info()

print("\n=== DESCRIBE() ===")
print(df.describe(include="all"))

print("\n=== VALORES NULOS ===")
print(df.isnull().sum())

print("\n=== FILAS DUPLICADAS ===")
print(df.duplicated().sum())

# Guardar copia antes de limpieza
df_antes = df.copy()

# ==========================================
# 3. LIMPIEZA Y TRANSFORMACIÓN
# ==========================================

# Imputar nulos numéricos
df["edad"] = df["edad"].fillna(df["edad"].median())
df["ingresos"] = df["ingresos"].fillna(df["ingresos"].mean())

# Imputar nulos categóricos
df["ciudad"] = df["ciudad"].fillna("Desconocida")
df["categoria"] = df["categoria"].fillna(df["categoria"].mode()[0])

# Eliminar duplicados
df = df.drop_duplicates()

# Convertir categórica en numérica con mapeo
mapa_categoria = {"Bronce": 1, "Plata": 2, "Oro": 3}
df["categoria_codigo"] = df["categoria"].map(mapa_categoria)

# ==========================================
# 4. OPTIMIZACIÓN Y ESTRUCTURACIÓN
# ==========================================

# Groupby y agregación
resumen_ciudad = df.groupby("ciudad").agg({
    "ingresos": ["mean", "max", "min"],
    "edad": "mean"
})

print("\n=== RESUMEN POR CIUDAD ===")
print(resumen_ciudad)

# Filtrar subconjunto de interés
clientes_altos_ingresos = df[df["ingresos"] > 1600]

print("\n=== CLIENTES CON INGRESOS > 1600 ===")
print(clientes_altos_ingresos)

# Renombrar columnas
df = df.rename(columns={
    "cliente": "Cliente",
    "edad": "Edad",
    "ciudad": "Ciudad",
    "ingresos": "Ingresos",
    "categoria": "Categoria"
})

# Reorganizar columnas
df = df[["id", "Cliente", "Edad", "Ciudad", "Ingresos", "Categoria", "categoria_codigo"]]

# Ordenar datos
df = df.sort_values(by="Ingresos", ascending=False)

print("\n=== DATAFRAME DESPUÉS DE TRANSFORMACIÓN ===")
print(df)

# ==========================================
# 5. EXPORTACIÓN
# ==========================================
ruta_csv_limpio = os.path.join(ruta, "clientes_limpios.csv")
ruta_excel_limpio = os.path.join(ruta, "clientes_limpios.xlsx")

df.to_csv(ruta_csv_limpio, index=False)
df.to_excel(ruta_excel_limpio, index=False)

print("\n✅ Archivos exportados correctamente:")
print("- clientes_original.csv")
print("- clientes_limpios.csv")
print("- clientes_limpios.xlsx")