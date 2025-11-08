import os
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
from core.logger import get_logs
from helpers.icon import get_icon
from ui.pages.logs.styles import LogPageStyle


class LogsPage(QWidget):
    styles = LogPageStyle()

    def __init__(self):
        super().__init__()
        self.log_file = os.path.join(os.getcwd(), "logs.json")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title = QLabel("📜 System Logs")
        title.setStyleSheet("color: #ccc; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.logs_text.setStyleSheet(self.styles.log_text())
        layout.addWidget(self.logs_text)

        self.reload_button = QPushButton(" Reload")
        self.reload_button.setIcon(QIcon(get_icon("reload.png")))
        self.reload_button.setIconSize(QSize(24, 24))
        self.reload_button.setStyleSheet(self.styles.button())

        self.export_button = QPushButton(" Export")
        self.reload_button.setIcon(QIcon(get_icon("save.png")))

        self.export_button.setIconSize(QSize(24, 24))
        self.export_button.setStyleSheet(self.styles.button())

        self.reload_button.clicked.connect(self.load_logs)
        self.export_button.clicked.connect(self.export_logs)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.reload_button)
        button_layout.addWidget(self.export_button)
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(0, 10, 10, 0)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_logs(self):
        self.logs_text.clear()
        logs = get_logs()

        if not logs:
            self.logs_text.setPlainText("No log data found.")
            return

        formatted_logs = "\n".join(
            f"[{log['timestamp']}] [{log['level']}] [{log['source']}] {log['message']}"
            for log in logs
        )

        self.logs_text.setPlainText(formatted_logs)

    def export_logs(self):
        if not os.path.exists(self.log_file):
            self.logs_text.append("No logs to export.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Export Logs", "logs_export.json", "JSON Files (*.json)"
        )
        if path:
            try:
                with open(self.log_file, "r") as src, open(path, "w") as dst:
                    dst.write(src.read())
                self.logs_text.append(f"Logs exported to {path}")
            except Exception as e:
                self.logs_text.append(f"Failed to export logs: {e}")

    def showEvent(self, event):
        """Override showEvent to load logs when the page is shown."""
        super().showEvent(event)
        self.load_logs()
