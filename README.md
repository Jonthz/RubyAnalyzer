# Analizador Léxico, Semántico y Sintáctico en Python para Ruby

> Por el momento solo esta implementado el analizador léxico, en las siguientes semanas se irá implementando el resto del analizador, y también la GUI.

Este proyecto es un **analizador léxico** hecho en Python usando la librería [PLY](https://www.dabeaz.com/ply/).  
Se encarga de leer código Ruby y detectar los tokens que lo componen: palabras clave, identificadores, operadores, números, cadenas, símbolos especiales y más.

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
```

2. Escoje entre probar un código propio, o uno de los algoritmos ya hechos:

>1. Ingresar código Ruby manualmente
>2. Usar algoritmo de prueba Insertion Sort.
>3. Usar algoritmo de prueba Quick Sort
>4. Usar algoritmo de prueba Class
>5. Salir

3. Observa los resultados por consola o en los logs generados automaticamentes en la carpeta `logs`.

## 📝 Notas

Revisar el archivo `ContribucionesLexico` para tener más detalle de que realizo cada integrante. En el código del analizador también se encuentra señalado en comentarios la parte de cada uno.