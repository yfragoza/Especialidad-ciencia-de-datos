# 📘 Documentación Técnica

## 🧠 Descripción general

El sistema de gestión de contactos es una aplicación desarrollada en Python que permite registrar, editar, eliminar y buscar contactos mediante una interfaz de consola.

El objetivo es aplicar conceptos fundamentales de programación, estructuras de datos y programación orientada a objetos.

---

## 🏗️ Arquitectura del sistema

El sistema está dividido en tres módulos principales:

### 1. contacto.py
- Define la clase `Contacto`
- Contiene atributos como nombre, teléfono, correo y dirección
- Implementa encapsulación mediante atributos privados y métodos getter/setter

---

### 2. gestor_contactos.py
- Define la clase `GestorContactos`
- Maneja la lógica del sistema
- Permite:
  - Agregar contactos
  - Buscar contactos
  - Editar contactos
  - Eliminar contactos
  - Listar contactos

---

### 3. main.py
- Implementa la interfaz de usuario por consola
- Permite la interacción mediante un menú
- Gestiona la entrada de datos del usuario

---

### 4. test_contactos.py
- Contiene pruebas unitarias
- Permite validar el funcionamiento del sistema

---

## 🗂️ Estructuras de datos utilizadas

- **Listas**: almacenamiento de contactos
- **Diccionarios**: representación estructurada de datos (opcional con `to_dict()`)

---

## 🧩 Principios aplicados

- Programación orientada a objetos (POO)
- Encapsulación
- Separación de responsabilidades
- Código modular
- Reutilización de código

---

## ⚙️ Funcionamiento general

1. El usuario interactúa con el menú en `main.py`
2. Se envían solicitudes a `GestorContactos`
3. Se crean o modifican objetos `Contacto`
4. Se almacenan en una lista interna

---

## ⚠️ Limitaciones

- No persistencia de datos (no guarda en archivos o base de datos)
- Interfaz solo en consola
- Validaciones básicas

---

## 🚀 Posibles mejoras

- Guardar datos en archivo o base de datos
- Interfaz gráfica (Tkinter o web con Flask/Django)
- Validaciones más robustas
- Integración con API externa