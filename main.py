import json
import re

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
        self.emailInputLogin.setText ("ramy@ramy.nl") # for testing - remove in the final version!!!!
        # hide error messaages in the GUI by default
        self.errorTextSignUp.setText("")
        self.errorTextLogin.setText("")


    def logIN (self):

        if self.emailInputLogin.text() :
            # Load the JSON file
            with open('users.json', 'r') as file:
                users_data = json.load(file)

            # Check if the new user already exists
            global userEmail, userName
            for user in users_data['UsersDB'].values():
                if user['Email'] == self.emailInputLogin.text():
                    
                    userEmail = self.emailInputLogin.text()
                    userName = user['Name']
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

        # Set the title of the workspace based on user's name!
        self.titleWorkspaceLabel.setText(f"{userName}'s Workspace!")
        # Hide error messages by default from the GUI
        self.errorTextRecipientsEmailLabel.setText("")
        self.errorTextProjectLabel.setText("")
        self.errorTextSubjectLabel.setText("")

        # Remove default example items from UI
        self.deleteRecipientCombo.clear()

        # Display lists 
        self.displayRecipients()

        self.addRecipientButton.clicked.connect(self.addRecipient)
        self.deleteRecipientButton.clicked.connect(self.deleteRecipient)


    def displayRecipients (self) :

        with open('recipients.json') as f:
            users = json.load(f)['RecipientsDB']

        email_to_find = userEmail
        for key in users:
            if users[key]['Email'] == email_to_find:
                recipients = users[key]['RecipientsEmails']
                self.deleteRecipientCombo.clear()
                self.deleteRecipientCombo.addItems(recipients)
                break
        else:
            pass #print(f"No user with email {email_to_find} was found to have a recipients list.")


    def is_valid_email(self, email_to_check):
        
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(email_pattern, email_to_check))


    def addRecipient (self) :

        addRecipient_email = self.addRecipientInput.text()

        if self.is_valid_email(addRecipient_email) : # If what the user typed is actually a valid email

            with open('recipients.json') as f:
                recipients_db = json.load(f)

            # Find the user's email in the JSON
            user_email = userEmail
            for user in recipients_db["RecipientsDB"].values():
                if user["Email"] == user_email:

                    if addRecipient_email in user['RecipientsEmails']: # does this email already exisit in RecipientsEmails?
                        self.errorTextRecipientsEmailLabel.setText(f"{addRecipient_email} already exists in the list of recipients.")
                    else :
                        user["RecipientsEmails"].append(addRecipient_email) # DONE!
                        self.errorTextRecipientsEmailLabel.setText(f"{addRecipient_email} was added.")

                        # Save the updated JSON to file
                        with open('recipients.json', 'w') as f:
                            json.dump(recipients_db, f)

                        self.displayRecipients() # update the GUI
        else :
            self.errorTextRecipientsEmailLabel.setText("This is not a valid email address!")

    def deleteRecipient (self):

        recipientToDelete = self.deleteRecipientCombo.currentText()

        # Load the JSON file into a dictionary
        with open('recipients.json', 'r') as f:
            recipients_db = json.load(f)

        # Find the user
        for user in recipients_db['RecipientsDB'].values():
            if user['Email'] == userEmail:
                # Check if recipientToDelete exists in the user's list of recipients
                if recipientToDelete in user['RecipientsEmails']:
                    # Remove recipientToDelete from the list of recipients
                    user['RecipientsEmails'].remove(recipientToDelete)
                break

        # Save the updated dictionary to the JSON file
        with open('recipients.json', 'w') as f:
            json.dump(recipients_db, f, indent=2)

        self.displayRecipients()


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
