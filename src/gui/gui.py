import sys
from datetime import datetime
from threading import Thread, Event

from PySide6.QtCore import Qt, Slot, QObject, Signal
from PySide6.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QLabel

from src.data.data import client_style, agent_style


class MessageReceiver(QObject):
    messageReceived = Signal(dict)

    def __init__(self, message_queue):
        super().__init__()
        self.message_queue = message_queue

    def start_receiving_messages(self):
        # Simulating receiving messages
        thread = Thread(
            target=self.simulate_message_receiving
        )
        thread.start()

    def simulate_message_receiving(self):
        while not self.message_queue.empty():
            message_dict = self.message_queue.get()
            self.messageReceived.emit(message_dict)
            Event().wait(2)


class ChatLayout(QWidget):
    def __init__(self, message_receiver):
        super().__init__()
        self.layout = None
        self.chat_area = None
        self.input_area = None
        self.setWindowTitle("Chat")
        self.message_receiver = message_receiver
        self.setup_ui()
        self.message_receiver.messageReceived.connect(self.add_message)

    def setup_ui(self):
        """Initializes the ui for the application"""
        # init layout
        self.layout = QVBoxLayout()

        # Chat area to display messages
        self.chat_area = QVBoxLayout()
        self.layout.addLayout(self.chat_area)

        # Input are for typing messages
        self.input_area = QTextEdit()
        self.layout.addWidget(self.input_area)

        self.setLayout(self.layout)

    @Slot(dict)
    def add_message(self, message_dict):
        speaker = message_dict.get("speaker", "agent")
        timestamp = message_dict.get(
            "timestamp", datetime.now().strftime("%H:%M:%S")
        )
        message = message_dict.get("message", "")
        message_widget = QLabel(f"{timestamp}: {message}")

        if speaker == 'cliente':
            message_widget.setAlignment(Qt.AlignLeft)
            message_widget.setStyleSheet(client_style)
        elif speaker == 'agente':
            message_widget.setAlignment(Qt.AlignRight)
            message_widget.setStyleSheet(agent_style)

        self.chat_area.addWidget(message_widget)


def run_app(*args, **kwargs):
    app = QApplication(sys.argv)
    transcribe_queue = args[0]
    message_receiver = MessageReceiver(transcribe_queue)
    window = ChatLayout(message_receiver)
    window.show()

    message_receiver.start_receiving_messages()

    sys.exit(app.exec())
