import pandas as pd
import numpy as np
import os

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================
RUTA = os.path.dirname(__file__)

def guardar_csv(df, nombre):
    ruta = os.path.join(RUTA, nombre)
    df.to_csv(ruta, index=False)
    print(f"✅ CSV guardado: {nombre}")

def guardar_excel(df, nombre):
    ruta = os.path.join(RUTA, nombre)
    df.to_excel(ruta, index=False)
    print(f"✅ Excel guardado: {nombre}")


# ==========================================
# LECCIÓN 1 - NUMPY
# ==========================================
def leccion_1_numpy():
    print("\n" + "=" * 50)
    print("LECCIÓN 1 - NUMPY")
    print("=" * 50)

    np.random.seed(42)

    ids = np.arange(1, 21)
    edades = np.random.randint(18, 65, size=20)
    compras = np.random.randint(1, 15, size=20)
    gasto_total = np.random.randint(5000, 300000, size=20)

    datos_numpy = np.column_stack((ids, edades, compras, gasto_total))

    print("Array generado:")
    print(datos_numpy[:5])

    print("\nOperaciones básicas:")
    print("Suma gasto_total:", np.sum(gasto_total))
    print("Media gasto_total:", np.mean(gasto_total))
    print("Conteo registros:", len(ids))
    print("Máximo gasto_total:", np.max(gasto_total))
    print("Mínimo gasto_total:", np.min(gasto_total))

    ruta_npy = os.path.join(RUTA, "leccion_1_numpy.npy")
    np.save(ruta_npy, datos_numpy)
    print("\n✅ Archivo NPY guardado: leccion_1_numpy.npy")

    return datos_numpy


# ==========================================
# LECCIÓN 2 - PANDAS
# ==========================================
def leccion_2_pandas():
    print("\n" + "=" * 50)
    print("LECCIÓN 2 - PANDAS")
    print("=" * 50)

    ruta_npy = os.path.join(RUTA, "leccion_1_numpy.npy")
    datos = np.load(ruta_npy)

    df = pd.DataFrame(datos, columns=[
        "cliente_id", "edad", "cantidad_compras", "gasto_total"
    ])

    print("Primeras filas:")
    print(df.head())

    print("\nÚltimas filas:")
    print(df.tail())

    print("\nEstadísticas descriptivas:")
    print(df.describe())

    print("\nFiltro: clientes con gasto_total > 150000")
    print(df[df["gasto_total"] > 150000])

    guardar_csv(df, "leccion_2_clientes.csv")
    return df


