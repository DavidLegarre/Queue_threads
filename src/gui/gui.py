import sys

from PySide6.QtWidgets import QApplication, QDialog, QWidget, QTextEdit, QVBoxLayout


class ChatLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat")
        self.setup_ui()

    def setup_ui(self):
        """Initializes the ui for the application"""
        # init layout
        self.layout = QVBoxLayout()

        # Chat area to display messages
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.layout.addWidget(self.chat_area)

        # Input are for typing messages
        self.input_area = QTextEdit()
        self.layout.addWidget(self.input_area)

        # Send button



class App(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.form = Form()

    def run(self):
        self.form.show()
        sys.exit(self.exec())


def run_app(*args, **kwargs):
    app = App()
    app.run()
