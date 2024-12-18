"""
anydoc_to_markdown

A tool for converting various document formats to markdown.
Uses the MarkItDown library to handle the conversion of different file types.
Supports both GUI and CLI modes.
"""

from gui.main_window import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()