import sys
from PyQt6.QtWidgets import QApplication

from app.container import build_container
from app.navegation import Navigation


def main():
    app = QApplication(sys.argv)

    container = build_container()
    navigation = Navigation(app, container)

    navigation.show_login()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()