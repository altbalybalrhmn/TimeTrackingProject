import json

from time import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

class LoginUI(QDialog):
    def __init__(self):
        super(LoginUI,self).__init__()
        loadUi("./UI/login.ui",self)

        # This is example of changing screen
        self.loginButton.clicked.connect(self.logIN)

        self.signUpButton.clicked.connect(self.signUp)

        # hide error messaages in the GUI by default
        self.errorTextSignUp.setText("")
        self.errorTextLogin.setText("")


    def logIN (self):
        if self.emailInputLogin.text() :
            # Load the JSON file
            with open('users.json', 'r') as file:
                users_data = json.load(file)

            # Check if the new user already exists

            for user in users_data['UsersDB'].values():
                if user['Email'] == self.emailInputLogin.text():
                    self.go_main_menu()
                    break
            else:
                self.errorTextLogin.setText("Email does not exist!")
        else:
            self.errorTextLogin.setText("Email can't be empty")

    def signUp (self) :

        name = self.nameInputSignUp.text()
        new_user_email = self.emailInputSignUp.text()

        if name and new_user_email :

            # Load the JSON file
            with open('users.json', 'r') as file:
                users_data = json.load(file)

            # Check if the new user already exists

            for user in users_data['UsersDB'].values():
                if user['Email'] == new_user_email:
                    self.errorTextSignUp.setText("User with email address already exists.")

                    break
            else:
                # Add the new user
                new_user_id = str(len(users_data['UsersDB']) + 1)
                new_user = {'Email': new_user_email, 'Name': name}  
                users_data['UsersDB'][new_user_id] = new_user

                # Save the updated JSON file
                with open('users.json', 'w') as file:
                    json.dump(users_data, file, indent=4)
                
                self.errorTextSignUp.setText("New user added, you may login!")
        else:
            self.errorTextSignUp.setText("Name or email is empty!")


    def go_main_menu(self):
        main_menu = MainMenuUI()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)


class MainMenuUI(QDialog):
    def __init__(self):
        super(MainMenuUI,self).__init__()
        loadUi("./UI/mainMenu.ui",self)

class PomodoroUI(QDialog):
    def __init__(self):
        super(PomodoroUI,self).__init__()
        loadUi("./UI/pomodoro.ui",self)


class ShortBreakUI(QDialog):
    def __init__(self):
        super(ShortBreakUI,self).__init__()
        loadUi("./UI/shortBreak.ui",self)

class LongBreakUI(QDialog):
    def __init__(self):
        super(LongBreakUI,self).__init__()
        loadUi("./UI/longBreak.ui",self)


app = QApplication(sys.argv)
UI = LoginUI() # This line determines which screen you will load at first

# You can also try one of other screens to see them.
    # UI = MainMenuUI()
    # UI = PomodoroUI()
    # UI = ShortBreakUI()
    # UI = LongBreakUI()

widget = QtWidgets.QStackedWidget()
widget.addWidget(UI)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.setWindowTitle("Time Tracking App")
widget.show()
sys.exit(app.exec_())
