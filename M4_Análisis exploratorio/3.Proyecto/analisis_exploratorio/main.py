import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

from sklearn.metrics import mean_squared_error, mean_absolute_error

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================
RUTA = os.path.dirname(__file__)
RUTA_GRAFICOS = os.path.join(RUTA, "graficos")
RUTA_RESULTADOS = os.path.join(RUTA, "resultados")

os.makedirs(RUTA_GRAFICOS, exist_ok=True)
os.makedirs(RUTA_RESULTADOS, exist_ok=True)

sns.set_theme(style="whitegrid")


def guardar_grafico(nombre):
    ruta = os.path.join(RUTA_GRAFICOS, nombre)
    plt.savefig(ruta, bbox_inches="tight")
    print(f"✅ Gráfico guardado: {nombre}")


# ==========================================
# LECCIÓN 1 - GENERAR DATASET E IDA
# ==========================================
def generar_dataset():
    np.random.seed(42)

    n = 300

    df = pd.DataFrame({
        "cliente_id": range(1, n + 1),
        "edad": np.random.randint(18, 70, n),
        "visitas_web": np.random.randint(1, 60, n),
        "compras_realizadas": np.random.randint(0, 15, n),
        "monto_compra": np.random.normal(120000, 45000, n).round(0),
        "devoluciones": np.random.randint(0, 4, n),
        "resena_score": np.random.randint(1, 6, n),
        "categoria_favorita": np.random.choice(
            ["Tecnología", "Moda", "Hogar", "Deportes"], n
        ),
        "canal_origen": np.random.choice(
            ["Orgánico", "Publicidad", "Email", "Redes Sociales"], n
        ),
        "cliente_frecuente": np.random.choice(
            ["Sí", "No"], n, p=[0.35, 0.65]
        )
    })

    # Ajustes para hacerlo más realista
    df["monto_compra"] = df["monto_compra"].clip(lower=5000)
    df.loc[np.random.choice(df.index, 8, replace=False), "monto_compra"] *= 2.5
    df.loc[np.random.choice(df.index, 6, replace=False), "monto_compra"] = np.nan
    df.loc[np.random.choice(df.index, 4, replace=False), "resena_score"] = np.nan

    ruta_csv = os.path.join(RUTA, "clientes_comercioya.csv")
    df.to_csv(ruta_csv, index=False)
    print("✅ Dataset generado: clientes_comercioya.csv")
    return df


def ida_inicial(df):
    print("\n=== HEAD ===")
    print(df.head())

    print("\n=== INFO ===")
    print(df.info())

    print("\n=== NULOS ===")
    print(df.isnull().sum())

    print("\n=== TIPOS DE VARIABLES ===")
    print(df.dtypes)

    numericas = df.select_dtypes(include=np.number).columns.tolist()
    categoricas = df.select_dtypes(exclude=np.number).columns.tolist()

    print("\nVariables numéricas:", numericas)
    print("Variables categóricas:", categoricas)

    # limpieza básica
    df["monto_compra"] = df["monto_compra"].fillna(df["monto_compra"].median())
    df["resena_score"] = df["resena_score"].fillna(df["resena_score"].mode()[0])

    ruta_limpio = os.path.join(RUTA_RESULTADOS, "dataset_limpio.csv")
    df.to_csv(ruta_limpio, index=False)
    print("✅ Dataset limpio guardado: dataset_limpio.csv")

    return df, numericas, categoricas


