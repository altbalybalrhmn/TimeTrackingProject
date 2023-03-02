import datetime
import re
from PyQt5.QtWidgets import QMessageBox


def DayMonthYear(timestmap):

    timestmap = float(timestmap)
    datetime_object = datetime.datetime.fromtimestamp(timestmap)
    result = datetime_object.strftime("%d/%m/%Y")

    return (result)


def HourMinute12HoursFormat(timestmap):

    timestmap = float(timestmap)
    datetime_object = datetime.datetime.fromtimestamp(timestmap)
    result = datetime_object.strftime("%I:%M%p")

    return (result)


# print (HourMinute12HoursFormat("1677493119.798744"))


def is_valid_email(email_to_check):

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(email_pattern, email_to_check))


def show_popup(txt):
    # Create and show the popup message
    msg = QMessageBox()
    msg.setText(txt)
    msg.setWindowTitle("PomodoroApp")
    msg.exec_()


def show_popupYesNo(txt):
    # Create and show the popup message
    msg = QMessageBox()
    msg.setText(txt)
    msg.setWindowTitle("PomodoroApp")

    # Add buttons for yes or no
    yes_button = msg.addButton(QMessageBox.Yes)
    no_button = msg.addButton(QMessageBox.No)

    # Set the default button to be "No"
    msg.setDefaultButton(no_button)

    # Execute the popup message and check the user's choice
    choice = msg.exec_()
    if choice == QMessageBox.Yes:
        return True  # print("YESSSSSSSSSSes")
    elif choice == QMessageBox.No:
        return False  # print("NOOOOOOOOO")
