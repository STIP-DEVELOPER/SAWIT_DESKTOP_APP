import os
import json
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QHBoxLayout,
    QSizePolicy,
)


class LogsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.log_file = "logs.json"
        self._build_ui()
        self.load_logs()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # ======================
        # Label judul
        # ======================
        title = QLabel("📜 System Logs")
        title.setStyleSheet("color: #ccc; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # ======================
        # Area teks log
        # ======================
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.logs_text.setStyleSheet(
            """
            QTextEdit {
                background-color: #111;
                color: #0f0;
                border: 1px solid #333;
                border-radius: 6px;
                font-family: Consolas, monospace;
                font-size: 13px;
                padding: 8px;
            }
            """
        )
        layout.addWidget(self.logs_text)

        # ======================
        # Tombol Reload & Export (kanan bawah)
        # ======================
        self.reload_button = QPushButton(" Reload")
        self.reload_button.setIcon(QIcon(os.path.join("assets", "icons", "reload.png")))
        self.reload_button.setIconSize(QSize(24, 24))
        self.reload_button.setStyleSheet(self._button_style())

        self.export_button = QPushButton(" Export")
        self.export_button.setIcon(QIcon(os.path.join("assets", "icons", "save.png")))
        self.export_button.setIconSize(QSize(24, 24))
        self.export_button.setStyleSheet(self._button_style())

        self.reload_button.clicked.connect(self.load_logs)
        self.export_button.clicked.connect(self.export_logs)

        # Layout horizontal untuk tombol
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # dorong tombol ke kanan
        button_layout.addWidget(self.reload_button)
        button_layout.addWidget(self.export_button)
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(0, 10, 10, 0)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_logs(self):
        self.logs_text.clear()
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r") as f:
                    logs = json.load(f)
                    self.logs_text.setPlainText(json.dumps(logs, indent=4))
            except Exception as e:
                self.logs_text.setPlainText(f"❌ Error reading log: {e}")
        else:
            self.logs_text.setPlainText("⚠️ No log file found.")

    def export_logs(self):
        if not os.path.exists(self.log_file):
            self.logs_text.append("\n⚠️ No logs to export.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Export Logs", "logs_export.json", "JSON Files (*.json)"
        )
        if path:
            try:
                with open(self.log_file, "r") as src, open(path, "w") as dst:
                    dst.write(src.read())
                self.logs_text.append(f"\n✅ Logs exported to {path}")
            except Exception as e:
                self.logs_text.append(f"\n❌ Failed to export logs: {e}")

    def _button_style(self):
        return """
            QPushButton {
                background-color: #1976d2;
                color: white;
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2196f3; }
            QPushButton:pressed { background-color: #0d47a1; }
        """
