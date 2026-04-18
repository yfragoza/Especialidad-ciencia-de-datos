import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score
from sklearn.covariance import EllipticEnvelope

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================
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


# =========================================================
# GENERAR DATASET
# =========================================================
def generar_dataset():
    n = 350

    edad = np.random.randint(18, 70, n)
    visitas_mes = np.random.randint(1, 60, n)
    tiempo_sitio = np.random.normal(12, 4, n).clip(2, 35)
    productos_vistos = np.random.randint(1, 45, n)
    clics_ofertas = np.random.randint(0, 18, n)
    historial_compras = np.random.randint(0, 25, n)
    descuento_promedio = np.random.uniform(0, 0.35, n)
    sexo = np.random.choice(["Femenino", "Masculino"], n)
    dispositivo = np.random.choice(["Móvil", "Desktop", "Tablet"], n, p=[0.55, 0.35, 0.10])
    region = np.random.choice(["Norte", "Centro", "Sur"], n)
    miembro_premium = np.random.choice(["Sí", "No"], n, p=[0.35, 0.65])

    monto_compra = (
        20
        + edad * 0.9
        + visitas_mes * 1.8
        + tiempo_sitio * 3.2
        + productos_vistos * 1.4
        + clics_ofertas * 2.5
        + historial_compras * 4.2
        + descuento_promedio * 180
        + np.where(miembro_premium == "Sí", 35, 0)
        + np.where(dispositivo == "Desktop", 12, 0)
        + np.random.normal(0, 18, n)
    )

    df = pd.DataFrame({
        "edad": edad,
        "visitas_mes": visitas_mes,
        "tiempo_sitio": tiempo_sitio.round(2),
        "productos_vistos": productos_vistos,
        "clics_ofertas": clics_ofertas,
        "historial_compras": historial_compras,
        "descuento_promedio": descuento_promedio.round(3),
        "sexo": sexo,
        "dispositivo": dispositivo,
        "region": region,
        "miembro_premium": miembro_premium,
        "monto_compra": monto_compra.round(2)
    })

    # introducir nulos
    idx_nulos_1 = np.random.choice(df.index, 10, replace=False)
    idx_nulos_2 = np.random.choice(df.index, 8, replace=False)
    df.loc[idx_nulos_1, "tiempo_sitio"] = np.nan
    df.loc[idx_nulos_2, "descuento_promedio"] = np.nan

    # introducir outliers
    idx_outliers = np.random.choice(df.index, 6, replace=False)
    df.loc[idx_outliers, "monto_compra"] *= 2.3

    ruta_csv = os.path.join(RUTA, "clientes_ecommerce_ml.csv")
    df.to_csv(ruta_csv, index=False)
    print("✅ Dataset generado: clientes_ecommerce_ml.csv")

    resumen = df.describe(include="all")
    resumen.to_csv(os.path.join(RUTA_RESULTADOS, "resumen_dataset.csv"))

    return df


# =========================================================
# LECCIÓN 1 - FUNDAMENTOS ML
# =========================================================
def leccion_1_fundamentos():
    print("\n" + "=" * 60)
    print("LECCIÓN 1 - FUNDAMENTOS DEL APRENDIZAJE DE MÁQUINA")
    print("=" * 60)

    print("Problema definido como: REGRESIÓN SUPERVISADA")
    print("Variable objetivo: monto_compra")
    print("Clasificación no es adecuada porque queremos predecir un valor numérico continuo.")


# =========================================================
# PREPROCESAMIENTO
# =========================================================
def preparar_datos(df):
    # tratamiento simple de outliers en target usando IQR
    q1 = df["monto_compra"].quantile(0.25)
    q3 = df["monto_compra"].quantile(0.75)
    iqr = q3 - q1
    li = q1 - 1.5 * iqr
    ls = q3 + 1.5 * iqr
    df["monto_compra"] = df["monto_compra"].clip(lower=li, upper=ls)

    X = df.drop(columns=["monto_compra"])
    y = df["monto_compra"]

    num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = X.select_dtypes(exclude=["int64", "float64"]).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]),
                num_cols
            ),
            (
                "cat",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore"))
                ]),
                cat_cols
            )
        ]
    )

    return X, y, preprocessor, num_cols, cat_cols


