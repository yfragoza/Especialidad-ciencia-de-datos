import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================
RUTA = os.path.dirname(__file__)
RUTA_GRAFICOS = os.path.join(RUTA, "graficos")
RUTA_RESULTADOS = os.path.join(RUTA, "resultados")

os.makedirs(RUTA_GRAFICOS, exist_ok=True)
os.makedirs(RUTA_RESULTADOS, exist_ok=True)

np.random.seed(42)


def guardar_grafico(nombre):
    ruta = os.path.join(RUTA_GRAFICOS, nombre)
    plt.savefig(ruta, bbox_inches="tight")
    print(f"✅ Gráfico guardado: {nombre}")


# =====================================================
# LECCIÓN 1 - MÉTODO CIENTÍFICO Y ESTADÍSTICA
# =====================================================
def leccion_1_metodo_cientifico():
    print("\n" + "=" * 60)
    print("LECCIÓN 1 - MÉTODO CIENTÍFICO Y ESTADÍSTICA")
    print("=" * 60)

    problema = (
        "Analizar los factores que influyen en los hábitos saludables "
        "de jóvenes universitarios, especialmente sueño, alimentación y actividad física."
    )

    hipotesis_nula = (
        "H0: El promedio de horas de sueño de los estudiantes universitarios "
        "es igual a 7 horas por noche."
    )

    hipotesis_alternativa = (
        "H1: El promedio de horas de sueño de los estudiantes universitarios "
        "es distinto de 7 horas por noche."
    )

    variables = {
        "horas_sueno": "Cuantitativa continua",
        "actividad_fisica_dias": "Cuantitativa discreta",
        "porciones_frutas_verduras": "Cuantitativa discreta",
        "comida_rapida_dias": "Cuantitativa discreta",
        "nivel_estres": "Cuantitativa discreta",
        "desayuna_diario": "Cualitativa dicotómica",
        "sexo": "Cualitativa nominal"
    }

    print("Problema:", problema)
    print("Hipótesis nula:", hipotesis_nula)
    print("Hipótesis alternativa:", hipotesis_alternativa)
    print("\nVariables:")
    for k, v in variables.items():
        print(f"- {k}: {v}")

    return problema, hipotesis_nula, hipotesis_alternativa, variables


# =====================================================
# LECCIÓN 2 - PROBABILIDAD Y ESTADÍSTICA
# =====================================================
def generar_dataset():
    print("\n" + "=" * 60)
    print("LECCIÓN 2 - PROBABILIDAD Y ESTADÍSTICA")
    print("=" * 60)

    n = 150

    df = pd.DataFrame({
        "id_estudiante": np.arange(1, n + 1),
        "sexo": np.random.choice(["Femenino", "Masculino"], n),
        "horas_sueno": np.random.normal(loc=6.8, scale=1.1, size=n).round(2),
        "actividad_fisica_dias": np.random.binomial(n=7, p=0.45, size=n),
        "porciones_frutas_verduras": np.random.poisson(lam=3, size=n),
        "comida_rapida_dias": np.random.poisson(lam=2, size=n),
        "nivel_estres": np.random.randint(1, 11, n),
        "desayuna_diario": np.random.choice(["Sí", "No"], n, p=[0.58, 0.42])
    })

    # Ajustes de realismo
    df["horas_sueno"] = df["horas_sueno"].clip(lower=3.5, upper=10)
    df["porciones_frutas_verduras"] = df["porciones_frutas_verduras"].clip(lower=0)
    df["comida_rapida_dias"] = df["comida_rapida_dias"].clip(lower=0, upper=7)

    ruta_csv = os.path.join(RUTA, "dataset_habitos_saludables.csv")
    df.to_csv(ruta_csv, index=False)
    print("✅ Dataset generado: dataset_habitos_saludables.csv")

    # Tipo de muestreo
    tipo_muestreo = (
        "Muestreo aleatorio simple simulado. "
        "Cada estudiante tiene la misma probabilidad de ser seleccionado."
    )

    # Probabilidades básicas
    evento_a = (df["desayuna_diario"] == "Sí")
    evento_b = (df["actividad_fisica_dias"] >= 4)

    p_a = evento_a.mean()
    p_b = evento_b.mean()
    p_interseccion = (evento_a & evento_b).mean()
    p_union = p_a + p_b - p_interseccion
    p_complementario = 1 - p_a

    with open(os.path.join(RUTA_RESULTADOS, "probabilidades.txt"), "w", encoding="utf-8") as f:
        f.write("PROBABILIDADES BÁSICAS\n")
        f.write(f"P(A): desayuna diario = {p_a:.4f}\n")
        f.write(f"P(B): actividad física >= 4 días = {p_b:.4f}\n")
        f.write(f"P(A ∩ B) = {p_interseccion:.4f}\n")
        f.write(f"P(A ∪ B) = {p_union:.4f}\n")
        f.write(f"P(A complemento) = {p_complementario:.4f}\n")
        f.write("\nTipo de muestreo aplicado:\n")
        f.write(tipo_muestreo)

    print("✅ Archivo de probabilidades guardado")

    return df


