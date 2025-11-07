import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from controllers.main_controller import MainController
from core.logger import add_log
from enums.log import LogLevel, LogSource


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.controller = MainController(window)
    window.show()
    sys.exit(app.exec_())

    add_log(LogLevel.INFO.value, LogSource.MAIN.value, "Application started")


if __name__ == "__main__":
    main()