# =========================================================
# MÉTRICAS
# =========================================================
def calcular_metricas(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    return mae, mse, rmse, r2


def grafico_pred_real(y_true, y_pred, nombre, titulo):
    plt.figure(figsize=(7, 5))
    plt.scatter(y_true, y_pred, alpha=0.7)
    min_v = min(y_true.min(), y_pred.min())
    max_v = max(y_true.max(), y_pred.max())
    plt.plot([min_v, max_v], [min_v, max_v], linestyle="--")
    plt.xlabel("Valores reales")
    plt.ylabel("Predicciones")
    plt.title(titulo)
    guardar_grafico(nombre)
    plt.close()


# =========================================================
# LECCIÓN 2 - AJUSTE Y VALIDACIÓN CRUZADA
# =========================================================
def evaluar_cv(modelo, X_train, y_train, cv):
    scores = cross_val_score(modelo, X_train, y_train, cv=cv, scoring="r2")
    return scores.mean(), scores.std()


# =========================================================
# LECCIÓN 4 - REGRESIONES
# =========================================================
def entrenar_modelos(X_train, X_test, y_train, y_test, preprocessor):
    resultados = []

    modelos = {
        "Regresion_Lineal": LinearRegression(),
        "Ridge": Ridge(alpha=1.0),
        "Lasso": Lasso(alpha=0.05, max_iter=5000),
        "Gradient_Boosting": GradientBoostingRegressor(random_state=42)
    }

    # Regresión polinomial
    poly_pipeline = Pipeline([
        ("prep", preprocessor),
        ("poly", PolynomialFeatures(degree=2, include_bias=False)),
        ("model", LinearRegression())
    ])

    pipelines = {}

    for nombre, modelo in modelos.items():
        pipeline = Pipeline([
            ("prep", preprocessor),
            ("model", modelo)
        ])
        pipeline.fit(X_train, y_train)
        y_pred_train = pipeline.predict(X_train)
        y_pred_test = pipeline.predict(X_test)

        mae, mse, rmse, r2 = calcular_metricas(y_test, y_pred_test)
        mae_train, mse_train, rmse_train, r2_train = calcular_metricas(y_train, y_pred_train)

        resultados.append({
            "modelo": nombre,
            "MAE_train": mae_train,
            "RMSE_train": rmse_train,
            "R2_train": r2_train,
            "MAE_test": mae,
            "MSE_test": mse,
            "RMSE_test": rmse,
            "R2_test": r2
        })

        pipelines[nombre] = pipeline

    poly_pipeline.fit(X_train, y_train)
    y_pred_train = poly_pipeline.predict(X_train)
    y_pred_test = poly_pipeline.predict(X_test)

    mae, mse, rmse, r2 = calcular_metricas(y_test, y_pred_test)
    mae_train, mse_train, rmse_train, r2_train = calcular_metricas(y_train, y_pred_train)

    resultados.append({
        "modelo": "Regresion_Polinomial",
        "MAE_train": mae_train,
        "RMSE_train": rmse_train,
        "R2_train": r2_train,
        "MAE_test": mae,
        "MSE_test": mse,
        "RMSE_test": rmse,
        "R2_test": r2
    })
    pipelines["Regresion_Polinomial"] = poly_pipeline

    return pd.DataFrame(resultados), pipelines


# =========================================================
# LECCIÓN 5 - CLASIFICACIÓN
# =========================================================
def leccion_5_clasificacion(df):
    print("\n" + "=" * 60)
    print("LECCIÓN 5 - ALGORITMOS DE CLASIFICACIÓN")
    print("=" * 60)

    print("La clasificación no es el enfoque correcto porque el objetivo real es un valor continuo: monto_compra.")
    print("Se implementa un KNN solo como comparación conceptual.")

    df_clf = df.copy()
    df_clf["clase_gasto"] = pd.qcut(df_clf["monto_compra"], q=3, labels=["Bajo", "Medio", "Alto"])

    X = df_clf.drop(columns=["monto_compra", "clase_gasto"])
    y = df_clf["clase_gasto"]

    num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = X.select_dtypes(exclude=["int64", "float64"]).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]),
                num_cols
            ),
            (
                "cat",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore"))
                ]),
                cat_cols
            )
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    knn = Pipeline([
        ("prep", preprocessor),
        ("model", KNeighborsClassifier(n_neighbors=5))
    ])
    knn.fit(X_train, y_train)
    pred = knn.predict(X_test)
    acc = accuracy_score(y_test, pred)

    with open(os.path.join(RUTA_RESULTADOS, "cv_scores.txt"), "a", encoding="utf-8") as f:
        f.write("\n\nCOMPARACIÓN CON CLASIFICACIÓN\n")
        f.write(f"Accuracy KNN clasificador (solo referencia conceptual): {acc:.4f}\n")
        f.write("Conclusión: clasificación no es la formulación adecuada porque el objetivo del negocio es un monto numérico.\n")


