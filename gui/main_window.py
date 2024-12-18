"""
Main window implementation for the AnyDoc to Markdown converter GUI.
"""

import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QPushButton, QLabel, QFileDialog, QMessageBox,
                            QDialog, QHBoxLayout)
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
import subprocess

# Import the converter function
from converter import convert_to_markdown, save_to_file

class DropArea(QLabel):
    file_dropped = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create layout for the drop area
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add spacer at top
        layout.addStretch()
        
        # Add drop text label
        self.drop_text = QLabel("Drop File Here\nor")
        self.drop_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.drop_text)
        
        # Add browse button
        self.browse_btn = QPushButton("Browse File")
        self.browse_btn.setFixedWidth(120)  # Set fixed width for better appearance
        self.browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_btn)
        
        # Add spacer at bottom
        layout.addStretch()
        
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #666;
                border-radius: 6px;
                background-color: #2b2b2b;
                color: #ccc;
                padding: 20px;
            }
            QPushButton {
                background-color: #0d47a1;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)
        self.setAcceptDrops(True)

    def browse_file(self):
        file_filter = "Supported Files (*.pdf *.doc *.docx *.ppt *.pptx *.xls *.xlsx *.html *.htm *.txt *.json *.xml)"
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File to Convert",
            "",
            file_filter
        )
        if file_path:
            self.file_dropped.emit(file_path)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files:
            self.file_dropped.emit(files[0])

class SuccessDialog(QDialog):
    def __init__(self, output_path, parent=None):
        super().__init__(parent)
        self.output_path = output_path
        self.setWindowTitle("Conversion Successful")
        self.setMinimumWidth(400)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Add success message
        message = QLabel(f"Successfully converted to:\n{output_path}")
        message.setWordWrap(True)
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message)
        
        # Create button container
        button_layout = QHBoxLayout()
        
        # Create buttons
        open_file_btn = QPushButton("Open File")
        open_folder_btn = QPushButton("Open Folder")
        close_btn = QPushButton("Close")
        
        # Add buttons to layout
        button_layout.addWidget(open_file_btn)
        button_layout.addWidget(open_folder_btn)
        button_layout.addWidget(close_btn)
        
        # Add button layout to main layout
        layout.addLayout(button_layout)
        
        # Connect buttons
        open_file_btn.clicked.connect(self.open_file)
        open_folder_btn.clicked.connect(self.open_folder)
        close_btn.clicked.connect(self.accept)
        
        # Apply style
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #ffffff;
                margin: 10px;
            }
            QPushButton {
                background-color: #0d47a1;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 100px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)

    def open_file(self):
        if sys.platform == "win32":
            os.startfile(self.output_path)
        else:
            subprocess.run(["xdg-open", self.output_path])

    def open_folder(self):
        folder_path = os.path.dirname(self.output_path)
        if sys.platform == "win32":
            os.startfile(folder_path)
        else:
            subprocess.run(["xdg-open", folder_path])

class MainWindow(QMainWindow):
    SUPPORTED_FORMATS = [
        "*.pdf", "*.doc", "*.docx", "*.ppt", "*.pptx", "*.xls", "*.xlsx",
        "*.html", "*.htm", "*.txt",
        "*.json", "*.xml",
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AnyDoc to Markdown Converter")
        self.setMinimumSize(600, 400)
        self.current_file = None

        # Set up the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create and add drop area
        self.drop_area = DropArea()
        self.drop_area.file_dropped.connect(self.process_file)
        layout.addWidget(self.drop_area)

        # Selected file label
        self.file_label = QLabel("No file selected")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.file_label)

        # Convert button
        self.convert_btn = QPushButton("Convert to Markdown")
        self.convert_btn.clicked.connect(self.convert_file)
        self.convert_btn.setEnabled(False)
        layout.addWidget(self.convert_btn)

        # Supported formats label
        formats_label = QLabel("Supported Formats:\n" + 
                             "• PDF, PowerPoint, Word, Excel\n" +
                             "• HTML, JSON, XML, TXT")
        formats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(formats_label)

        self.apply_dark_style()

    def apply_dark_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QPushButton {
                background-color: #0d47a1;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:disabled {
                background-color: #666666;
            }
            QLabel {
                color: #cccccc;
            }
        """)

    def process_file(self, file_path):
        self.current_file = file_path
        self.file_label.setText(f"Selected: {os.path.basename(file_path)}")
        self.convert_btn.setEnabled(True)

    def convert_file(self):
        if not self.current_file:
            return

        try:
            # Convert the document to markdown
            markdown_content = convert_to_markdown(self.current_file)
            
            # Create output filename
            output_path = os.path.splitext(self.current_file)[0] + ".md"
            save_to_file(markdown_content, output_path)
            
            # Show success dialog with options
            dialog = SuccessDialog(output_path, self)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error converting file:\n{str(e)}"
            )

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 