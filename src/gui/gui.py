import sys
from datetime import datetime
from threading import Thread, Event

from PySide6.QtCore import Qt, Slot, QObject, Signal
from PySide6.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QLabel, QGridLayout, QMainWindow, QLineEdit

from src.data.data import client_style, agent_style, companion_style


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


class ChatLayout(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Chat")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.chat_receiver = kwargs.get('chat_receiver', None)
        self.companion_receiver = kwargs.get('companion_receiver', None)
        self.setup_ui()
        self.chat_receiver.messageReceived.connect(self.add_chat_message)
        self.companion_receiver.messageReceived.connect(self.add_companion_message)

    def setup_ui(self):
        """Initializes the ui for the application"""
        # init layout
        self.layout = QGridLayout(self.centralWidget())

        # Chat area to display messages
        self.column0 = QVBoxLayout()
        self.input_chat = QVBoxLayout()
        input_textbox = QLineEdit()
        self.input_chat.addWidget(input_textbox)

        # Second column for companion
        self.column1 = QVBoxLayout()

        self.layout.addLayout(self.column0, 0, 0)
        self.layout.addLayout(self.input_chat, 1, 0)
        self.layout.addLayout(self.column1, 0, 1)

    @Slot(dict)
    def add_chat_message(self, message_dict):
        speaker = message_dict.get("speaker", "agent")
        timestamp = message_dict.get(
            "timestamp", datetime.now().strftime("%H:%M:%S")
        )
        message = message_dict.get("message", "")

        if speaker == 'cliente':
            message_widget = QLabel(f"{timestamp}: {message}")
            message_widget.setAlignment(Qt.AlignLeft)
            message_widget.setStyleSheet(client_style)
        elif speaker == 'agente':
            message_widget = QLabel(f"{message} :{timestamp}")
            message_widget.setAlignment(Qt.AlignRight)
            message_widget.setStyleSheet(agent_style)

        self.column0.addWidget(message_widget)

    @Slot(dict)
    def add_companion_message(self, message_dict):
        timestamp = message_dict.get('timestamp')
        message = message_dict.get('message')

        message_widget = QLabel(f"{timestamp}: {message}")
        message_widget.setAlignment(Qt.AlignCenter)
        message_widget.setStyleSheet(companion_style)

        self.column1.addWidget(message_widget)


def run_app(*args, **kwargs):
    app = QApplication(sys.argv)
    transcribe_queue, companion_queue = args
    chat_receiver = MessageReceiver(transcribe_queue)
    companion_receiver = MessageReceiver(companion_queue)
    kwargs = {
        'companion_receiver': companion_receiver,
        'chat_receiver': chat_receiver
    }
    window = ChatLayout(**kwargs)
    window.show()

    chat_receiver.start_receiving_messages()
    companion_receiver.start_receiving_messages()

    sys.exit(app.exec())
