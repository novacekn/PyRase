import sys

from PySide2.QtWidgets import QApplication
from controllers import PyRaseController


def main():
    app = QApplication(sys.argv)
    pyrase_controller = PyRaseController()
    pyrase_controller.ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

