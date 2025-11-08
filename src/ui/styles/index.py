class StyleShared:
    def exit_button(self):
        return """
            QPushButton {
                background-color: #f52c80;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #d32f2f; }
            QPushButton:pressed { background-color: #880e4f; }
            """

    def menu_button(self):
        return """
                QPushButton {
                    background-color: #1a1a1a;
                    color: white;
                    border-radius: 6px;
                    padding: 8px 20px;
                    font-size: 14px;
                }
                QPushButton:hover { background-color: #333; }
                QPushButton:checked {
                    background-color: #00aaff;
                    color: black;
                    font-weight: bold;
                }
                """
