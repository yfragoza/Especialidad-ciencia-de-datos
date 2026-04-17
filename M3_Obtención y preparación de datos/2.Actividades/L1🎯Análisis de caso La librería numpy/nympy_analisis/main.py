import numpy as np

# ===============================
# 1. CARGA Y ESTRUCTURACIÓN
# ===============================

# Simulación de datos financieros (5 acciones x 5 días)
datos = np.random.randint(100, 500, size=(5, 5))

print("📊 Datos financieros:")
print(datos)

print("\n📐 Forma de la matriz:", datos.shape)

# ===============================
# 2. ANÁLISIS DE DATOS
# ===============================

# Promedio, máximo y mínimo por acción (filas)
promedios = np.mean(datos, axis=1)
maximos = np.max(datos, axis=1)
minimos = np.min(datos, axis=1)

print("\n📈 Promedios:", promedios)
print("📈 Máximos:", maximos)
print("📈 Mínimos:", minimos)

# Variación porcentual diaria
variacion = np.diff(datos) / datos[:, :-1] * 100

print("\n📊 Variación porcentual diaria:")
print(variacion)

# ===============================
# 3. FUNCIONES MATEMÁTICAS
# ===============================

logaritmo = np.log(datos)
exponencial = np.exp(datos / 100)

print("\n🔢 Logaritmo:")
print(logaritmo)

print("\n🔢 Exponencial:")
print(exponencial)

# ===============================
# 4. INDEXACIÓN Y SELECCIÓN
# ===============================

# Rendimiento de una acción específica (fila 0, día 2)
valor = datos[0, 2]
print("\n🎯 Valor específico:", valor)

# Selección condicional (valores mayores a 300)
mayores = datos[datos > 300]
print("\n📊 Valores mayores a 300:")
print(mayores)

# ===============================
# 5. BROADCASTING
# ===============================

# Normalización simple
normalizado = (datos - np.mean(datos)) / np.std(datos)

print("\n📉 Datos normalizados:")
print(normalizado)