# =========================================================
# LECCIÓN 7 - OPTIMIZACIÓN
# =========================================================
def optimizar_modelos(X_train, y_train, preprocessor):
    ridge_pipe = Pipeline([
        ("prep", preprocessor),
        ("model", Ridge())
    ])

    lasso_pipe = Pipeline([
        ("prep", preprocessor),
        ("model", Lasso(max_iter=5000))
    ])

    gb_pipe = Pipeline([
        ("prep", preprocessor),
        ("model", GradientBoostingRegressor(random_state=42))
    ])

    grid_ridge = GridSearchCV(
        ridge_pipe,
        param_grid={"model__alpha": [0.1, 1.0, 5.0, 10.0]},
        cv=5,
        scoring="r2"
    )
    grid_lasso = GridSearchCV(
        lasso_pipe,
        param_grid={"model__alpha": [0.001, 0.01, 0.05, 0.1]},
        cv=5,
        scoring="r2"
    )
    grid_gb = GridSearchCV(
        gb_pipe,
        param_grid={
            "model__n_estimators": [100, 150],
            "model__learning_rate": [0.05, 0.1],
            "model__max_depth": [2, 3]
        },
        cv=5,
        scoring="r2"
    )

    grid_ridge.fit(X_train, y_train)
    grid_lasso.fit(X_train, y_train)
    grid_gb.fit(X_train, y_train)

    return grid_ridge, grid_lasso, grid_gb


# =========================================================
# VISUALIZACIONES
# =========================================================
def graficos_generales(df, metricas_df):
    # target
    plt.figure(figsize=(7, 5))
    plt.hist(df["monto_compra"], bins=25, edgecolor="black")
    plt.title("Distribución del monto de compra")
    plt.xlabel("Monto de compra")
    plt.ylabel("Frecuencia")
    guardar_grafico("distribucion_target.png")
    plt.close()

    # correlación numéricas
    corr = df.select_dtypes(include=["int64", "float64"]).corr()
    plt.figure(figsize=(8, 6))
    plt.imshow(corr, aspect="auto")
    plt.colorbar()
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title("Correlación entre variables numéricas")
    guardar_grafico("correlacion_numericas.png")
    plt.close()

    # métricas
    plt.figure(figsize=(10, 5))
    plt.bar(metricas_df["modelo"], metricas_df["R2_test"])
    plt.xticks(rotation=30, ha="right")
    plt.title("Comparación de R² en test")
    plt.ylabel("R²")
    guardar_grafico("comparacion_metricas.png")
    plt.close()


