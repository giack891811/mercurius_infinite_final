# dashboard.py
"""
Mercurius∞ GUI – Interfaccia interattiva con stream webcam, trascrizione vocale, stato agenti
"""

import sys
import cv2
import threading
import speech_recognition as sr
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QListWidget, QHBoxLayout, QSplitter, QGraphicsView, QGraphicsScene
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap


class WebcamThread(QThread):
    frame_ready = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
                self.frame_ready.emit(img)


class SpeechThread(QThread):
    result_ready = pyqtSignal(str)

    def run(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            while True:
                audio = recognizer.listen(source)
                try:
                    text = recognizer.recognize_google(audio, language="it-IT")
                    self.result_ready.emit(text)
                except sr.UnknownValueError:
                    self.result_ready.emit("[...]")
                except sr.RequestError:
                    self.result_ready.emit("❌ Errore STT")


class MercuriusDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 Mercurius∞ – Interfaccia Sensoriale")
        self.setGeometry(100, 100, 1040, 640)

        self.menu = QListWidget()
        self.menu.addItems(["Stato", "Agenti", "Memoria", "Voce", "Visione", "Log", "Test"])
        self.menu.currentRowChanged.connect(self.change_section)

        self.content_area = QTextEdit()
        self.content_area.setReadOnly(True)

        self.btn_action = QPushButton("Esegui Comando")
        self.btn_action.clicked.connect(self.execute_action)

        sidebar = QVBoxLayout()
        sidebar.addWidget(QLabel("🔧 Menu"))
        sidebar.addWidget(self.menu)
        sidebar.addWidget(self.btn_action)

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(sidebar_widget)
        self.splitter.addWidget(self.content_area)

        layout = QHBoxLayout()
        layout.addWidget(self.splitter)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_status)
        self.timer.start(3000)

        # Webcam e STT
        self.cam_view = QLabel()
        self.scene = QGraphicsScene()
        self.stt_live = QTextEdit()
        self.stt_live.setReadOnly(True)

        self.cam_thread = WebcamThread()
        self.cam_thread.frame_ready.connect(self.update_cam)
        self.cam_thread.start()

        self.stt_thread = SpeechThread()
        self.stt_thread.result_ready.connect(self.update_speech)
        self.stt_thread.start()

    def update_cam(self, image):
        self.cam_view.setPixmap(QPixmap.fromImage(image).scaled(480, 360, Qt.KeepAspectRatio))

    def update_speech(self, text):
        self.stt_live.append(f"🗣️ {text}")

    def change_section(self, index):
        if index == 4:  # Visione
            self.content_area.setWidgetResizable(True)
            self.content_area.setPlainText("")
            self.splitter.widget(1).deleteLater()
            container = QWidget()
            cam_layout = QVBoxLayout()
            cam_layout.addWidget(QLabel("📷 Webcam Live"))
            cam_layout.addWidget(self.cam_view)
            container.setLayout(cam_layout)
            self.splitter.insertWidget(1, container)

        elif index == 3:  # Voce
            self.content_area.setWidgetResizable(True)
            self.splitter.widget(1).deleteLater()
            container = QWidget()
            stt_layout = QVBoxLayout()
            stt_layout.addWidget(QLabel("🎤 Trascrizione Vocale Live"))
            stt_layout.addWidget(self.stt_live)
            container.setLayout(stt_layout)
            self.splitter.insertWidget(1, container)

        elif index == 1:  # Agenti
            self.content_area.setPlainText("🤖 Agenti attivi:\n- Neo\n- AZR\n- MemoryTrainer")

        else:
            text_map = {
                0: "🧠 Stato:\n- Moduli online\n- Sensori attivi\n- Memoria attiva",
                2: "💾 Memoria:\n- Episodica: OK\n- Sinaptica: OK",
                5: "📜 Log:\n- Avvio: OK\n- Nessun errore rilevato",
                6: "🧪 TEST:\nPremi Esegui per simulare pensiero"
            }
            self.content_area.setPlainText(text_map.get(index, ""))

    def execute_action(self):
        self.content_area.append("🧠 Elaborazione pensiero...")

    def refresh_status(self):
        if self.menu.currentRow() == 0:
            self.change_section(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MercuriusDashboard()
    gui.show()
    sys.exit(app.exec_())
