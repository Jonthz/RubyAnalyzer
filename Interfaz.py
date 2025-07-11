import sys
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QGridLayout
from PyQt5.QtCore import Qt

class RubyExpressionValidator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the window
        self.setWindowTitle('Ruby Expression Validator')
        self.setGeometry(100, 100, 1000, 600)
        
        # Apply custom styles using QSS (similar to CSS)
        self.setStyleSheet("""
            QWidget {
                font-family: 'Consolas', 'Monaco', monospace;
                background-color: #f0f0f0;
                color: #333333;
            }

            QLabel {
                font-size: 16px;
                color: #333333;
                font-weight: bold;
                margin: 5px 0px;
            }

            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #333333;
                border-radius: 5px;
                font-size: 14px;
                font-family: 'Consolas', 'Monaco', monospace;
                padding: 10px;
                line-height: 1.4;
            }

            QTextEdit:focus {
                border: 1px solid #007acc;
            }

            QPushButton {
                font-size: 20px;
                font-weight: bold;
                border: none;
                padding: 12px 20px;
                border-radius: 5px;
                margin: 2px;
                min-width: 100px;
                min-height: 40px;
            }

            QPushButton#run_button {
                background-color: #5a9fd4;
                color: white;
            }

            QPushButton#run_button:hover {
                background-color: #4a8fc4;
            }

            QPushButton#run_button:pressed {
                background-color: #3a7fb4;
            }

            QPushButton#clear_button {
                background-color: #d4af37;
                color: white;
            }

            QPushButton#clear_button:hover {
                background-color: #c49f27;
            }

            QPushButton#clear_button:pressed {
                background-color: #b48f17;
            }

            #title_label {
                font-size: 26px;
                font-weight: bold;
                color: #333333;
                margin-left: 10px;
            }

            #text_expression_label {
                font-size: 18px;
                color: #333333;
                margin-bottom: 5px;
            }

            #result_label, #errors_label {
                font-size: 18px;
                color: #333333;
                margin-bottom: 5px;
            }
        """)

        # Main layout for the window
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header layout with logo and title
        header_layout = QHBoxLayout()
        
        # Ruby Logo Image
        self.image_label = QLabel(self)
        pixmap = QPixmap('assets/Ruby_logo.png')
        if pixmap.isNull():
            # Create a placeholder if image is not found
            self.image_label.setText("💎")
            self.image_label.setStyleSheet("font-size: 40px; margin-right: 10px;")
        else:
            self.image_label.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # Title label
        self.title_label = QLabel('RUBY EXPRESSION\nVALIDATOR', self)
        self.title_label.setObjectName("title_label")
        
        header_layout.addWidget(self.image_label)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()  # Push everything to the left
        
        # Buttons layout in header
        buttons_layout = QHBoxLayout()
        self.run_button = QPushButton('▶ RUN', self)
        self.run_button.setObjectName("run_button")
        self.clear_button = QPushButton('🗑 CLEAR', self)
        self.clear_button.setObjectName("clear_button")
        
        self.run_button.clicked.connect(self.run_expression)
        self.clear_button.clicked.connect(self.clear_input)
        
        buttons_layout.addWidget(self.run_button)
        buttons_layout.addWidget(self.clear_button)
        
        header_layout.addLayout(buttons_layout)
        
        # Add header to main layout
        main_layout.addLayout(header_layout)

        # Content layout
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Left column: Text Expression area
        left_column_layout = QVBoxLayout()
        
        self.text_expression_label = QLabel('Text Expression', self)
        self.text_expression_label.setObjectName("text_expression_label")
        
        self.text_area = QTextEdit(self)
        self.text_area.setPlaceholderText('Write your syntax here')
        self.text_area.setMinimumHeight(350)
        
        # Add line numbers simulation
        self.setup_line_numbers()
        
        left_column_layout.addWidget(self.text_expression_label)
        left_column_layout.addWidget(self.text_area)

        # Right column: Result and Errors sections
        right_column_layout = QVBoxLayout()

        # Result section
        self.result_label = QLabel('Result', self)
        self.result_label.setObjectName("result_label")
        
        self.result_console = QTextEdit(self)
        self.result_console.setReadOnly(True)
        self.result_console.setPlaceholderText('Console\n>')
        self.result_console.setMaximumHeight(150)

        # Errors section
        self.errors_label = QLabel('Errors', self)
        self.errors_label.setObjectName("errors_label")
        
        self.errors_console = QTextEdit(self)
        self.errors_console.setReadOnly(True)
        self.errors_console.setPlaceholderText('>')
        self.errors_console.setMaximumHeight(150)

        right_column_layout.addWidget(self.result_label)
        right_column_layout.addWidget(self.result_console)
        right_column_layout.addWidget(self.errors_label)
        right_column_layout.addWidget(self.errors_console)
        right_column_layout.addStretch()  # Push content to top

        # Add columns to content layout
        content_layout.addLayout(left_column_layout, 1)  # Give more space to left column
        content_layout.addLayout(right_column_layout, 1)

        # Add content layout to main layout
        main_layout.addLayout(content_layout)

        # Set the main layout for the window
        self.setLayout(main_layout)

    def setup_line_numbers(self):
        # This is a simplified line number setup
        # In a real implementation, you'd want a more sophisticated line number widget
        initial_text = ""
        for i in range(1, 21):  # Show first 20 line numbers
            initial_text += f"{i}\n"
        
        # Set initial placeholder with line numbers appearance
        self.text_area.textChanged.connect(self.update_line_numbers)

    def update_line_numbers(self):
        # This is a basic implementation - in practice you'd want a separate line number widget
        pass

    def run_expression(self):
        expression = self.text_area.toPlainText()

        try:
            # WARNING: Using eval() is dangerous in production - this is just for demonstration
            result = eval(expression)
            self.result_console.setPlainText(f"Console\n> {str(result)}")
            self.errors_console.clear()
            self.errors_console.setPlaceholderText('>')
        except Exception as e:
            self.errors_console.setPlainText(f"> {str(e)}")
            self.result_console.clear()
            self.result_console.setPlaceholderText('Console\n>')

    def clear_input(self):
        self.text_area.clear()
        self.result_console.clear()
        self.result_console.setPlaceholderText('Console\n>')
        self.errors_console.clear()
        self.errors_console.setPlaceholderText('>')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RubyExpressionValidator()
    ex.show()
    sys.exit(app.exec_())