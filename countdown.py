from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QWidget
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Countdown Timer")
        self.resize(300, 100)

        # Create the widgets
        self.timeLabel = QLabel(self)
        self.startStopButton = QPushButton("Start", self)
        self.startStopButton.clicked.connect(self.start_stop_timer)

        # Create the layouts
        hbox = QHBoxLayout()
        hbox.addWidget(self.timeLabel)
        hbox.addWidget(self.startStopButton)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        # Set the main widget
        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        # Initialize the timer
        self.timer = QTimer(self)
        self.timer.setInterval(1000) # 1 second
        self.timer.timeout.connect(self.update_time)
        self.remaining_time = QTime(0, 25, 0) # 25 minutes

    def start_stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.startStopButton.setText("Start")
        else:
            self.timer.start()
            self.startStopButton.setText("Stop")

    def update_time(self):
        self.remaining_time = self.remaining_time.addSecs(-1)
        if self.remaining_time.minute() == 0 and self.remaining_time.second() == 0:
            self.timer.stop()
            self.startStopButton.setText("Start")
        self.timeLabel.setText(self.remaining_time.toString("mm:ss"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())