# =====================================================
# LECCIÓN 3 - DISTRIBUCIONES DE PROBABILIDAD
# =====================================================
def leccion_3_distribuciones(df):
    print("\n" + "=" * 60)
    print("LECCIÓN 3 - DISTRIBUCIONES DE PROBABILIDAD")
    print("=" * 60)

    # Normal para horas de sueño
    media_sueno = df["horas_sueno"].mean()
    std_sueno = df["horas_sueno"].std()

    # Binomial: desayuna diario
    p_desayuna = (df["desayuna_diario"] == "Sí").mean()

    # Poisson: comida rápida
    lambda_comida = df["comida_rapida_dias"].mean()

    print(f"Media horas_sueno: {media_sueno:.2f}")
    print(f"Desviación horas_sueno: {std_sueno:.2f}")
    print(f"p desayuna diario: {p_desayuna:.4f}")
    print(f"Lambda comida rápida: {lambda_comida:.2f}")

    # Probabilidades
    prob_sueno_mas_8 = 1 - stats.norm.cdf(8, loc=media_sueno, scale=std_sueno)
    prob_desayunan_4_de_5 = stats.binom.pmf(4, 5, p_desayuna)
    prob_comida_rapida_3 = stats.poisson.pmf(3, lambda_comida)

    with open(os.path.join(RUTA_RESULTADOS, "probabilidades.txt"), "a", encoding="utf-8") as f:
        f.write("\n\nDISTRIBUCIONES DE PROBABILIDAD\n")
        f.write(f"P(horas_sueno > 8) ~ Normal = {prob_sueno_mas_8:.4f}\n")
        f.write(f"P(4 de 5 desayunan diario) ~ Binomial = {prob_desayunan_4_de_5:.4f}\n")
        f.write(f"P(comida_rapida_dias = 3) ~ Poisson = {prob_comida_rapida_3:.4f}\n")

    # Gráfico normal aproximado
    x = np.linspace(media_sueno - 4*std_sueno, media_sueno + 4*std_sueno, 300)
    y = stats.norm.pdf(x, media_sueno, std_sueno)

    plt.figure(figsize=(8, 5))
    plt.plot(x, y)
    plt.title("Distribución normal aproximada de horas de sueño")
    plt.xlabel("Horas de sueño")
    plt.ylabel("Densidad")
    guardar_grafico("distribucion_horas_sueno.png")
    plt.close()

    # Binomial
    x_bin = np.arange(0, 6)
    y_bin = stats.binom.pmf(x_bin, 5, p_desayuna)

    plt.figure(figsize=(8, 5))
    plt.bar(x_bin, y_bin)
    plt.title("Distribución binomial: estudiantes que desayunan diario (n=5)")
    plt.xlabel("Cantidad que desayuna")
    plt.ylabel("Probabilidad")
    guardar_grafico("distribucion_binomial_desayuno.png")
    plt.close()

    # Poisson
    x_pois = np.arange(0, 8)
    y_pois = stats.poisson.pmf(x_pois, lambda_comida)

    plt.figure(figsize=(8, 5))
    plt.bar(x_pois, y_pois)
    plt.title("Distribución Poisson: días de comida rápida")
    plt.xlabel("Días por semana")
    plt.ylabel("Probabilidad")
    guardar_grafico("distribucion_poisson_comida_rapida.png")
    plt.close()


