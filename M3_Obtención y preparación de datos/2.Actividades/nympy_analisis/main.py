import numpy as np

# ===============================
# 1. CARGA Y ESTRUCTURACIÓN
# ===============================

# Simulación de datos financieros (5 acciones x 5 días)
datos = np.random.randint(100, 500, size=(5, 5))

print("📊 Datos financieros:")
print(datos)

# ===============================
# 2. ANÁLISIS DE DATOS
# ===============================

# Promedio, máximo y mínimo por acción (filas)
promedios = np.mean(datos, axis=1)
maximos = np.max(datos, axis=1)
minimos = np.min(datos, axis=1)

print("\n📈 Promedio por acción:", promedios)
print("📈 Máximo por acción:", maximos)
print("📈 Mínimo por acción:", minimos)

# Variación porcentual diaria
variacion = np.diff(datos, axis=1) / datos[:, :-1] * 100

print("\n📊 Variación porcentual diaria:")
print(variacion)

# ===============================
# 3. FUNCIONES MATEMÁTICAS
# ===============================

logaritmo = np.log(datos)
exponencial = np.exp(datos / 100)
normalizado = (datos - np.mean(datos)) / np.std(datos)

print("\n🔢 Logaritmo de los datos:")
print(logaritmo)

print("\n🔢 Exponencial de los datos:")
print(exponencial)

print("\n📉 Datos normalizados:")
print(normalizado)

# ===============================
# 4. INDEXACIÓN Y SELECCIÓN
# ===============================

# Rendimiento de una acción específica (fila 0, día 2)
valor_especifico = datos[0, 2]
print("\n🎯  Rendimiento de la acción 1 en el día 3:", valor_especifico)

# Selección condicional (valores mayores a 300)
mayores_300 = datos[datos > 300]
print("\n📊 Valores mayores a 300:")
print(mayores_300)

rendimientos_especificos = datos[[0, 2, 4], [1, 3, 0]]
print("\n📌 Selección avanzada de elementos:")
print(rendimientos_especificos)

# ===============================
# 5. BROADCASTING
# ===============================

# Normalización simple
ajuste = np.array([1, 2, 3, 4, 5])
datos_ajustados = datos + ajuste
print("\n⚡ Datos ajustados con broadcasting:")
print(datos_ajustados)