# =========================================================
# MAIN
# =========================================================
def main():
    leccion_1_fundamentos()
    df = generar_dataset()

    X, y, preprocessor, num_cols, cat_cols = preparar_datos(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    cv = KFold(n_splits=5, shuffle=True, random_state=42)

    # modelos base
    metricas_df, pipelines = entrenar_modelos(X_train, X_test, y_train, y_test, preprocessor)

    # validación cruzada
    with open(os.path.join(RUTA_RESULTADOS, "cv_scores.txt"), "w", encoding="utf-8") as f:
        f.write("VALIDACIÓN CRUZADA Y AJUSTE\n\n")
        for nombre, pipe in pipelines.items():
            mean_cv, std_cv = evaluar_cv(pipe, X_train, y_train, cv)
            f.write(f"{nombre}: R2 CV mean={mean_cv:.4f}, std={std_cv:.4f}\n")

    # clasificación conceptual
    leccion_5_clasificacion(df)

    # optimización
    grid_ridge, grid_lasso, grid_gb = optimizar_modelos(X_train, y_train, preprocessor)

    modelos_opt = {
        "Ridge_Optimizado": grid_ridge.best_estimator_,
        "Lasso_Optimizado": grid_lasso.best_estimator_,
        "GB_Optimizado": grid_gb.best_estimator_
    }

    filas_opt = []
    for nombre, modelo in modelos_opt.items():
        modelo.fit(X_train, y_train)
        pred = modelo.predict(X_test)
        mae, mse, rmse, r2 = calcular_metricas(y_test, pred)
        filas_opt.append({
            "modelo": nombre,
            "MAE_train": np.nan,
            "RMSE_train": np.nan,
            "R2_train": np.nan,
            "MAE_test": mae,
            "MSE_test": mse,
            "RMSE_test": rmse,
            "R2_test": r2
        })

    metricas_opt_df = pd.DataFrame(filas_opt)
    metricas_final = pd.concat([metricas_df, metricas_opt_df], ignore_index=True)
    metricas_final.to_csv(os.path.join(RUTA_RESULTADOS, "metricas_modelos.csv"), index=False)

    # mejor modelo
    idx_best = metricas_final["R2_test"].idxmax()
    mejor_modelo_nombre = metricas_final.loc[idx_best, "modelo"]

    with open(os.path.join(RUTA_RESULTADOS, "mejor_modelo.txt"), "w", encoding="utf-8") as f:
        f.write("MODELO FINAL ELEGIDO\n\n")
        f.write(f"Mejor modelo según R2_test: {mejor_modelo_nombre}\n")
        f.write("Justificación: se elige el modelo con mejor desempeño predictivo y mayor robustez en validación.\n")
        f.write("\nMejores hiperparámetros:\n")
        f.write(f"Ridge: {grid_ridge.best_params_}\n")
        f.write(f"Lasso: {grid_lasso.best_params_}\n")
        f.write(f"Gradient Boosting: {grid_gb.best_params_}\n")

    # interpretación coeficientes lineales
    with open(os.path.join(RUTA_RESULTADOS, "interpretacion_coeficientes.txt"), "w", encoding="utf-8") as f:
        f.write("INTERPRETACIÓN CONCEPTUAL\n\n")
        f.write("En regresión lineal, los coeficientes indican el cambio esperado en el monto de compra ante variaciones en las variables explicativas, manteniendo el resto constante.\n")
        f.write("Las variables con efecto positivo aumentan el monto esperado y las de efecto negativo lo reducen.\n")
        f.write("El modelo polinomial mejora relaciones no lineales, mientras Ridge y Lasso ayudan a controlar complejidad.\n")

    # gráficos generales
    graficos_generales(df, metricas_final)

    # gráficos pred vs real
    for nombre, pipe in pipelines.items():
        pred = pipe.predict(X_test)
        archivo = {
            "Regresion_Lineal": "pred_vs_real_lineal.png",
            "Regresion_Polinomial": "pred_vs_real_polinomial.png",
            "Ridge": "pred_vs_real_ridge.png",
            "Lasso": "pred_vs_real_lasso.png",
            "Gradient_Boosting": "pred_vs_real_gb.png"
        }.get(nombre, None)
        if archivo:
            grafico_pred_real(y_test, pred, archivo, f"{nombre}: Predicción vs Real")

    # gráfico mejor modelo boosting optimizado
    best_gb = grid_gb.best_estimator_
    best_gb.fit(X_train, y_train)

    # importancia de variables del modelo boosting
    transformed_feature_names = []
    ohe = best_gb.named_steps["prep"].named_transformers_["cat"].named_steps["onehot"]
    cat_features = ohe.get_feature_names_out(cat_cols).tolist()
    transformed_feature_names = num_cols + cat_features

    importancias = best_gb.named_steps["model"].feature_importances_
    top_idx = np.argsort(importancias)[-10:]

    plt.figure(figsize=(10, 5))
    plt.barh(np.array(transformed_feature_names)[top_idx], importancias[top_idx])
    plt.title("Top variables importantes - Gradient Boosting")
    plt.xlabel("Importancia")
    guardar_grafico("feature_importance_gb.png")
    plt.close()

    print("\n✅ Proyecto M6 completado correctamente.")
    print("✅ Revisa resultados y gráficos exportados.")


if __name__ == "__main__":
    main()