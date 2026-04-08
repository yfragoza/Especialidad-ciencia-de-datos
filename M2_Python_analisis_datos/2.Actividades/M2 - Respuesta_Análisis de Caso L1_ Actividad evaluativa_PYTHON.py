# 1. Declaración de variables y año actual
nombre = "Carlos Pérez"
edad = 30
puesto = "Analista de Datos"
anio_actual = 2026 # Definido por la actividad [cite: 38]

# 2. Cálculo de jubilación (Aritmética básica)
# Restamos la edad actual a los 65 años para saber cuánto falta [cite: 40]
anios_restantes = 65 - edad 
# Sumamos esos años al año actual [cite: 42]
anio_jubilacion = anio_actual + anios_restantes

# 3. Mostrar información en consola [cite: 17, 42]
print("--- Registro de Empleado ---")
print("Nombre:", nombre)
print("Edad:", edad)
print("Puesto:", puesto)
print("Año estimado de jubilación:", anio_jubilacion)

print("Resumen:", nombre, "trabaja como", puesto, "y se jubilará en", anio_jubilacion)
print("----------------------------")

#5 (OPCIONAL): más empleados
# Empleado 2
nombre = "María"
edad = 40
puesto = "Gerente"

anios_restantes = 65 - edad
anio_jubilacion = anio_actual + anios_restantes

print("--- Registro de Empleado ---")
print("Nombre:", nombre)
print("Edad:", edad)
print("Puesto:", puesto)
print("Año estimado de jubilación:", anio_jubilacion)

print("Resumen:", nombre, "trabaja como", puesto, "y se jubilará en", anio_jubilacion)
print("----------------------------")