# ==========================================
# LECCIÓN 2 - ESTADÍSTICA DESCRIPTIVA
# ==========================================
def estadistica_descriptiva(df):
    resumen = df.describe(include="all")
    resumen.to_csv(os.path.join(RUTA_RESULTADOS, "resumen_estadistico.csv"))
    print("✅ Resumen estadístico guardado")

    print("\n=== MEDIA ===")
    print(df[["edad", "visitas_web", "compras_realizadas", "monto_compra"]].mean())

    print("\n=== MEDIANA ===")
    print(df[["edad", "visitas_web", "compras_realizadas", "monto_compra"]].median())

    print("\n=== MODA ===")
    print(df[["categoria_favorita", "canal_origen", "cliente_frecuente"]].mode().iloc[0])

    print("\n=== VARIANZA ===")
    print(df[["edad", "visitas_web", "compras_realizadas", "monto_compra"]].var())

    print("\n=== DESVIACIÓN ESTÁNDAR ===")
    print(df[["edad", "visitas_web", "compras_realizadas", "monto_compra"]].std())

    print("\n=== CUARTILES ===")
    print(df[["edad", "visitas_web", "compras_realizadas", "monto_compra"]].quantile([0.25, 0.50, 0.75]))

    print("\n=== PERCENTILES ===")
    print(df["monto_compra"].quantile([0.10, 0.25, 0.50, 0.75, 0.90]))

    # Histograma
    plt.figure(figsize=(8, 5))
    sns.histplot(df["monto_compra"], kde=True)
    plt.title("Distribución del monto de compra")
    plt.xlabel("Monto de compra")
    plt.ylabel("Frecuencia")
    guardar_grafico("hist_monto_compra.png")
    plt.close()

    # Boxplot
    plt.figure(figsize=(8, 5))
    sns.boxplot(x=df["monto_compra"])
    plt.title("Boxplot del monto de compra")
    plt.xlabel("Monto de compra")
    guardar_grafico("boxplot_monto_compra.png")
    plt.close()

    # outliers por IQR
    q1 = df["monto_compra"].quantile(0.25)
    q3 = df["monto_compra"].quantile(0.75)
    iqr = q3 - q1
    limite_inf = q1 - 1.5 * iqr
    limite_sup = q3 + 1.5 * iqr

    outliers = df[(df["monto_compra"] < limite_inf) | (df["monto_compra"] > limite_sup)]
    print(f"\nCantidad de outliers en monto_compra: {len(outliers)}")

    return outliers


# ==========================================
# LECCIÓN 3 - CORRELACIÓN
# ==========================================
def correlacion(df):
    columnas_num = ["edad", "visitas_web", "compras_realizadas", "monto_compra", "devoluciones", "resena_score"]
    corr = df[columnas_num].corr()
    corr.to_csv(os.path.join(RUTA_RESULTADOS, "correlacion.csv"))
    print("✅ Correlación guardada")

    print("\n=== MATRIZ DE CORRELACIÓN ===")
    print(corr)

    pearson = df["visitas_web"].corr(df["monto_compra"], method="pearson")
    print(f"\nCoeficiente de Pearson entre visitas_web y monto_compra: {pearson:.4f}")

    # scatterplot
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="visitas_web", y="monto_compra", hue="cliente_frecuente")
    plt.title("Relación entre visitas web y monto de compra")
    guardar_grafico("scatter_visitas_monto.png")
    plt.close()

    # heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Mapa de calor de correlaciones")
    guardar_grafico("heatmap_correlacion.png")
    plt.close()

    return corr


# ==========================================
# LECCIÓN 4 - REGRESIONES
# ==========================================
def regresiones(df):
    # regresión simple
    X_simple = sm.add_constant(df["visitas_web"])
    y = df["monto_compra"]

    modelo_simple = sm.OLS(y, X_simple).fit()
    pred_simple = modelo_simple.predict(X_simple)

    r2_simple = modelo_simple.rsquared
    mse_simple = mean_squared_error(y, pred_simple)
    mae_simple = mean_absolute_error(y, pred_simple)

    print("\n=== REGRESIÓN SIMPLE ===")
    print(modelo_simple.summary())

    # regresión múltiple
    X_multiple = df[["visitas_web", "compras_realizadas", "edad", "devoluciones", "resena_score"]]
    X_multiple = sm.add_constant(X_multiple)

    modelo_multiple = sm.OLS(y, X_multiple).fit()
    pred_multiple = modelo_multiple.predict(X_multiple)

    r2_multiple = modelo_multiple.rsquared
    mse_multiple = mean_squared_error(y, pred_multiple)
    mae_multiple = mean_absolute_error(y, pred_multiple)

    print("\n=== REGRESIÓN MÚLTIPLE ===")
    print(modelo_multiple.summary())

    # guardar métricas
    with open(os.path.join(RUTA_RESULTADOS, "metricas_regresion.txt"), "w", encoding="utf-8") as f:
        f.write("REGRESIÓN SIMPLE\n")
        f.write(f"R²: {r2_simple:.4f}\n")
        f.write(f"MSE: {mse_simple:.2f}\n")
        f.write(f"MAE: {mae_simple:.2f}\n\n")

        f.write("REGRESIÓN MÚLTIPLE\n")
        f.write(f"R²: {r2_multiple:.4f}\n")
        f.write(f"MSE: {mse_multiple:.2f}\n")
        f.write(f"MAE: {mae_multiple:.2f}\n")

    # gráfico regresión
    plt.figure(figsize=(8, 5))
    sns.regplot(data=df, x="visitas_web", y="monto_compra", line_kws={"linewidth": 2})
    plt.title("Regresión lineal simple: visitas web vs monto de compra")
    guardar_grafico("regresion_simple.png")
    plt.close()

    return modelo_simple, modelo_multiple


