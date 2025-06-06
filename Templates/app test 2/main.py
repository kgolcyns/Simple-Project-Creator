# main.py
# Main entry point for the application.
# Run this file to start the application.
import sys
#from exceptionhandler import *
import mainwindow
from app import Application

if __name__ == "__main__":
    app = Application(sys.argv); app.setStyle("Windows")
    win = mainwindow.MainWindow()
    win.show()
    app.exec_()
    #sys.exit(app.exec_())