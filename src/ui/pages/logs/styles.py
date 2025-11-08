class LogPageStyle:
    def log_text(self):
        return """
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

    def button(self):
        return """
            QPushButton {
                background-color: #222;
                color: white;
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2196f3; }
            QPushButton:pressed { background-color: #0d47a1; }
        """
