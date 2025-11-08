class HomePageStyle:

    def button_style(self):
        return """
            QToolButton {
                background-color: #222;
                border-radius: 6px;
                color: white;
                font-size: 14px;
                padding: 6px 14px;
            }
            QToolButton:hover { background-color: #444; }
            QToolButton:pressed { background-color: #000; }
        """

    def camera_style(self):
        return """
            border: 2px solid #444;
            background-color: #111;
            color: #aaa;
            font-size: 14px;
        """

    def log_style(self):
        return """
            QTextEdit {
                background-color: rgba(0, 0, 0, 150);
                color: #0f0;
                font-family: Consolas, monospace;
                font-size: 12px;
                border: 1px solid #333;
                border-radius: 6px;
                padding: 6px;
            }
        """