# ==========================================
# CREAR FUENTES ADICIONALES PARA LA LECCIÓN 3
# ==========================================
def crear_fuentes_adicionales():
    print("\n" + "=" * 50)
    print("CREACIÓN DE FUENTES ADICIONALES")
    print("=" * 50)

    df_excel = pd.DataFrame({
        "cliente_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "ciudad": ["Santiago", "Valparaíso", "Concepción", "La Serena", None, 
                   "Temuco", "Santiago", "Rancagua", "Talca", "Iquique", 
                   "Antofagasta", "Puerto Montt"],
        "categoria": ["Bronce", "Plata", "Oro", "Bronce", "Plata",
                      "Oro", "Bronce", None, "Plata", "Oro",
                      "Bronce", "Plata"]
    })

    guardar_excel(df_excel, "clientes_ecommerce.xlsx")

    tabla_web = pd.DataFrame({
        "cliente_id": [1, 2, 3, 4, 5, 13, 14, 15, 16, 17],
        "canal_origen": ["Web", "App", "Web", "Marketplace", "App",
                         "Web", "App", "Web", "Marketplace", "App"],
        "estado_cliente": ["Activo", "Activo", "Inactivo", "Activo", "Activo",
                           "Inactivo", "Activo", "Activo", "Inactivo", "Activo"]
    })

    html = tabla_web.to_html(index=False)
    ruta_html = os.path.join(RUTA, "tabla_web_clientes.html")
    with open(ruta_html, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ Tabla web simulada creada: tabla_web_clientes.html")


# ==========================================
# LECCIÓN 3 - OBTENCIÓN DE DATOS DESDE ARCHIVOS
# ==========================================
def leccion_3_fuentes():
    print("\n" + "=" * 50)
    print("LECCIÓN 3 - OBTENCIÓN DE DATOS")
    print("=" * 50)

    df_csv = pd.read_csv(os.path.join(RUTA, "leccion_2_clientes.csv"))
    df_excel = pd.read_excel(os.path.join(RUTA, "clientes_ecommerce.xlsx"))
    df_web = pd.read_html(os.path.join(RUTA, "tabla_web_clientes.html"))[0]

    print("CSV:")
    print(df_csv.head())

    print("\nExcel:")
    print(df_excel.head())

    print("\nTabla web:")
    print(df_web.head())

    # merge de fuentes
    df_merge = pd.merge(df_csv, df_excel, on="cliente_id", how="left")
    df_merge = pd.merge(df_merge, df_web, on="cliente_id", how="left")

    # concat de registros extra
    df_extra = pd.DataFrame({
        "cliente_id": [18, 19, 20, 21, 21],
        "edad": [33, np.nan, 61, 29, 29],
        "cantidad_compras": [3, 11, 5, 4, 4],
        "gasto_total": [40000, 290000, 1200000, 85000, 85000],  # 1200000 será outlier
        "ciudad": ["Arica", "Santiago", "Concepción", "Talca", "Talca"],
        "categoria": ["Bronce", "Oro", "Plata", "Bronce", "Bronce"],
        "canal_origen": ["Web", "App", "Marketplace", "Web", "Web"],
        "estado_cliente": ["Activo", "Activo", "Inactivo", "Activo", "Activo"]
    })

    df_consolidado = pd.concat([df_merge, df_extra], ignore_index=True)

    # meter nulos artificialmente para la limpieza
    df_consolidado.loc[2, "gasto_total"] = np.nan
    df_consolidado.loc[5, "ciudad"] = None
    df_consolidado.loc[7, "categoria"] = None

    guardar_csv(df_consolidado, "leccion_3_consolidado.csv")
    return df_consolidado


# ==========================================
# LECCIÓN 4 - NULOS Y OUTLIERS
# ==========================================
def detectar_outliers_iqr(df, columna):
    q1 = df[columna].quantile(0.25)
    q3 = df[columna].quantile(0.75)
    iqr = q3 - q1
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    return (df[columna] < limite_inferior) | (df[columna] > limite_superior)

def leccion_4_limpieza():
    print("\n" + "=" * 50)
    print("LECCIÓN 4 - VALORES PERDIDOS Y OUTLIERS")
    print("=" * 50)

    df = pd.read_csv(os.path.join(RUTA, "leccion_3_consolidado.csv"))

    print("Valores nulos por columna:")
    print(df.isnull().sum())

    # imputación numéricos
    df["edad"] = df["edad"].fillna(df["edad"].median())
    df["gasto_total"] = df["gasto_total"].fillna(df["gasto_total"].median())

    # imputación categóricos
    df["ciudad"] = df["ciudad"].fillna("Desconocida")
    df["categoria"] = df["categoria"].fillna(df["categoria"].mode()[0])
    df["canal_origen"] = df["canal_origen"].fillna("Desconocido")
    df["estado_cliente"] = df["estado_cliente"].fillna("Desconocido")

    print("\nValores nulos después de imputación:")
    print(df.isnull().sum())

    # detectar outliers con IQR
    outliers = detectar_outliers_iqr(df, "gasto_total")
    print("\nCantidad de outliers detectados en gasto_total:", outliers.sum())

    # tratamiento: cap al percentil 95
    p95 = df["gasto_total"].quantile(0.95)
    df.loc[df["gasto_total"] > p95, "gasto_total"] = p95

    guardar_csv(df, "leccion_4_limpio.csv")
    return df


# ==========================================
# LECCIÓN 5 - DATA WRANGLING
# ==========================================
def normalizar_minmax(serie):
    return (serie - serie.min()) / (serie.max() - serie.min())

def leccion_5_wrangling():
    print("\n" + "=" * 50)
    print("LECCIÓN 5 - DATA WRANGLING")
    print("=" * 50)

    df = pd.read_csv(os.path.join(RUTA, "leccion_4_limpio.csv"))

    print("Duplicados antes:", df.duplicated().sum())
    df = df.drop_duplicates()
    print("Duplicados después:", df.duplicated().sum())

    # transformar tipos de datos
    df["cliente_id"] = df["cliente_id"].astype(int)
    df["edad"] = df["edad"].astype(float)
    df["cantidad_compras"] = df["cantidad_compras"].astype(int)
    df["gasto_total"] = df["gasto_total"].astype(float)

    # nueva columna calculada
    df["ticket_promedio"] = df["gasto_total"] / df["cantidad_compras"]

    # apply / lambda
    df["segmento_edad"] = df["edad"].apply(
        lambda x: "Joven" if x < 30 else ("Adulto" if x < 50 else "Senior")
    )

    # map
    mapa_categoria = {"Bronce": 1, "Plata": 2, "Oro": 3}
    df["categoria_codigo"] = df["categoria"].map(mapa_categoria)

    # normalización
    df["gasto_total_normalizado"] = normalizar_minmax(df["gasto_total"])

    # discretización
    df["nivel_gasto"] = pd.cut(
        df["gasto_total"],
        bins=3,
        labels=["Bajo", "Medio", "Alto"]
    )

    # ordenar columnas
    columnas = [
        "cliente_id", "edad", "segmento_edad", "cantidad_compras",
        "gasto_total", "gasto_total_normalizado", "ticket_promedio",
        "nivel_gasto", "ciudad", "categoria", "categoria_codigo",
        "canal_origen", "estado_cliente"
    ]
    df = df[columnas]

    guardar_csv(df, "leccion_5_wrangling.csv")
    return df


# ==========================================
# LECCIÓN 6 - AGRUPAMIENTO Y PIVOTEO
# ==========================================
def leccion_6_agrupamiento():
    print("\n" + "=" * 50)
    print("LECCIÓN 6 - AGRUPAMIENTO Y PIVOTEO")
    print("=" * 50)

    df = pd.read_csv(os.path.join(RUTA, "leccion_5_wrangling.csv"))

    # groupby
    resumen_ciudad = df.groupby("ciudad").agg({
        "gasto_total": ["mean", "sum", "max"],
        "cantidad_compras": "mean",
        "ticket_promedio": "mean"
    }).reset_index()

    print("Resumen por ciudad:")
    print(resumen_ciudad.head())

    # pivot
    pivot_categoria = df.pivot_table(
        index="ciudad",
        columns="categoria",
        values="gasto_total",
        aggfunc="mean"
    ).reset_index()

    print("\nPivot por ciudad y categoría:")
    print(pivot_categoria.head())

    # melt
    melt_gasto = pd.melt(
        df,
        id_vars=["cliente_id", "ciudad"],
        value_vars=["gasto_total", "ticket_promedio"],
        var_name="metrica",
        value_name="valor"
    )

    print("\nMelt:")
    print(melt_gasto.head())

    # merge adicional
    df_beneficios = pd.DataFrame({
        "categoria": ["Bronce", "Plata", "Oro"],
        "beneficio": ["Descuento 5%", "Descuento 10%", "Descuento 15%"]
    })

    df_final = pd.merge(df, df_beneficios, on="categoria", how="left")

    guardar_csv(df_final, "dataset_final.csv")
    guardar_excel(df_final, "dataset_final.xlsx")

    return df_final, resumen_ciudad, pivot_categoria, melt_gasto


# ==========================================
# MAIN
# ==========================================
def main():
    leccion_1_numpy()
    leccion_2_pandas()
    crear_fuentes_adicionales()
    leccion_3_fuentes()
    leccion_4_limpieza()
    leccion_5_wrangling()
    leccion_6_agrupamiento()

    print("\n" + "=" * 50)
    print("✅ PROYECTO COMPLETADO")
    print("=" * 50)

if __name__ == "__main__":
    main()