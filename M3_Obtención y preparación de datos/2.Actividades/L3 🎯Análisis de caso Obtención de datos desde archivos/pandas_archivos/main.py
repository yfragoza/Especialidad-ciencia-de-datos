import pandas as pd
import numpy as np
import os
from io import StringIO
from urllib.request import Request, urlopen

# ==================================================
# 0. RUTA DE TRABAJO
# ==================================================
ruta = os.path.dirname(__file__)

# ==================================================
# 1. CREACIÓN DE DATOS DE EJEMPLO
# ==================================================

# Archivo CSV de ejemplo
df_clientes = pd.DataFrame({
    "id": [1, 2, 3, 4, 4],
    "nombre": ["Ana", "Luis", "María", "Pedro", "Pedro"],
    "edad": [25, np.nan, 30, 22, 22],
    "ciudad": ["Santiago", "Valparaíso", None, "Concepción", "Concepción"]
})
df_clientes.to_csv(os.path.join(ruta, "datos_clientes.csv"), index=False)

# Archivo Excel de ejemplo
df_ventas = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "ventas": [1000, 1500, np.nan, 2000],
    "categoria": ["A", "B", "A", "C"]
})
df_ventas.to_excel(os.path.join(ruta, "datos_ventas.xlsx"), index=False)

# ==================================================
# 2. CARGA DE DATOS
# ==================================================

clientes = pd.read_csv(os.path.join(ruta, "datos_clientes.csv"))
ventas = pd.read_excel(os.path.join(ruta, "datos_ventas.xlsx"))

print("=== CSV ORIGINAL ===")
print(clientes)

print("\n=== EXCEL ORIGINAL ===")
print(ventas)

# Tabla web con encabezado de navegador para evitar 403
try:
    url = "https://www.worldometers.info/world-population/population-by-country/"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urlopen(req).read().decode("utf-8")
    tabla_web = pd.read_html(StringIO(html))[0]

    print("\n=== TABLA WEB ORIGINAL (primeras filas) ===")
    print(tabla_web.head())

except Exception as e:
    print("\n⚠️ No se pudo cargar la tabla web, pero el programa continúa.")
    print("Detalle:", e)
    tabla_web = pd.DataFrame({
        "Pais": ["Chile", "Argentina", "Perú"],
        "Poblacion": [19603733, 46234830, 34038964]
    })
    print("\n=== TABLA WEB DE RESPALDO ===")
    print(tabla_web)

# ==================================================
# 3. UNIÓN DE DATOS Y ESTADO ANTES DE LIMPIEZA
# ==================================================

df_antes = pd.merge(clientes, ventas, on="id", how="left")

print("\n=== DATOS ANTES DE LIMPIEZA ===")
print(df_antes)

print("\n=== VALORES NULOS POR COLUMNA ===")
print(df_antes.isnull().sum())

# ==================================================
# 4. LIMPIEZA Y ESTRUCTURACIÓN
# ==================================================

df = df_antes.copy()

# Imputación de valores nulos
df["edad"] = df["edad"].fillna(df["edad"].mean())
df["ciudad"] = df["ciudad"].fillna("Desconocida")
df["ventas"] = df["ventas"].fillna(df["ventas"].median())

# Eliminar duplicados
df = df.drop_duplicates()

# Ajustar tipos de datos
df["id"] = df["id"].astype(int)
df["edad"] = df["edad"].astype(float)
df["ventas"] = df["ventas"].astype(float)
df["nombre"] = df["nombre"].astype(str)
df["ciudad"] = df["ciudad"].astype(str)
df["categoria"] = df["categoria"].astype(str)

# ==================================================
# 5. TRANSFORMACIÓN Y OPTIMIZACIÓN
# ==================================================

# Selección de columnas relevantes
df = df[["id", "nombre", "edad", "ciudad", "ventas", "categoria"]]

# Renombrar columnas
df = df.rename(columns={
    "nombre": "Nombre",
    "edad": "Edad",
    "ciudad": "Ciudad",
    "ventas": "Ventas",
    "categoria": "Categoria"
})

# Ordenar por columna clave
df = df.sort_values(by="Ventas", ascending=False)

print("\n=== DATOS DESPUÉS DE LIMPIEZA ===")
print(df)

# ==================================================
# 6. EXPORTACIÓN
# ==================================================

df.to_csv(os.path.join(ruta, "datos_limpios.csv"), index=False)
df.to_excel(os.path.join(ruta, "datos_limpios.xlsx"), index=False)

print("\n✅ Archivos exportados correctamente en:")
print(ruta)
print("- datos_clientes.csv")
print("- datos_ventas.xlsx")
print("- datos_limpios.csv")
print("- datos_limpios.xlsx")