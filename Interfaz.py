import sys
import io
import os
import traceback
from contextlib import redirect_stdout, redirect_stderr
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QLabel, QGridLayout, 
                             QProgressBar, QMessageBox, QSplitter, QDialog, QDialogButtonBox, QListWidget)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer

class AnalysisWorker(QThread):
    """Worker thread para análisis asíncrono"""
    finished = pyqtSignal(str, str)  # resultados, errores
    progress = pyqtSignal(str)  # progreso
    error = pyqtSignal(str)  # errores críticos
    
    def __init__(self, code):
        super().__init__()
        self.code = code
        self.results = []
        self.all_errors = []
        
    def run(self):
        """Ejecutar análisis en hilo separado"""
        try:
            self.emit_progress("Iniciando análisis completo...")
            
            # Buffer para capturar toda la salida
            output_buffer = io.StringIO()
            error_buffer = io.StringIO()
            
            with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
                # Análisis léxico
                self.emit_progress("Ejecutando análisis léxico...")
                self.analyze_lexical()
                
                # Análisis sintáctico
                self.emit_progress("Ejecutando análisis sintáctico...")
                self.analyze_syntactic()
                
                # Análisis semántico
                self.emit_progress("Ejecutando análisis semántico...")
                self.analyze_semantic()
            
            # Capturar salidas
            stdout_content = output_buffer.getvalue()
            stderr_content = error_buffer.getvalue()
            
            # Procesar resultados
            self.emit_progress("Procesando resultados...")
            result_text = self.format_results(stdout_content, stderr_content)
            error_text = self.format_errors()
            
            self.finished.emit(result_text, error_text)
            
        except Exception as e:
            self.error.emit(f"Error crítico durante el análisis: {str(e)}\n\n{traceback.format_exc()}")
    
    def emit_progress(self, message):
        """Emitir progreso con validación"""
        self.progress.emit(message)
    
    def analyze_lexical(self):
        """Análisis léxico mejorado"""
        try:
            # Import seguro con manejo de errores
            from AnalizadorLexico import test_lexical_analyzer
            
            # Ejecutar análisis
            result = test_lexical_analyzer(self.code)
            
            # Validar retorno y manejar diferentes formatos
            if result is None:
                tokens, error_tokens = [], []
                self.all_errors.append("LÉXICO: La función retornó None")
            elif isinstance(result, tuple) and len(result) == 2:
                tokens, error_tokens = result
            elif isinstance(result, list):
                tokens, error_tokens = result, []
            else:
                tokens, error_tokens = [str(result)], []
            
            # Validar tipos
            if not isinstance(tokens, list):
                tokens = [str(tokens)] if tokens else []
            if not isinstance(error_tokens, list):
                error_tokens = [str(errorTokens)] if errorTokens else []
            
            self.results.append("\n[1] ANÁLISIS LÉXICO")
            self.results.append("-" * 25)
            
            if tokens:
                self.results.append(f"Tokens reconocidos ({len(tokens)}):")
                self.results.extend([f"  {i+1}. {token}" for i, token in enumerate(tokens[:50])])  # Limitar a 50
                if len(tokens) > 50:
                    self.results.append(f"  ... y {len(tokens) - 50} tokens más")
            else:
                self.results.append("No se encontraron tokens")
            
            # Agregar errores léxicos
            if error_tokens:
                for error in error_tokens:
                    self.all_errors.append(f"LÉXICO: {error}")
            
            self.results.append("STATUS: Completado exitosamente")
            
        except ImportError as e:
            self.all_errors.append(f"LÉXICO: No se pudo importar AnalizadorLexico - {str(e)}")
        except Exception as e:
            self.all_errors.append(f"LÉXICO: Error durante análisis - {str(e)}")
    
    def analyze_syntactic(self):
        """Análisis sintáctico mejorado"""
        try:
            from AnalizadorSintactico import test_parser
            
            # Ejecutar análisis
            result = test_parser(self.code)
            
            # Validar retorno y manejar diferentes formatos
            if result is None:
                syntax_result, syntax_errors = [], []
                self.all_errors.append("SINTÁCTICO: La función retornó None")
            elif isinstance(result, tuple) and len(result) == 2:
                syntax_result, syntax_errors = result
            elif isinstance(result, list):
                syntax_result, syntax_errors = result, []
            else:
                syntax_result, syntax_errors = [str(result)], []
            
            # Validar tipos
            if not isinstance(syntax_result, list):
                syntax_result = [str(syntax_result)] if syntax_result else []
            if not isinstance(syntax_errors, list):
                syntax_errors = [str(syntax_errors)] if syntax_errors else []
            
            self.results.append("\n[2] ANÁLISIS SINTÁCTICO")
            self.results.append("-" * 28)
            
            if syntax_result:
                self.results.append("Estructura sintáctica:")
                self.results.extend([f"  {line}" for line in syntax_result[:30]])  # Limitar salida
                if len(syntax_result) > 30:
                    self.results.append(f"  ... y {len(syntax_result) - 30} líneas más")
            else:
                self.results.append("No se encontró estructura sintáctica")
            
            # Agregar errores sintácticos
            if syntax_errors:
                for error in syntax_errors:
                    self.all_errors.append(f"SINTÁCTICO: {error}")
            
            self.results.append("STATUS: Completado exitosamente")
            
        except ImportError as e:
            self.all_errors.append(f"SINTÁCTICO: No se pudo importar AnalizadorSintacticoCopy - {str(e)}")
        except Exception as e:
            self.all_errors.append(f"SINTÁCTICO: Error durante análisis - {str(e)}")
    
    def analyze_semantic(self):
        """Análisis semántico mejorado"""
        try:
            from AnalizadorSemantico import analizar_codigo
            
            # Ejecutar análisis
            result = analizar_codigo(self.code)
            
            # Validar retorno y manejar diferentes formatos
            if result is None:
                semantic_errors, semantic_warnings, symbol_table, defined_methods = [], [], {}, []
                self.all_errors.append("SEMÁNTICO: La función retornó None")
            elif isinstance(result, tuple) and len(result) == 4:
                semantic_errors, semantic_warnings, symbol_table, defined_methods = result
            elif isinstance(result, tuple) and len(result) == 2:
                semantic_errors, semantic_warnings = result
                symbol_table, defined_methods = {}, []
            elif isinstance(result, list):
                semantic_errors, semantic_warnings = result, []
                symbol_table, defined_methods = {}, []
            else:
                semantic_errors, semantic_warnings = [str(result)], []
                symbol_table, defined_methods = {}, []
            
            # Validar tipos
            if not isinstance(semantic_errors, list):
                semantic_errors = [str(semantic_errors)] if semantic_errors else []
            if not isinstance(semantic_warnings, list):
                semantic_warnings = [str(semantic_warnings)] if semantic_warnings else []
            if not isinstance(symbol_table, dict):
                symbol_table = {}
            if not isinstance(defined_methods, list):
                defined_methods = []
            
            self.results.append("\n[3] ANÁLISIS SEMÁNTICO")
            self.results.append("-" * 26)
            
            # Agregar información de la tabla de símbolos
            if symbol_table:
                self.results.append("Tabla de símbolos:")
                for key, value in list(symbol_table.items())[:10]:  # Limitar a 10 entradas
                    self.results.append(f"  {key}: {value}")
                if len(symbol_table) > 10:
                    self.results.append(f"  ... y {len(symbol_table) - 10} símbolos más")
            else:
                self.results.append("Tabla de símbolos: vacía")
            
            # Agregar métodos definidos
            if defined_methods:
                self.results.append("Métodos definidos:")
                for method in defined_methods[:10]:  # Limitar a 10 métodos
                    self.results.append(f"  {method}")
                if len(defined_methods) > 10:
                    self.results.append(f"  ... y {len(defined_methods) - 10} métodos más")
            else:
                self.results.append("Métodos definidos: ninguno")
            
            # Agregar errores semánticos
            if semantic_errors:
                for error in semantic_errors:
                    self.all_errors.append(f"SEMÁNTICO: {error}")
            
            # Agregar advertencias semánticas
            if semantic_warnings:
                for warning in semantic_warnings:
                    self.all_errors.append(f"ADVERTENCIA: {warning}")
            
            self.results.append("STATUS: Completado exitosamente")
            
        except ImportError as e:
            self.all_errors.append(f"SEMÁNTICO: No se pudo importar AnalizadorSemantico - {str(e)}")
        except Exception as e:
            self.all_errors.append(f"SEMÁNTICO: Error durante análisis - {str(e)}")
    
    def format_results(self, stdout_content, stderr_content):
        """Formatear resultados finales"""
        result_text = "\n".join(self.results)
        
        # Agregar salida detallada si existe
        if stdout_content.strip():
            result_text += f"\n\n[SALIDA DETALLADA]\n{'-' * 30}\n{stdout_content[:1500]}"
            if len(stdout_content) > 1500:
                result_text += "\n... (salida truncada)"
        
        if stderr_content.strip():
            result_text += f"\n\n[ERRORES DE SISTEMA]\n{'-' * 30}\n{stderr_content[:1000]}"
            if len(stderr_content) > 1000:
                result_text += "\n... (errores truncados)"
        
        # Resumen final
        if not self.all_errors:
            result_text += "\n\n[RESUMEN FINAL]\n" + "="*20 + "\n✅ ANÁLISIS COMPLETADO EXITOSAMENTE\nNo se encontraron errores en el código Ruby"
        else:
            result_text += f"\n\n[RESUMEN FINAL]\n" + "="*20 + f"\n❌ ANÁLISIS COMPLETADO CON {len(self.all_errors)} ERROR(ES)\nRevisar panel de errores para detalles"
        
        return result_text
    
    def format_errors(self):
        """Formatear errores por categoría"""
        if not self.all_errors:
            return "✅ ANÁLISIS EXITOSO\n\nNo se encontraron errores\n\nEl código Ruby es sintáctica y semánticamente correcto."
        
        error_text = f"Se encontraron {len(self.all_errors)} error(es):\n" + "="*50 + "\n\n"
        
        # Agrupar errores por tipo
        lexical_errors = [e for e in self.all_errors if e.startswith("LÉXICO:")]
        syntactic_errors = [e for e in self.all_errors if e.startswith("SINTÁCTICO:")]
        semantic_errors_list = [e for e in self.all_errors if e.startswith("SEMÁNTICO:")]
        warnings_list = [e for e in self.all_errors if e.startswith("ADVERTENCIA:")]
        
        if lexical_errors:
            error_text += f"🔍 [ERRORES LÉXICOS] ({len(lexical_errors)})\n"
            for error in lexical_errors:
                error_text += f"  • {error.replace('LÉXICO: ', '')}\n"
            error_text += "\n"
        
        if syntactic_errors:
            error_text += f"📝 [ERRORES SINTÁCTICOS] ({len(syntactic_errors)})\n"
            for error in syntactic_errors:
                error_text += f"  • {error.replace('SINTÁCTICO: ', '')}\n"
            error_text += "\n"
        
        if semantic_errors_list:
            error_text += f"🧠 [ERRORES SEMÁNTICOS] ({len(semantic_errors_list)})\n"
            for error in semantic_errors_list:
                error_text += f"  • {error.replace('SEMÁNTICO: ', '')}\n"
            error_text += "\n"
        
        if warnings_list:
            error_text += f"⚠️ [ADVERTENCIAS] ({len(warnings_list)})\n"
            for warning in warnings_list:
                error_text += f"  • {warning.replace('ADVERTENCIA: ', '')}\n"
        
        return error_text


