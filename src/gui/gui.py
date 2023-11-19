import sys
import time
from datetime import datetime
from threading import Thread, Event

from PySide6.QtCore import Qt, Slot, QObject, Signal
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QMainWindow, QSizePolicy, \
    QScrollArea, QListWidget, QHBoxLayout, QLineEdit, QPushButton, QListWidgetItem
from qt_material import apply_stylesheet

from src.data.data import client_style, agent_style, companion_style, input_style


class MessageReceiver(QObject):
    messageReceived = Signal(dict)

    def __init__(self, message_queue):
        super().__init__()
        self.message_queue = message_queue

    def start_receiving_messages(self):
        # Simulating receiving messages
        thread = Thread(
            target=self.simulate_message_receiving,
            daemon=True
        )
        thread.start()

    def simulate_message_receiving(self):
        while True:
            message_dict = self.message_queue.get()
            self.messageReceived.emit(message_dict)
            time.sleep(1)


class ChatLayout(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__()
        # Main window Config
        self.setWindowTitle("Chat")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.resize(800, 600)

        # Set message receiver objects
        self.chat_receiver = kwargs.get('chat_receiver')
        self.companion_receiver = kwargs.get('companion_receiver')

        # Load ui
        self.setup_ui()

        # Connect receivers
        self.chat_receiver.messageReceived.connect(self.add_chat_message)
        self.companion_receiver.messageReceived.connect(self.add_companion_message)

    def setup_ui(self):
        """Initializes the ui for the application"""
        # init layout
        self.layout = QGridLayout(self.centralWidget())

        """Left column"""
        column0_wrapper = QVBoxLayout()

        # Add title
        title = QLabel("Transcripción")
        title.setAlignment(Qt.AlignCenter)
        column0_wrapper.addWidget(title)

        # Chat history column
        self.column0 = QVBoxLayout()
        chat_area = QScrollArea()
        chat_area.setWidgetResizable(True)
        self.chat_history = QListWidget()
        self.chat_history.setLayout(self.column0)
        chat_area.setWidget(self.chat_history)
        column0_wrapper.addWidget(chat_area)

        # Set Column0 in layout
        self.layout.addLayout(column0_wrapper, 0, 0)
        self.layout.setColumnStretch(0, 2)

        # Input messages from user
        self.input_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.send = QPushButton("Send")
        self.send.clicked.connect(self.add_input)
        self.input_layout.addWidget(self.input)
        self.input_layout.addWidget(self.send)
        self.layout.addLayout(self.input_layout, 1, 0)

        """Right column"""
        column1_wrapper = QVBoxLayout()

        # Add title
        title = QLabel("Companion")
        title.setAlignment(Qt.AlignCenter)
        column1_wrapper.addWidget(title)

        # Companion text area
        self.column1 = QVBoxLayout()
        companion_area = QScrollArea()
        companion_area.setLayout(self.column1)
        column1_wrapper.addWidget(companion_area)

        # Set Column1 in layout
        self.layout.addLayout(column1_wrapper, 0, 1)

    def add_input(self):
        message = self.input.text()
        if message:
            message = f"User inputted: {message}"
            self.add_message_chat_history(message)
            self.input.clear()

    def add_message_chat_history(self, message: str | QLabel):
        item = QListWidgetItem(self.chat_history)

        if isinstance(message, str):
            message = QLabel(message)
            message.setAlignment(Qt.AlignRight)
            message.setStyleSheet(input_style)
            # message.setWordWrap(True)

        message.adjustSize()

        item.setSizeHint(message.sizeHint())
        self.chat_history.addItem(item)
        self.chat_history.setItemWidget(item, message)

    @Slot(dict)
    def add_chat_message(self, message_dict):
        """Adds a message to the chat layout"""
        speaker = message_dict.get("speaker", "agent")
        timestamp = message_dict.get(
            "timestamp", datetime.now().strftime("%H:%M:%S")
        )
        message = message_dict.get("message", "")

        if speaker == 'cliente':
            message_widget = QLabel(f"{timestamp} {message}")
            message_widget.setAlignment(Qt.AlignLeft)
            message_widget.setStyleSheet(client_style)
        elif speaker == 'agente':
            message_widget = QLabel(f"{message} {timestamp}")
            message_widget.setAlignment(Qt.AlignRight)
            message_widget.setStyleSheet(agent_style)

        message_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.add_message_chat_history(message_widget)

    @Slot(dict)
    def add_companion_message(self, message_dict):
        """Adds a message to the companion chat layout"""
        timestamp = message_dict.get('timestamp')
        message = message_dict.get('message')

        message_widget = QLabel(f"{timestamp} {message}")
        message_widget.setAlignment(Qt.AlignCenter)
        message_widget.setStyleSheet(companion_style)

        self.column1.addWidget(message_widget)


def run_app(*args, **kwargs):
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_red.xml')
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
