# 🧪 Informe de Pruebas

## 🎯 Objetivo
Validar que las funcionalidades principales del sistema operen correctamente.

## 🛠️ Herramienta utilizada
- unittest (librería estándar de Python)

## Pruebas realizadas

### 1. Agregar contacto
- Entrada: contacto nuevo con teléfono único
- Resultado esperado: contacto agregado
- Resultado obtenido: exitoso

### 2. Evitar teléfono duplicado
- Entrada: contacto con teléfono ya registrado
- Resultado esperado: no se agrega
- Resultado obtenido: exitoso

### 3. Buscar por nombre
- Entrada: "Ana"
- Resultado esperado: retorna contacto de Ana Pérez
- Resultado obtenido: exitoso

### 4. Buscar por teléfono
- Entrada: "123456789"
- Resultado esperado: retorna contacto encontrado
- Resultado obtenido: exitoso

### 5. Editar contacto
- Entrada: cambiar nombre de un contacto existente
- Resultado esperado: contacto actualizado
- Resultado obtenido: exitoso

### 6. Eliminar contacto
- Entrada: teléfono de un contacto existente
- Resultado esperado: contacto eliminado
- Resultado obtenido: exitoso


## ▶️ Ejecución de pruebas
- python -m unittest test_contactos.py


## Conclusión
Las funcionalidades principales fueron probadas correctamente mediante pruebas unitarias y se verificó el comportamiento esperado del sistema.