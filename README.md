# Analizador Léxico, Semántico y Sintáctico en Python para Ruby

Este proyecto es un **analizador completo** hecho en Python usando la librería [PLY](https://www.dabeaz.com/ply/) y PyQt5 para la interfaz gráfica.  
Se encarga de leer código Ruby y realizar análisis léxico, sintáctico y semántico completo con una interfaz moderna y amigable.

## 🧠 ¿Qué hace?

- **Análisis Léxico:** Extrae tokens del código Ruby (palabras clave, identificadores, operadores, números, cadenas, etc.)
- **Análisis Sintáctico:** Verifica la estructura gramatical del código
- **Análisis Semántico:** Valida tipos, métodos, variables y compatibilidad semántica
- **Interfaz Gráfica:** Permite analizar código de manera visual con resultados detallados
- **Gestión de Algoritmos:** Carga automáticamente algoritmos de prueba desde archivos
- **Análisis Asíncrono:** Procesamiento en hilos separados para mejor rendimiento

---

## 📦 Requisitos

### **Dependencias Python:**
```bash
# Instalar todas las dependencias necesarias
pip install ply PyQt5
```

### **Versiones específicas:**
- **Python:** 3.7 o superior
- **PLY:** 3.11 o superior (`pip install ply`)
- **PyQt5:** 5.15.0 o superior (`pip install PyQt5`)

### **Instalación completa:**
```bash
# Instalar dependencias
pip install -r requirements.txt
```

### **Crear requirements.txt:**
```txt
ply>=3.11
PyQt5>=5.15.0
```

---

## ▶️ ¿Cómo se usa?

### **1. Ejecutar la Interfaz Gráfica:**
```bash
python Interfaz.py
```

### **2. Opciones de Entrada:**
- **Escribir código:** Ingresa código Ruby directamente en el editor
- **Cargar algoritmos:** Usa el botón "🔬 ALGORITMOS" para cargar archivos desde `algorithms/`

### **3. Análisis:**
- Presiona "🚀 ANALIZAR" para ejecutar análisis completo
- Los resultados aparecen en tiempo real en las consolas de resultados y errores

### **4. Controles Disponibles:**
- **🚀 ANALIZAR:** Ejecuta análisis léxico, sintáctico y semántico
- **⏹️ DETENER:** Interrumpe análisis en progreso
- **🧹 LIMPIAR:** Limpia todas las áreas de texto
- **🔬 ALGORITMOS:** Carga algoritmos de prueba desde `algorithms/`

---

## 📝 Notas

- La interfaz gráfica requiere un entorno con soporte para ventanas (no funciona en terminales puras)
- Los archivos de algoritmos deben estar en formato UTF-8
- El análisis se ejecuta en hilos separados para mantener la interfaz responsiva
- Los errores se categorizan por tipo (léxico, sintáctico, semántico)

---

## 👨‍💻 Autores

**Jonathan Zambrano, Darwin Pacheco, Giovanni Sambonino** - Analizador Ruby con interfaz PyQt5

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para detalles.

