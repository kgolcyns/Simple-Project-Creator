# app.py
# The QtApplication Class
import version
from PyQt5.QtWidgets import QApplication

class Application(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setApplicationName(version.display_name)
        self.setApplicationVersion(version.version)
