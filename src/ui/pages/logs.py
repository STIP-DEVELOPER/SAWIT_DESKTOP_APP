import os
import json
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QFileDialog,
)


class LogsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.log_file = "logs.json"
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setStyleSheet(
            """
            background-color: #111;
            color: #0f0;
            border: 1px solid #333;
            font-family: Consolas, monospace;
            font-size: 13px;
        """
        )

        self.reload_button = QPushButton("🔄 Reload Logs")
        self.export_button = QPushButton("💾 Export Logs")
        for btn in [self.reload_button, self.export_button]:
            btn.setStyleSheet(self._button_style())

        self.reload_button.clicked.connect(self.load_logs)
        self.export_button.clicked.connect(self.export_logs)

        layout.addWidget(QLabel("📜 System Logs:"))
        layout.addWidget(self.logs_text)
        layout.addWidget(self.reload_button)
        layout.addWidget(self.export_button)
        layout.addStretch()
        self.setLayout(layout)

    def load_logs(self):
        self.logs_text.clear()
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r") as f:
                    logs = json.load(f)
                    self.logs_text.setPlainText(json.dumps(logs, indent=4))
            except Exception as e:
                self.logs_text.setPlainText(f"Error reading log: {e}")
        else:
            self.logs_text.setPlainText("No log file found.")

    def export_logs(self):
        if not os.path.exists(self.log_file):
            self.logs_text.append("No logs to export.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Logs", "logs_export.json", "JSON Files (*.json)"
        )
        if path:
            with open(self.log_file, "r") as src, open(path, "w") as dst:
                dst.write(src.read())
            self.logs_text.append(f"✅ Logs exported to {path}")

    def _button_style(self):
        return """
            QPushButton {
                background-color: #333;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #555; }
            QPushButton:pressed { background-color: #222; }
        """
