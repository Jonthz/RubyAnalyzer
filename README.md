# Analizador Léxico en Python para Ruby

Este proyecto es un **analizador léxico** hecho en Python usando la librería [PLY](https://www.dabeaz.com/ply/).  
Se encarga de leer código Ruby y detectar los tokens que lo componen: palabras clave, identificadores, operadores, números, cadenas, símbolos especiales y más.

> 🔧 Esta herramienta forma parte de un proyecto más grande para construir un compilador básico de Ruby. Por ahora, solo realiza el análisis léxico, pero en el futuro se agregarán análisis sintáctico, semántico y generación de código.

---

## 🧠 ¿Qué hace?

- Analiza fragmentos de código Ruby.
- Extrae una lista de tokens con su tipo y contenido.
- Permite ver cómo está formado el código desde el punto de vista léxico.
- Sirve como base para construir un parser o AST (Árbol de Sintaxis Abstracta) más adelante.

---

## 📦 Requisitos

- Python 3.x
- PLY (instalable con `pip install ply`)

---

## ▶️ ¿Cómo se usa?

1. Ejecuta el archivo principal desde la terminal:

```bash
python main.py
