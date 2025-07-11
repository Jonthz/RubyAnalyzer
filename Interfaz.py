import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QGridLayout
from PyQt5.QtCore import Qt

# ===== IMPORTAR TUS ANALIZADORES (SIN VARIABLES GLOBALES) =====
# SOLO importar las funciones, NO las listas de errores aquí
from AnalizadorLexico import test_lexical_analyzer
from AnalizadorSintacticoCopy import test_parser  
from AnalizadorSemantico import analizar_codigo

class RubyExpressionValidator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the window
        self.setWindowTitle('Ruby Espression Validator')
        self.setGeometry(100, 100, 1200, 700)
        
        # Apply custom styles using QSS (similar to CSS)
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                background-color: #f5f5f5;
                color: #333333;
            }

            QLabel {
                font-size: 14px;
                color: #2c3e50;
                font-weight: bold;
                margin: 5px 0px;
            }

            QTextEdit {
                background-color: #ffffff;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                padding: 12px;
                line-height: 1.4;
            }

            QTextEdit:focus {
                border: 2px solid #3498db;
            }

            QPushButton {
                font-size: 14px;
                font-weight: bold;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                margin: 4px;
                min-width: 120px;
                min-height: 40px;
            }

            QPushButton#run_button {
                background-color: #3498db;
                color: white;
            }

            QPushButton#run_button:hover {
                background-color: #2980b9;
            }

            QPushButton#run_button:pressed {
                background-color: #1f618d;
            }

            QPushButton#clear_button {
                background-color: #e67e22;
                color: white;
            }

            QPushButton#clear_button:hover {
                background-color: #d35400;
            }

            QPushButton#clear_button:pressed {
                background-color: #a0522d;
            }

            QPushButton#load_button {
                background-color: #27ae60;
                color: white;
            }

            QPushButton#load_button:hover {
                background-color: #229954;
            }

            #title_label {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
                margin-left: 15px;
            }

            #text_expression_label {
                font-size: 16px;
                color: #34495e;
                margin-bottom: 8px;
            }

            #result_label, #errors_label {
                font-size: 16px;
                color: #34495e;
                margin-bottom: 8px;
            }

            #result_console {
                background-color: #1e1e1e;
                color: #00ff00;
                border: 2px solid #34495e;
                font-family: 'Consolas', 'Monaco', monospace;
            }

            #errors_console {
                background-color: #1e1e1e;
                color: #ff6b6b;
                border: 2px solid #34495e;
                font-family: 'Consolas', 'Monaco', monospace;
            }
        """)

        # Main layout for the window
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # Header layout with logo and title
        header_layout = QHBoxLayout()
        
        # Ruby Logo placeholder
        self.image_label = QLabel(self)
        self.image_label.setText("RUBY")
        self.image_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #e74c3c; margin-right: 15px;")
        
        # Title label
        self.title_label = QLabel('RUBY ANALYZER\nJonathan Zambrano', self)
        self.title_label.setObjectName("title_label")
        
        header_layout.addWidget(self.image_label)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()  # Push everything to the left
        
        # Buttons layout in header
        buttons_layout = QHBoxLayout()
        
        # ===== BOTONES PROFESIONALES =====
        self.run_button = QPushButton('ANALIZAR', self)
        self.run_button.setObjectName("run_button")
        
        self.clear_button = QPushButton('LIMPIAR', self)
        self.clear_button.setObjectName("clear_button")
        
        self.load_button = QPushButton('CARGAR EJEMPLO', self)
        self.load_button.setObjectName("load_button")
        
        # ===== CONECTAR EVENTOS =====
        self.run_button.clicked.connect(self.analyze_ruby_code)
        self.clear_button.clicked.connect(self.clear_input)
        self.load_button.clicked.connect(self.load_sample_code)
        
        buttons_layout.addWidget(self.run_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.load_button)
        
        header_layout.addLayout(buttons_layout)
        
        # Add header to main layout
        main_layout.addLayout(header_layout)

        # Content layout
        content_layout = QHBoxLayout()
        content_layout.setSpacing(25)

        # Left column: Text Expression area
        left_column_layout = QVBoxLayout()
        
        self.text_expression_label = QLabel('Código Ruby', self)
        self.text_expression_label.setObjectName("text_expression_label")
        
        self.text_area = QTextEdit(self)
        self.text_area.setPlaceholderText('# Escriba su código Ruby aquí...\n# Ejemplo:\nclass Calculator\n  def add(x, y)\n    x + y\n  end\nend\n\ncalc = Calculator.new\nresult = calc.add(5, 3)\nputs result')
        self.text_area.setMinimumHeight(450)
        
        left_column_layout.addWidget(self.text_expression_label)
        left_column_layout.addWidget(self.text_area)

        # Right column: Result and Errors sections
        right_column_layout = QVBoxLayout()

        # Result section
        self.result_label = QLabel('Resultados del Análisis', self)
        self.result_label.setObjectName("result_label")
        
        self.result_console = QTextEdit(self)
        self.result_console.setObjectName("result_console")
        self.result_console.setReadOnly(True)
        self.result_console.setPlaceholderText('Los resultados del análisis aparecerán aquí...')
        self.result_console.setMaximumHeight(320)

        # Errors section
        self.errors_label = QLabel('Errores y Advertencias', self)
        self.errors_label.setObjectName("errors_label")
        
        self.errors_console = QTextEdit(self)
        self.errors_console.setObjectName("errors_console")
        self.errors_console.setReadOnly(True)
        self.errors_console.setPlaceholderText('Los errores aparecerán aquí...')
        self.errors_console.setMaximumHeight(320)

        right_column_layout.addWidget(self.result_label)
        right_column_layout.addWidget(self.result_console)
        right_column_layout.addWidget(self.errors_label)
        right_column_layout.addWidget(self.errors_console)

        # Add columns to content layout
        content_layout.addLayout(left_column_layout, 2)  # Give more space to left column
        content_layout.addLayout(right_column_layout, 1)

        # Add content layout to main layout
        main_layout.addLayout(content_layout)

        # Set the main layout for the window
        self.setLayout(main_layout)

    def analyze_ruby_code(self):
        """
        Función principal para analizar código Ruby
        Ejecuta: Léxico → Sintáctico → Semántico
        """
        code = self.text_area.toPlainText().strip()
        
        if not code:
            self.errors_console.setPlainText("ERROR: No hay código para analizar")
            return
        
        # Limpiar consolas
        self.result_console.clear()
        self.errors_console.clear()
        
        # Mostrar inicio del análisis
        self.result_console.setPlainText("INICIANDO ANÁLISIS COMPLETO...\n" + "="*60)
        
        try:
            # ===== IMPORTS CON MANEJO DE ERRORES =====
            from AnalizadorLexico import test_lexical_analyzer
            from AnalizadorSintacticoCopy import test_parser
            from AnalizadorSemantico import analizar_codigo
            
            # ===== IMPORTAR VARIABLES CON MANEJO DE ERRORES =====
            try:
                from AnalizadorLexico import error_tokens
            except ImportError:
                error_tokens = []
                print("WARNING: error_tokens no disponible en AnalizadorLexico")
            
            try:
                from AnalizadorSemantico import semantic_errors, semantic_warnings
            except ImportError:
                semantic_errors = []
                semantic_warnings = []
                print("WARNING: semantic_errors/warnings no disponibles en AnalizadorSemantico")
            
            # ===== LIMPIAR ERRORES SI EXISTEN =====
            if hasattr(error_tokens, 'clear'):
                error_tokens.clear()
            
            if hasattr(semantic_errors, 'clear'):
                semantic_errors.clear()
                
            if hasattr(semantic_warnings, 'clear'):
                semantic_warnings.clear()
            
            # ===== CAPTURAR SALIDAS DE TODOS LOS ANALIZADORES =====
            results = []
            all_errors = []
            
            # Buffer para capturar prints
            output_buffer = io.StringIO()
            
            with redirect_stdout(output_buffer):
                # ===== 1. ANÁLISIS LÉXICO =====
                results.append("\n[1] ANÁLISIS LÉXICO")
                results.append("-" * 25)
                
                try:
                    # Ejecutar análisis léxico
                    tokens, error_tokens = test_lexical_analyzer(code)
                    results.append("Tokens reconocidos:")
                    results.extend(tokens)
                    results.append("STATUS: Completado exitosamente")
                except Exception as e:
                    all_errors.append(f"LÉXICO: Error durante análisis - {str(e)}")
                    all_errors.append(e)
                
                # ===== 2. ANÁLISIS SINTÁCTICO =====
                results.append("\n[2] ANÁLISIS SINTÁCTICO")
                results.append("-" * 28)
                
                try:
                    result, syntax_errors =  test_parser(code)
                    results.append("Estructura sintáctica:")
                    results.extend(result)
                    results.append("STATUS: Completado exitosamente")
                except Exception as e:
                    all_errors.append(f"SINTÁCTICO: {str(e)}")
                
                # ===== 3. ANÁLISIS SEMÁNTICO =====
                results.append("\n[3] ANÁLISIS SEMÁNTICO")
                results.append("-" * 26)
                
                try:
                    # Ejecutar análisis semántico
                    semantic_errors, semantic_warnings, symbol_table, defined_methods = analizar_codigo(code)
                    results.append("STATUS: Completado exitosamente")
                    results.append("Tabla de símbolos:")
                    results.append(str(symbol_table))
                    results.append("Métodos definidos:")
                    results.append(str(defined_methods))
                except Exception as e:
                    all_errors.append(f"SEMÁNTICO: Error durante análisis - {str(e)}")
            
            # ===== CAPTURAR ERRORES DESPUÉS DEL ANÁLISIS =====
            
            # Capturar errores léxicos
            if error_tokens and len(error_tokens) > 0:
                for error in error_tokens:
                    all_errors.append(f"LÉXICO: {error}")
                    print(f"DEBUG: Agregando error léxico: {error}")

            # Capturar errores sintácticos
            if syntax_errors and len(syntax_errors) > 0:
                for error in syntax_errors:
                    all_errors.append(f"SINTÁCTICO: {error}")
                    print(f"DEBUG: Agregando error sintáctico: {error}")
            
            # Capturar errores y advertencias semánticas
            if semantic_errors and len(semantic_errors) > 0:
                for error in semantic_errors:
                    all_errors.append(f"SEMÁNTICO: {error}")
                    print(f"DEBUG: Agregando error semántico: {error}")
            
            if semantic_warnings and len(semantic_warnings) > 0:
                for warning in semantic_warnings:
                    all_errors.append(f"ADVERTENCIA: {warning}")
                    print(f"DEBUG: Agregando advertencia: {warning}")
            
            # ===== CAPTURAR OUTPUT DETALLADO =====
            detailed_output = output_buffer.getvalue()
            
            # ===== MOSTRAR RESULTADOS EN LA INTERFAZ =====
            
            # Resultado principal
            result_text = "\n".join(results)
            
            if detailed_output:
                result_text += f"\n\n[DETALLES DEL ANÁLISIS]\n{'-' * 30}\n{detailed_output[:2000]}"
                if len(detailed_output) > 2000:
                    result_text += "\n... (salida truncada, ver logs para detalles completos)"
            
            # Agregar resumen final
            if not all_errors:
                result_text += "\n\n[RESUMEN FINAL]\n" + "="*20 + "\nANÁLISIS COMPLETADO EXITOSAMENTE\nNo se encontraron errores en el código Ruby"
            else:
                result_text += f"\n\n[RESUMEN FINAL]\n" + "="*20 + f"\nANÁLISIS COMPLETADO CON {len(all_errors)} ERROR(ES)\nRevisar panel de errores para detalles"
            
            self.result_console.setPlainText(result_text)
            
            # ===== MOSTRAR ERRORES =====
            if all_errors:
                error_text = f"Se encontraron {len(all_errors)} error(es):\n" + "="*50 + "\n\n"
                
                # Agrupar errores por tipo
                lexical_errors = [e for e in all_errors if e.startswith("LÉXICO:")]
                syntactic_errors = [e for e in all_errors if e.startswith("SINTÁCTICO:")]
                semantic_errors_list = [e for e in all_errors if e.startswith("SEMÁNTICO:")]
                warnings_list = [e for e in all_errors if e.startswith("ADVERTENCIA:")]
                
                if lexical_errors:
                    error_text += "[ERRORES LÉXICOS]\n"
                    for error in lexical_errors:
                        error_text += f"  • {error.replace('LÉXICO: ', '')}\n"
                    error_text += "\n"
                
                if syntactic_errors:
                    error_text += "[ERRORES SINTÁCTICOS]\n"
                    for error in syntactic_errors:
                        error_text += f"  • {error.replace('SINTÁCTICO: ', '')}\n"
                    error_text += "\n"
                
                if semantic_errors_list:
                    error_text += "[ERRORES SEMÁNTICOS]\n"
                    for error in semantic_errors_list:
                        error_text += f"  • {error.replace('SEMÁNTICO: ', '')}\n"
                    error_text += "\n"
                
                if warnings_list:
                    error_text += "[ADVERTENCIAS]\n"
                    for warning in warnings_list:
                        error_text += f"  • {warning.replace('ADVERTENCIA: ', '')}\n"
                
                self.errors_console.setPlainText(error_text)
            else:
                self.errors_console.setPlainText("ANÁLISIS EXITOSO\n\nNo se encontraron errores\n\nEl código Ruby es sintáctica y semánticamente correcto.")
                
        except Exception as e:
            # Error crítico durante el análisis
            error_details = f"ERROR CRÍTICO DURANTE EL ANÁLISIS:\n{str(e)}\n\nVerifique que el código sea válido."
            print(f"DEBUG: Error crítico capturado: {e}")
            self.errors_console.setPlainText(error_details)
            self.result_console.setPlainText("Análisis interrumpido por error crítico")
        
    def clear_input(self):
        """Limpiar todas las áreas de texto"""
        self.text_area.clear()
        self.result_console.clear()
        self.result_console.setPlaceholderText('Los resultados del análisis aparecerán aquí...')
        self.errors_console.clear()
        self.errors_console.setPlaceholderText('Los errores aparecerán aquí...')

    def load_sample_code(self):
        """Cargar código de ejemplo"""
        sample_code = '''# Ejemplo de código Ruby - Jonathan Zambrano
class Calculator
  def initialize(name)
    @name = name
  end

  def add_numbers(x, y)
    result = x + y
    puts "Suma: #{result}"
    return result
  end

  def add_strings(str1, str2)
    result = str1.to_i + str2.to_i
    puts "Suma de strings: #{result}"
    return result
  end
end

# Crear instancia y probar
calc = Calculator.new("MiCalculadora")
sum1 = calc.add_numbers(10, 20)
sum2 = calc.add_strings("15", "25")

puts "Resultados:"
puts sum1
puts sum2'''
        
        self.text_area.setPlainText(sample_code)
        self.result_console.setPlainText("Código de ejemplo cargado exitosamente")
        self.errors_console.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RubyExpressionValidator()
    ex.show()
    sys.exit(app.exec_())