from PySide6.QtWidgets import QMainWindow
from src.rfmetadata.windows.main_window import MainWindow


def test_main_window_initialization(qtbot):

    window = MainWindow()

    qtbot.addWidget(window)
    assert isinstance(window, QMainWindow)