# =====================================================
# LECCIÓN 4 - DISTRIBUCIÓN MUESTRAL Y TLC
# =====================================================
def leccion_4_tlc(df):
    print("\n" + "=" * 60)
    print("LECCIÓN 4 - DISTRIBUCIÓN MUESTRAL Y TLC")
    print("=" * 60)

    variable = df["horas_sueno"].values
    tamanos = [5, 30, 50]
    muestras_por_tamano = 1000

    medias_muestrales = {}

    for n in tamanos:
        medias = []
        for _ in range(muestras_por_tamano):
            muestra = np.random.choice(variable, size=n, replace=True)
            medias.append(np.mean(muestra))
        medias_muestrales[n] = medias

    # Histograma de medias muestrales n=30
    plt.figure(figsize=(8, 5))
    plt.hist(medias_muestrales[30], bins=25, edgecolor="black")
    plt.title("Distribución muestral de la media (n=30)")
    plt.xlabel("Media muestral de horas de sueño")
    plt.ylabel("Frecuencia")
    guardar_grafico("tlc_horas_sueno.png")
    plt.close()

    # Comparación población vs muestral
    plt.figure(figsize=(10, 5))
    plt.hist(variable, bins=25, alpha=0.6, label="Población simulada")
    plt.hist(medias_muestrales[30], bins=25, alpha=0.6, label="Medias muestrales n=30")
    plt.title("Comparación entre distribución poblacional y distribución muestral")
    plt.xlabel("Horas de sueño")
    plt.ylabel("Frecuencia")
    plt.legend()
    guardar_grafico("comparacion_poblacion_muestral.png")
    plt.close()

    with open(os.path.join(RUTA_RESULTADOS, "probabilidades.txt"), "a", encoding="utf-8") as f:
        f.write("\n\nTEOREMA DEL LÍMITE CENTRAL\n")
        for n in tamanos:
            f.write(
                f"n={n}: media de medias={np.mean(medias_muestrales[n]):.4f}, "
                f"desviación={np.std(medias_muestrales[n]):.4f}\n"
            )

    print("✅ Análisis TLC completado")


# =====================================================
# LECCIÓN 5 - INTERVALOS DE CONFIANZA
# =====================================================
def intervalo_confianza_media(data, confianza):
    n = len(data)
    media = np.mean(data)
    s = np.std(data, ddof=1)
    error = stats.t.ppf((1 + confianza) / 2, df=n - 1) * (s / np.sqrt(n))
    return media - error, media + error


def leccion_5_intervalos(df):
    print("\n" + "=" * 60)
    print("LECCIÓN 5 - INFERENCIA E INTERVALOS DE CONFIANZA")
    print("=" * 60)

    variables = ["horas_sueno", "actividad_fisica_dias"]
    niveles = [0.90, 0.95, 0.99]

    with open(os.path.join(RUTA_RESULTADOS, "intervalos_confianza.txt"), "w", encoding="utf-8") as f:
        f.write("INTERVALOS DE CONFIANZA PARA LA MEDIA\n\n")

        for var in variables:
            f.write(f"Variable: {var}\n")
            datos = df[var].values
            for confianza in niveles:
                li, ls = intervalo_confianza_media(datos, confianza)
                ancho = ls - li
                f.write(
                    f"Nivel {int(confianza*100)}%: ({li:.4f}, {ls:.4f}) | "
                    f"ancho={ancho:.4f}\n"
                )
            f.write("\n")

        # Impacto del tamaño muestral
        datos_sueno = df["horas_sueno"].values
        for n in [20, 50, 100]:
            muestra = np.random.choice(datos_sueno, size=n, replace=True)
            li, ls = intervalo_confianza_media(muestra, 0.95)
            f.write(
                f"Tamaño muestral {n} para horas_sueno al 95%: "
                f"({li:.4f}, {ls:.4f}) | ancho={ls-li:.4f}\n"
            )

    print("✅ Intervalos de confianza guardados")