class AlgorithmSelectorDialog(QDialog):
    """Diálogo para seleccionar algoritmos desde la carpeta algorithms"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_file = None
        self.algorithms_path = "algorithms"
        self.initUI()
        self.load_algorithms()
    
    def initUI(self):
        """Configurar interfaz del diálogo"""
        self.setWindowTitle('🔬 Seleccionar Algoritmo')
        self.setGeometry(200, 200, 500, 400)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Título
        title_label = QLabel('Selecciona un algoritmo para cargar:')
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # Lista de algoritmos
        self.algorithms_list = QListWidget()
        self.algorithms_list.setStyleSheet("""
            QListWidget {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                font-size: 12px;
                padding: 8px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e9ecef;
            }
            QListWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #e3f2fd;
            }
        """)
        layout.addWidget(self.algorithms_list)
        
        # Información del archivo seleccionado
        self.info_label = QLabel('Selecciona un archivo para ver información')
        self.info_label.setStyleSheet("font-size: 11px; color: #6c757d; margin: 5px;")
        layout.addWidget(self.info_label)
        
        # Botones
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                font-size: 12px;
                border-radius: 4px;
                margin: 2px;
            }
            QPushButton[text="OK"] {
                background-color: #28a745;
                color: white;
                border: none;
            }
            QPushButton[text="Cancel"] {
                background-color: #6c757d;
                color: white;
                border: none;
            }
        """)
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Eventos
        self.algorithms_list.itemSelectionChanged.connect(self.on_selection_changed)
        self.algorithms_list.itemDoubleClicked.connect(self.accept)
        
        self.setLayout(layout)
    
    def load_algorithms(self):
        """Cargar archivos .rb desde la carpeta algorithms"""
        self.algorithms_list.clear()
        
        if not os.path.exists(self.algorithms_path):
            self.algorithms_list.addItem("❌ Carpeta 'algorithms' no encontrada")
            self.info_label.setText("Crea la carpeta 'algorithms' en el directorio principal")
            return
        
        # Buscar archivos .rb
        ruby_files = []
        for file in os.listdir(self.algorithms_path):
            if file.endswith('.rb'):
                ruby_files.append(file)
        
        if not ruby_files:
            self.algorithms_list.addItem("📁 No hay archivos .rb en la carpeta algorithms")
            self.info_label.setText("Agrega archivos .rb a la carpeta 'algorithms'")
            return
        
        # Agregar archivos a la lista
        for file in sorted(ruby_files):
            file_path = os.path.join(self.algorithms_path, file)
            
            # Leer primeras líneas para obtener descripción
            description = self.get_file_description(file_path)
            
            # Crear item con icono y descripción
            item_text = f"📄 {file}"
            if description:
                item_text += f" - {description}"
            
            self.algorithms_list.addItem(item_text)
    
    def get_file_description(self, file_path):
        """Obtener descripción del archivo desde comentarios"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:10]  # Leer primeras 10 líneas
                
            for line in lines:
                line = line.strip()
                if line.startswith('#') and any(keyword in line.lower() for keyword in ['algoritmo', 'description', 'clase', 'ejemplo']):
                    # Limpiar comentario y retornar
                    clean_desc = line.replace('#', '').strip()
                    if len(clean_desc) > 50:
                        clean_desc = clean_desc[:47] + "..."
                    return clean_desc
            
            return "Algoritmo Ruby"
            
        except Exception as e:
            return "Sin descripción"
    
    def on_selection_changed(self):
        """Manejar cambio de selección"""
        current_item = self.algorithms_list.currentItem()
        if not current_item:
            return
        
        # Extraer nombre del archivo
        item_text = current_item.text()
        if item_text.startswith("📄 "):
            file_name = item_text.split(" - ")[0].replace("📄 ", "")
            file_path = os.path.join(self.algorithms_path, file_name)
            
            if os.path.exists(file_path):
                # Obtener información del archivo
                file_size = os.path.getsize(file_path)
                self.info_label.setText(f"📄 {file_name} ({file_size} bytes)")
                self.selected_file = file_path
            else:
                self.info_label.setText("❌ Archivo no encontrado")
                self.selected_file = None
        else:
            self.selected_file = None
    
    def get_selected_file(self):
        """Obtener archivo seleccionado"""
        return self.selected_file


class RubyExpressionValidator(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.analysis_in_progress = False
        self.initUI()

    def initUI(self):
        # Set up the window
        self.setWindowTitle('Ruby Expression Validator - Mejorado')
        self.setGeometry(100, 100, 1400, 800)
        
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

            QPushButton:disabled {
                background-color: #95a5a6;
                color: #7f8c8d;
            }

            QPushButton#run_button {
                background-color: #3498db;
                color: white;
            }

            QPushButton#run_button:hover:enabled {
                background-color: #2980b9;
            }

            QPushButton#run_button:pressed {
                background-color: #1f618d;
            }

            QPushButton#clear_button {
                background-color: #e67e22;
                color: white;
            }

            QPushButton#clear_button:hover:enabled {
                background-color: #d35400;
            }

            QPushButton#clear_button:pressed {
                background-color: #a0522d;
            }


            QPushButton#stop_button {
                background-color: #e74c3c;
                color: white;
            }

            QPushButton#stop_button:hover:enabled {
                background-color: #c0392b;
            }

            QPushButton#algorithms_button {
                background-color: #8e44ad;
                color: white;
            }

            QPushButton#algorithms_button:hover:enabled {
                background-color: #7d3c98;
            }

            QPushButton#algorithms_button:pressed {
                background-color: #6c3483;
            }

            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
                color: #2c3e50;
            }

            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 3px;
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

            #status_label {
                font-size: 12px;
                color: #7f8c8d;
                font-weight: normal;
                margin: 2px 0px;
            }
        """)

        # Main layout for the window
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # Header layout with logo and title
        header_layout = QHBoxLayout()
        
        # Ruby Logo desde archivo de imagen
        self.image_label = QLabel(self)
        try:
            # Cargar imagen desde la carpeta assets
            pixmap = QPixmap("assets/ruby_logo.png")  # Cambia por el nombre real de tu imagen
            
            # Verificar si la imagen se cargó correctamente
            if not pixmap.isNull():
                # Redimensionar la imagen manteniendo la proporción
                scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)
                self.image_label.setAlignment(Qt.AlignCenter)
                
                # Estilos para la imagen
                self.image_label.setStyleSheet("""
                    margin-right: 15px; 
                    border: 2px solid #e74c3c; 
                    border-radius: 8px; 
                    padding: 5px;
                    background-color: white;
                """)
                
                print("✅ Imagen del logo cargada exitosamente")
                
            else:
                # Si no se puede cargar la imagen, usar texto como respaldo
                self.image_label.setText("💎 RUBY")
                self.image_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #e74c3c; margin-right: 15px;")
                print("⚠️ No se pudo cargar la imagen, usando texto como respaldo")
                
        except Exception as e:
            # Si hay error, usar texto como respaldo
            self.image_label.setText("💎 RUBY")
            self.image_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #e74c3c; margin-right: 15px;")
            print(f"⚠️ Error al cargar imagen: {e}")
        
        # Title label
        self.title_label = QLabel('RUBY ANALYZER v2.0', self)
        self.title_label.setObjectName("title_label")
        
        header_layout.addWidget(self.image_label)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()  # Push everything to the left
        
        # Buttons layout in header
        buttons_layout = QHBoxLayout()
        
        # ===== BOTONES MEJORADOS =====
        self.run_button = QPushButton('🚀 ANALIZAR', self)
        self.run_button.setObjectName("run_button")
        
        self.stop_button = QPushButton('⏹️ DETENER', self)
        self.stop_button.setObjectName("stop_button")
        self.stop_button.setEnabled(False)
        
        self.clear_button = QPushButton('🧹 LIMPIAR', self)
        self.clear_button.setObjectName("clear_button")
    
        # ===== NUEVO BOTÓN PARA ALGORITMOS =====
        self.algorithms_button = QPushButton('🔬 ALGORITMOS', self)
        self.algorithms_button.setObjectName("algorithms_button")
        
        # ===== CONECTAR EVENTOS =====
        self.run_button.clicked.connect(self.analyze_ruby_code)
        self.stop_button.clicked.connect(self.stop_analysis)
        self.clear_button.clicked.connect(self.clear_input)
        self.algorithms_button.clicked.connect(self.load_algorithm_code)  # NUEVO EVENTO
        
        buttons_layout.addWidget(self.run_button)
        buttons_layout.addWidget(self.stop_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.algorithms_button)  # AGREGAR AL LAYOUT
        header_layout.addLayout(buttons_layout)
        
        # Add header to main layout
        main_layout.addLayout(header_layout)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        main_layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel('Listo para analizar código Ruby', self)
        self.status_label.setObjectName("text_expression_label")
        main_layout.addWidget(self.status_label)

        # Content layout with splitter
        content_splitter = QSplitter(Qt.Horizontal)
        content_splitter.setHandleWidth(10)

        # Left column: Text Expression area
        left_widget = QWidget()
        left_column_layout = QVBoxLayout(left_widget)
        
        self.text_expression_label = QLabel('📝 Código Ruby', self)
        self.text_expression_label.setObjectName("text_expression_label")
        
        self.text_area = QTextEdit(self)
        self.text_area.setPlaceholderText('# Escriba su código Ruby aquí...\n# Ejemplo:\nclass Calculator\n  def add(x, y)\n    x + y\n  end\nend\n\ncalc = Calculator.new\nresult = calc.add(5, 3)\nputs result')
        self.text_area.setMinimumHeight(500)
        
        left_column_layout.addWidget(self.text_expression_label)
        left_column_layout.addWidget(self.text_area)

        # Right column: Result and Errors sections
        right_widget = QWidget()
        right_column_layout = QVBoxLayout(right_widget)

        # Result section
        self.result_label = QLabel('📊 Resultados del Análisis', self)
        self.result_label.setObjectName("result_label")
        
        self.result_console = QTextEdit(self)
        self.result_console.setObjectName("result_console")
        self.result_console.setReadOnly(True)
        self.result_console.setPlaceholderText('Los resultados del análisis aparecerán aquí...')

        # Errors section
        self.errors_label = QLabel('⚠️ Errores y Advertencias', self)
        self.errors_label.setObjectName("errors_label")
        
        self.errors_console = QTextEdit(self)
        self.errors_console.setObjectName("errors_console")
        self.errors_console.setReadOnly(True)
        self.errors_console.setPlaceholderText('Los errores aparecerán aquí...')

        right_column_layout.addWidget(self.result_label)
        right_column_layout.addWidget(self.result_console)
        right_column_layout.addWidget(self.errors_label)
        right_column_layout.addWidget(self.errors_console)

        # Add widgets to splitter
        content_splitter.addWidget(left_widget)
        content_splitter.addWidget(right_widget)
        content_splitter.setSizes([800, 600])  # Set initial sizes

        # Add splitter to main layout
        main_layout.addWidget(content_splitter)

        # Set the main layout for the window
        self.setLayout(main_layout)

    def analyze_ruby_code(self):
        """Iniciar análisis asíncrono"""
        code = self.text_area.toPlainText().strip()
        
        if not code:
            QMessageBox.warning(self, "Advertencia", "No hay código para analizar")
            return
        
        if self.analysis_in_progress:
            QMessageBox.information(self, "Información", "Ya hay un análisis en progreso")
            return
        
        # Limpiar consolas
        self.result_console.clear()
        self.errors_console.clear()
        
        # Configurar UI para análisis
        self.analysis_in_progress = True
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Analizando código...")
        
        # Crear y configurar worker
        self.worker = AnalysisWorker(code)
        self.worker.finished.connect(self.on_analysis_finished)
        self.worker.progress.connect(self.on_progress_update)
        self.worker.error.connect(self.on_analysis_error)
        
        # Iniciar análisis
        self.worker.start()
    
    def stop_analysis(self):
        """Detener análisis en progreso"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait(3000)  # Wait up to 3 seconds
            
            if self.worker.isRunning():
                self.worker.kill()
                self.worker.wait()
            
            self.reset_ui_state()
            self.status_label.setText("Análisis detenido por el usuario")
            self.errors_console.setPlainText("ANÁLISIS INTERRUMPIDO\n\nEl análisis fue detenido por el usuario")
    
    def on_analysis_finished(self, results, errors):
        """Manejar finalización del análisis"""
        self.result_console.setPlainText(results)
        self.errors_console.setPlainText(errors)
        self.reset_ui_state()
        self.status_label.setText("Análisis completado exitosamente")
    
    def on_progress_update(self, message):
        """Actualizar progreso del análisis"""
        self.status_label.setText(message)
    
    def on_analysis_error(self, error_message):
        """Manejar errores críticos del análisis"""
        self.errors_console.setPlainText(error_message)
        self.result_console.setPlainText("Análisis interrumpido por error crítico")
        self.reset_ui_state()
        self.status_label.setText("Error durante el análisis")
        
        # Mostrar mensaje de error
        QMessageBox.critical(self, "Error Crítico", 
                           f"Ocurrió un error crítico durante el análisis:\n\n{error_message[:500]}...")
    
    def reset_ui_state(self):
        """Resetear estado de la UI después del análisis"""
        self.analysis_in_progress = False
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        if self.worker:
            self.worker.deleteLater()
            self.worker = None
        
    def clear_input(self):
        """Limpiar todas las áreas de texto"""
        if self.analysis_in_progress:
            QMessageBox.information(self, "Información", "No se puede limpiar durante el análisis")
            return
            
        self.text_area.clear()
        self.result_console.clear()
        self.result_console.setPlaceholderText('Los resultados del análisis aparecerán aquí...')
        self.errors_console.clear()
        self.errors_console.setPlaceholderText('Los errores aparecerán aquí...')
        self.status_label.setText("Listo para analizar código Ruby")


        
       # self.text_area.setPlainText(sample_code)
        self.result_console.setPlainText("✅ Código de ejemplo cargado exitosamente")
        self.errors_console.clear()
        self.status_label.setText("Código de ejemplo cargado - Listo para analizar")

    # En la clase RubyExpressionValidator, agregar el método:

    def load_algorithm_code(self):
        """Cargar código desde archivos de algoritmos"""
        if self.analysis_in_progress:
            QMessageBox.information(self, "Información", "No se puede cargar algoritmos durante el análisis")
            return
        
        # Mostrar diálogo de selección
        dialog = AlgorithmSelectorDialog(self)
        
        if dialog.exec_() == QDialog.Accepted:
            selected_file = dialog.get_selected_file()
            
            if selected_file and os.path.exists(selected_file):
                try:
                    # Leer archivo
                    with open(selected_file, 'r', encoding='utf-8') as f:
                        algorithm_code = f.read()
                    
                    # Cargar en el editor
                    self.text_area.setPlainText(algorithm_code)
                    
                    # Actualizar consolas
                    file_name = os.path.basename(selected_file)
                    self.result_console.setPlainText(f"✅ Algoritmo cargado: {file_name}\n\nArchivo: {selected_file}\nTamaño: {len(algorithm_code)} caracteres")
                    self.errors_console.clear()
                    self.status_label.setText(f"Algoritmo '{file_name}' cargado - Listo para analizar")
                    
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo:\n\n{str(e)}")
                    
            else:
                QMessageBox.warning(self, "Advertencia", "No se seleccionó un archivo válido")
    
    def closeEvent(self, event):
        """Manejar cierre de la aplicación"""
        if self.analysis_in_progress:
            reply = QMessageBox.question(self, 'Confirmar cierre', 
                                       'Hay un análisis en progreso. ¿Desea cerrarlo?',
                                       QMessageBox.Yes | QMessageBox.No, 
                                       QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.stop_analysis()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Configurar aplicación
    app.setApplicationName("Ruby Expression Validator")
    app.setApplicationVersion("2.0")
    
    # Crear y mostrar ventana principal
    ex = RubyExpressionValidator()
    ex.show()
    
    sys.exit(app.exec_())