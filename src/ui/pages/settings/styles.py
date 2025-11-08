class SettingPageStyle:
    def model_layout(self):
        return """
            QComboBox {
                background-color: #222;
                color: #fff;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox:focus {
                border: 1px solid #00bcd4;
            }
            """

    def input_field(self):
        return """
                QLineEdit {
                    background-color: #222;
                    color: #fff;
                    border: 1px solid #555;
                    border-radius: 6px;
                    padding: 6px 10px;
                    font-size: 14px;
                }
                QLineEdit:focus {
                    border: 1px solid #00bcd4;
                }
            """

    def button(self):
        return """
            QPushButton {
                background-color: #222;
                color: white;
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2196f3; }
            QPushButton:pressed { background-color: #0d47a1; }
            """