# =====================================================
# LECCIÓN 6 - TEST DE SIGNIFICANCIA
# =====================================================
def leccion_6_test_hipotesis(df):
    print("\n" + "=" * 60)
    print("LECCIÓN 6 - TEST DE SIGNIFICANCIA")
    print("=" * 60)

    # H0: mu = 7 horas
    datos = df["horas_sueno"].values
    mu0 = 7
    alpha = 0.05

    t_stat, p_valor = stats.ttest_1samp(datos, popmean=mu0)

    decision = "Rechazar H0" if p_valor < alpha else "No rechazar H0"

    with open(os.path.join(RUTA_RESULTADOS, "prueba_hipotesis.txt"), "w", encoding="utf-8") as f:
        f.write("PRUEBA DE HIPÓTESIS PARA LA MEDIA DE HORAS DE SUEÑO\n\n")
        f.write(f"H0: mu = {mu0}\n")
        f.write(f"H1: mu != {mu0}\n")
        f.write(f"Estadístico t = {t_stat:.4f}\n")
        f.write(f"Valor-p = {p_valor:.6f}\n")
        f.write(f"Nivel de significancia alpha = {alpha}\n")
        f.write(f"Decisión: {decision}\n\n")
        f.write("Error tipo I: rechazar H0 siendo verdadera.\n")
        f.write("Error tipo II: no rechazar H0 siendo falsa.\n")

    print(f"t = {t_stat:.4f}")
    print(f"p = {p_valor:.6f}")
    print(f"Decisión: {decision}")


# =====================================================
# RESULTADOS AUXILIARES
# =====================================================
def guardar_resumen_y_diccionario(df):
    resumen = df.describe(include="all")
    resumen.to_csv(os.path.join(RUTA_RESULTADOS, "resumen_estadistico.csv"))

    with open(os.path.join(RUTA_RESULTADOS, "diccionario_variables.txt"), "w", encoding="utf-8") as f:
        f.write("DICCIONARIO DE VARIABLES\n\n")
        f.write("id_estudiante: identificador único del estudiante\n")
        f.write("sexo: sexo del estudiante\n")
        f.write("horas_sueno: promedio de horas dormidas por noche\n")
        f.write("actividad_fisica_dias: cantidad de días con actividad física por semana\n")
        f.write("porciones_frutas_verduras: porciones consumidas por día\n")
        f.write("comida_rapida_dias: cantidad de días por semana que consume comida rápida\n")
        f.write("nivel_estres: nivel de estrés percibido de 1 a 10\n")
        f.write("desayuna_diario: indica si desayuna diariamente\n")

    # gráfico actividad física
    plt.figure(figsize=(8, 5))
    plt.hist(df["actividad_fisica_dias"], bins=np.arange(-0.5, 8.5, 1), edgecolor="black")
    plt.title("Distribución de actividad física por semana")
    plt.xlabel("Días por semana")
    plt.ylabel("Frecuencia")
    guardar_grafico("distribucion_actividad_fisica.png")
    plt.close()


# =====================================================
# MAIN
# =====================================================
def main():
    leccion_1_metodo_cientifico()
    df = generar_dataset()
    guardar_resumen_y_diccionario(df)
    leccion_3_distribuciones(df)
    leccion_4_tlc(df)
    leccion_5_intervalos(df)
    leccion_6_test_hipotesis(df)

    print("\n✅ Proyecto M5 completado correctamente.")


if __name__ == "__main__":
    main()