# ==========================================
# LECCIÓN 5 - ANÁLISIS VISUAL CON SEABORN
# ==========================================
def visualizaciones_seaborn(df):
    columnas_pairplot = ["edad", "visitas_web", "compras_realizadas", "monto_compra", "resena_score", "cliente_frecuente"]
    g = sns.pairplot(df[columnas_pairplot], hue="cliente_frecuente")
    g.fig.suptitle("Pairplot general", y=1.02)
    g.savefig(os.path.join(RUTA_GRAFICOS, "pairplot_general.png"))
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.violinplot(data=df, x="categoria_favorita", y="monto_compra")
    plt.title("Distribución del monto de compra por categoría favorita")
    guardar_grafico("violinplot_monto_categoria.png")
    plt.close()

    g = sns.jointplot(data=df, x="visitas_web", y="compras_realizadas", kind="scatter")
    g.fig.suptitle("Jointplot: visitas web y compras realizadas", y=1.02)
    g.savefig(os.path.join(RUTA_GRAFICOS, "jointplot_visitas_compras.png"))
    plt.close()

    # FacetGrid
    g = sns.FacetGrid(df, col="cliente_frecuente", height=5)
    g.map_dataframe(sns.histplot, x="monto_compra")
    g.fig.suptitle("Distribución de monto de compra por tipo de cliente", y=1.05)
    g.savefig(os.path.join(RUTA_GRAFICOS, "facetgrid_clientes.png"))
    plt.close()


# ==========================================
# LECCIÓN 6 - MATPLOTLIB
# ==========================================
def visualizaciones_matplotlib(df):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    axes[0, 0].hist(df["edad"], bins=15)
    axes[0, 0].set_title("Distribución de edades")
    axes[0, 0].set_xlabel("Edad")
    axes[0, 0].set_ylabel("Frecuencia")

    axes[0, 1].scatter(df["visitas_web"], df["monto_compra"])
    axes[0, 1].set_title("Visitas web vs monto de compra")
    axes[0, 1].set_xlabel("Visitas web")
    axes[0, 1].set_ylabel("Monto de compra")

    axes[1, 0].boxplot(df["compras_realizadas"])
    axes[1, 0].set_title("Boxplot compras realizadas")

    conteo_categoria = df["categoria_favorita"].value_counts()
    axes[1, 1].bar(conteo_categoria.index, conteo_categoria.values)
    axes[1, 1].set_title("Clientes por categoría favorita")
    axes[1, 1].tick_params(axis="x", rotation=20)

    fig.suptitle("Resumen de visualizaciones con Matplotlib")
    plt.tight_layout()
    guardar_grafico("subplots_resumen.png")
    plt.close()

    # gráfico final personalizado
    plt.figure(figsize=(9, 5))
    plt.plot(
        df.groupby("resena_score")["monto_compra"].mean().index,
        df.groupby("resena_score")["monto_compra"].mean().values,
        marker="o"
    )
    plt.title("Monto promedio según reseña")
    plt.xlabel("Reseña")
    plt.ylabel("Monto promedio")
    plt.annotate("Tendencia general", xy=(3, df.groupby("resena_score")["monto_compra"].mean().iloc[2]))
    guardar_grafico("monto_promedio_resena.png")
    plt.close()


# ==========================================
# MAIN
# ==========================================
def main():
    df = generar_dataset()
    df, numericas, categoricas = ida_inicial(df)
    outliers = estadistica_descriptiva(df)
    corr = correlacion(df)
    modelo_simple, modelo_multiple = regresiones(df)
    visualizaciones_seaborn(df)
    visualizaciones_matplotlib(df)

    print("\n✅ Proyecto EDA completado correctamente.")
    print("Variables numéricas:", numericas)
    print("Variables categóricas:", categoricas)
    print("Outliers detectados:", len(outliers))


if __name__ == "__main__":
    main()