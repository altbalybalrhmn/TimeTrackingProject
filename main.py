import json
import re

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

from PyQt5.QtCore import QTimer, QTime


import utils.dbReader
import utils.formating
import utils.dbWriter


class LoginUI(QDialog):
    def __init__(self):
        super(LoginUI,self).__init__()
        loadUi("./UI/login.ui",self)

        # This is example of changing screen
        self.loginButton.clicked.connect(self.logIN)

        self.signUpButton.clicked.connect(self.signUp)
        # for testing - remove in the final version!!!!
        self.emailInputLogin.setText("mr@cool.com")
        # hide error messaages in the GUI by default
        self.errorTextSignUp.setText("")
        self.errorTextLogin.setText("")

        self.emailInputLogin.returnPressed.connect(self.logIN)

    def logIN(self):

        global userEmail, userName

    def logIN (self):

            data = utils.dbReader.fetch_jsonDB()

            # Check if the new user already exists
            if utils.dbReader.user_exists(self.emailInputLogin.text(), data):
                userEmail = self.emailInputLogin.text()
                userName = utils.dbReader.get_username_from_email(
                    self.emailInputLogin.text(), data)
                self.go_main_menu()
            else:
                self.errorTextLogin.setText("Email does not exist!")
        else:
            self.errorTextLogin.setText("Email can't be empty")

    def signUp (self) :

        new_user_name = self.nameInputSignUp.text()
        new_user_email = self.emailInputSignUp.text()

        data = data = utils.dbReader.fetch_jsonDB()

        if new_user_name and new_user_email:

            if self.is_valid_email(new_user_email):

                # Check if the new user already exists
                if not utils.dbReader.user_exists(new_user_email, data):

                    utils.dbWriter.create_user(new_user_email, new_user_name)
                    self.errorTextSignUp.setText(
                        "New user added, you may login!")
                    self.emailInputLogin.setText(new_user_email)
                else:
                    self.errorTextSignUp.setText("User already exists.")
            else:
                self.errorTextSignUp.setText(
                    "This is not a valid email address!")

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
        self.selectProjectCombo.clear()
        self.selectSubjectCombo.clear()
        self.addSubjectOnProjectCombo.clear()
        self.projectDeleteCombo.clear()
        self.subjectDeleteCombo.clear()
        self.summaryTableValuesWidget.setRowCount(0)
        self.showSummarySubjectCombo.clear()

        # Display lists 
        self.displayRecipients()
        self.displayListsUI()

        # self.displayTrackingHistory()
        self.displayTrackingHistory()
        self.showSummarySubjectCombo.currentTextChanged.connect(
            self.displayTrackingHistory)

        self.addRecipientButton.clicked.connect(self.addRecipient)
        self.deleteRecipientButton.clicked.connect(self.deleteRecipient)

#######################################################################
#######################################################################
        self.addProjectButton.clicked.connect(self.addProject)
        # self.addProjectButton.clicked.connect(self.displayListsUI)

        self.addSubjectButton.clicked.connect(self.addSubject)
        # self.addSubjectButton.clicked.connect(self.displayListsUI)

        # self.selectProjectCombo.currentTextChanged.connect(self.displayListsUI)
        # self.projectDeleteCombo.currentTextChanged.connect(self.displayListsUI)


#######################################################################
#######################################################################

        self.projectDeleteButton.clicked.connect(self.removeProject)
        # self.projectDeleteButton.clicked.connect (self.updateListsUI)

        self.subjectDeleteButton.clicked.connect(self.removeSubject)
        # self.subjectDeleteButton.clicked.connect (self.displayListsUI)

        self.startPomodoroButton.clicked.connect(self.showPomodoroScreen)

        # self.selectProjectCombo.currentTextChanged.connect(self.displayListsUI)
        # self.projectDeleteCombo.currentTextChanged.connect(self.displayListsUI)

        # self.showSummaryProjectCombo.currentTextChanged.connect(self.displayListsUI)

        # self.showSummaryProjectCombo.currentTextChanged.connect (self.displayListsUI)

        self.projectDeleteCombo.currentTextChanged.connect(self.onListChange)
        self.selectProjectCombo.currentTextChanged.connect(self.onListChange)
        self.showSummaryProjectCombo.currentTextChanged.connect(
            self.onListChange)
        # self.showSummaryProjectCombo.currentTextChanged.connect(self.displaySubjectsLists)

    def displayTrackingHistory(self):

        # delete all rows
        self.summaryTableValuesWidget.setRowCount(0)

        which_project = self.showSummaryProjectCombo.currentText()
        which_subject = self.showSummarySubjectCombo.currentText()

        if which_project != "All" and which_subject != "All":

            data = utils.dbReader.fetch_jsonDB()
            # Get session details
            session_details = utils.dbReader.get_session_details(
                userEmail, which_project, which_subject, data)
            print("Session details:")
            for session in session_details:
                print(f"- StartTimestamp: {session['StartTimestamp']}")
                print(f"  EndTimestamp: {session['EndTimestamp']}")
                print(f"  CompletedTasks: {session['CompletedTasks']}")
                print(f"  UncompletedTasks: {session['UncompletedTasks']}")

                row_count = self.summaryTableValuesWidget.rowCount()
                self.summaryTableValuesWidget.setRowCount(row_count + 1)

                if isinstance(session['EndTimestamp'], float):
                    EndTimestamp = utils.formating.HourMinute12HoursFormat(
                        session['EndTimestamp'])

                else:

                    EndTimestamp = "N/A"

                # Add values to each cell in the new row
                a_item = QtWidgets.QTableWidgetItem(
                    utils.formating.DayMonthYear(session['StartTimestamp']))  # date
                b_item = QtWidgets.QTableWidgetItem(utils.formating.HourMinute12HoursFormat(
                    session['StartTimestamp']))  # starting time
                # end time   utils.formating.HourMinute12HoursFormat( session['EndTimestamp'])
                c_item = QtWidgets.QTableWidgetItem(EndTimestamp)
                d_item = QtWidgets.QTableWidgetItem(
                    ", ".join(session['CompletedTasks']))  # tasks True
                e_item = QtWidgets.QTableWidgetItem(
                    ", ".join(session['UncompletedTasks']))  # tasks False

                self.summaryTableValuesWidget.setItem(
                    row_count, 0, a_item)  # date
                self.summaryTableValuesWidget.setItem(
                    row_count, 1, b_item)  # starting time
                self.summaryTableValuesWidget.setItem(
                    row_count, 2, c_item)  # end time
                self.summaryTableValuesWidget.setItem(
                    row_count, 3, d_item)  # tasks True
                self.summaryTableValuesWidget.setItem(
                    row_count, 4, e_item)  # tasks False

    def updateSubjectsList(self):
        pass

    def showPomodoroScreen(self):
        global pomodoroProjectName, pomodoroSubjectName

        ProjectName = self.selectProjectCombo.currentText()
        SubjectName = self.selectSubjectCombo.currentText()

        if ProjectName != "" and SubjectName != "":
            pomodoroProjectName = ProjectName
            pomodoroSubjectName = SubjectName

            pomodoro_screen = PomodoroUI()
            widget.addWidget(pomodoro_screen)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def removeSubject(self):

        # Find the subject by name
        project_name = self.projectDeleteCombo.currentText()
        subject_name = self.subjectDeleteCombo.currentText()

        deleted = utils.dbWriter.delete_subject(
            userEmail, project_name, subject_name)

        if deleted is True:

            # delete the subject from all displayed lists in the UI

            index_to_remove = self.subjectDeleteCombo.findText(subject_name)
            if index_to_remove >= 0:
                self.subjectDeleteCombo.removeItem(index_to_remove)

            index_to_remove = self.selectSubjectCombo.findText(subject_name)
            if index_to_remove >= 0:
                self.selectSubjectCombo.removeItem(index_to_remove)

            index_to_remove = self.showSummarySubjectCombo.findText(
                subject_name)
            if index_to_remove >= 0:
                self.showSummarySubjectCombo.removeItem(index_to_remove)

    def addSubject(self):

        # Load the JSON file
        # data = utils.dbReader.fetch_jsonDB()

        project_name = self.addSubjectOnProjectCombo.currentText()
        new_subject_name = self.addSubjectInput.text()

        added = utils.dbWriter.add_subject(
            userEmail, project_name, new_subject_name)
        # print ("adddd:" , added)

        if added is True:
            self.errorTextSubjectLabel.setText("Added.")
            self.onListChange()

        elif project_name == "":
            self.errorTextSubjectLabel.setText(
                "Add a project first!")  # user have no projects yet

        else:
            self.errorTextSubjectLabel.setText("Already added!")

        # self.displayListsUI()

    def removeProject(self):

        project_name_to_delete = self.projectDeleteCombo.currentText()

        deleted = utils.dbWriter.delete_project(
            userEmail, project_name_to_delete)

        if deleted is True:

            index_to_remove = self.projectDeleteCombo.findText(
                project_name_to_delete)

            if index_to_remove >= 0:
                self.projectDeleteCombo.removeItem(index_to_remove)
                self.addSubjectOnProjectCombo.removeItem(index_to_remove)
                self.selectProjectCombo.removeItem(index_to_remove)
                self.showSummaryProjectCombo.removeItem(index_to_remove + 1)

            # self.displayListsUI()
            # self.projectDeleteCombo.addItem ("xxxx")

    def addProject(self):
        # print (self.addProjectInput.text() )

        # data = utils.dbReader.fetch_jsonDB()
        new_project_name = self.addProjectInput.text()

        add_project = utils.dbWriter.add_project(userEmail, new_project_name)

        if add_project == "Added":
            self.errorTextProjectLabel.setText("Added!")
            self.projectDeleteCombo.addItem(new_project_name)

            self.selectProjectCombo.addItem(new_project_name)
            self.showSummaryProjectCombo.addItem(new_project_name)
            self.addSubjectOnProjectCombo.addItem(new_project_name)

        else:
            # some error happened!
            self.errorTextProjectLabel.setText(add_project)

    def displayRecipients(self):

        data = utils.dbReader.fetch_jsonDB()
        recipients_list = utils.dbReader.get_user_recipients(userEmail, data)

        self.deleteRecipientCombo.clear()
        self.deleteRecipientCombo.addItems(recipients_list)

    def displayListsUI(self):

        self.selectProjectCombo.clear()
        self.addSubjectOnProjectCombo.clear()
        self.projectDeleteCombo.clear()
        self.selectSubjectCombo.clear()
        self.subjectDeleteCombo.clear()
        self.showSummaryProjectCombo.clear()

        self.showSummaryProjectCombo.addItem("All")

        # retrieve the list of projects for the user
        data = utils.dbReader.fetch_jsonDB()
        projects = utils.dbReader.get_user_projects(userEmail, data)

        # add the projects to the combo boxes
        for project in projects:
            self.selectProjectCombo.addItem(project)
            self.addSubjectOnProjectCombo.addItem(project)
            self.projectDeleteCombo.addItem(project)
            self.showSummaryProjectCombo.addItem(project)

        # retrieve the list of subjects for the currently selected project
        selected_project_name = self.selectProjectCombo.currentText()
        subjects_list = utils.dbReader.get_project_subjects(
            userEmail, selected_project_name, data)

        # add the subjects to the combo boxes
        for subject in subjects_list:
            self.selectSubjectCombo.addItem(subject)
            self.subjectDeleteCombo.addItem(subject)

    def onListChange(self):

        data = utils.dbReader.fetch_jsonDB()
        # retrieve the list of subjects for the currently selected project
        selected_project_name = self.selectProjectCombo.currentText()
        subjects_list = utils.dbReader.get_project_subjects(
            userEmail, selected_project_name, data)

        self.selectSubjectCombo.clear()
        self.selectSubjectCombo.addItems(subjects_list)

        ##############################################
        # data = utils.dbReader.fetch_jsonDB()
        selected_project_name = self.projectDeleteCombo.currentText()
        subjects_list = utils.dbReader.get_project_subjects(
            userEmail, selected_project_name, data)

        self.subjectDeleteCombo.clear()
        self.subjectDeleteCombo.addItems(subjects_list)
        ##############################################
        selected_project_name = self.showSummaryProjectCombo.currentText()

        subjects_list = utils.dbReader.get_project_subjects(
            userEmail, selected_project_name, data)

        self.showSummarySubjectCombo.clear()
        self.showSummarySubjectCombo.addItem("All")

        for subject in subjects_list:
            if subject != "All":
                self.showSummarySubjectCombo.addItem(subject)

        print("OnListChange is activated!")

    def updateListsUI(self):

        ###########################################################
        # Get the  subject name
        project_name = self.selectProjectCombo.currentText()

        data = utils.dbReader.fetch_jsonDB()
        list_of_subjects = utils.dbReader.get_project_subjects(
            userEmail, project_name, data)

        self.selectSubjectCombo.clear()

        # If the project was found, print the names of its subjects
        if list_of_subjects:
            for subject in list_of_subjects:
                self.selectSubjectCombo.addItem(subject)
        ###########################################################
        ###########################################################
        # Get the  subject names
        data = data = utils.dbReader.fetch_jsonDB()

        project_name = self.projectDeleteCombo.currentText()

        list_of_subjects = utils.dbReader.get_project_subjects(
            userEmail, project_name, data)

        self.subjectDeleteCombo.clear()

        if list_of_subjects:
            for subject in list_of_subjects:
                self.subjectDeleteCombo.addItem(subject)

    def is_valid_email(self, email_to_check):
        
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(email_pattern, email_to_check))


    def addRecipient (self) :

        addRecipient_email = self.addRecipientInput.text()

        if self.is_valid_email(addRecipient_email) : # If what the user typed is actually a valid email

            add = utils.dbWriter.add_recipient(userEmail, addRecipient_email)

            if add is True:
                self.errorTextRecipientsEmailLabel.setText("Added.")
                self.displayRecipients()  # update the GUI
            else:
                self.errorTextRecipientsEmailLabel.setText("Already added.")

        else:
            self.errorTextRecipientsEmailLabel.setText(
                "This is not a valid email address!")

    def deleteRecipient (self):

        recipientToDelete = self.deleteRecipientCombo.currentText()

        if recipientToDelete:

            do = utils.dbWriter.delete_Recipient(userEmail, recipientToDelete)

            if do is True:
                self.errorTextRecipientsEmailLabel.setText("Deleted!")

        self.displayRecipients()


pomodoro_count = 1


class PomodoroUI(QDialog):
    def __init__(self):
        super(PomodoroUI, self).__init__()
        loadUi("./UI/pomodoro.ui", self)
        global pomodoro_count

        self.goToMainMenuButton.clicked.connect(self.backtoHomeScreen)

        self.addTask.clicked.connect(self.addNewTask)

        self.doneButton.clicked.connect(self.saveSession)

        self.numberOfSession.setText(str(pomodoro_count))

        self.showTasksList()

        # pomodoro_count = 1

        self.startStopButton.clicked.connect(self.start_stop_timer)
        # Initialize the timer
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # each 1 second
        # run this fucntion  self.update_time
        self.timer.timeout.connect(self.update_time)
        self.remaining_time = QTime(0, 0, 3)  # 25 minutes QTime(0, 25, 0)

        # print (userEmail)

        # print (pomodoroProjectName, pomodoroSubjectName )

    def start_stop_timer(self):
        global pomodoro_count, pomodoro_currentTask

        # find out if no task is chosen first
        how_many_tasks = self.tasksCombo.count()
        if how_many_tasks == 0:
            pass
        else:
            pomodoro_currentTask = self.tasksCombo.currentText()
            print("starting with task: ", pomodoro_currentTask)
            if self.timer.isActive():
                self.timer.stop()
                self.startStopButton.setText("Start")
                # Finished the 1st pomodoro
                # pomodoro_count += 1

            else:
                # Re-initialize remaining_time to the correct value
                # 25 minutes QTime(0, 25, 0)
                self.remaining_time = QTime(0, 0, 3)
                self.timer.start()
                self.startStopButton.setText("Stop")

    def update_time(self):
        global pomodoro_count
        self.remaining_time = self.remaining_time.addSecs(-1)

        if self.remaining_time.minute() == 0 and self.remaining_time.second() == 0:

            if pomodoro_count == 4:
                print("Time for LOOOONG BREAK!!!!!!")
                pomodoro_count = 1

                UI = LongBreakUI()
                widget.addWidget(UI)
                widget.setCurrentIndex(widget.currentIndex()+1)

            else:
                self.timer.stop()
                self.startStopButton.setText("Start")
                # Finished a pomodoro
                pomodoro_count += 1
                self.numberOfSession.setText(str(pomodoro_count))

                take_short_break = ShortBreakUI()
                widget.addWidget(take_short_break)
                widget.setCurrentIndex(widget.currentIndex()+1)

        self.timeLabel.setText(self.remaining_time.toString("mm:ss"))

    def addNewTask(self):

        new_task_name = self.taskInput.text()

        if new_task_name != "":

            data = utils.dbReader.fetch_jsonDB()
            task_list = utils.dbReader.get_subject_task_names(
                userEmail, pomodoroProjectName, pomodoroSubjectName, data)

            if new_task_name in task_list:
                print("task name alredy there!")
            else:

                utils.dbWriter.add_task(
                    userEmail, pomodoroProjectName, pomodoroSubjectName, new_task_name)
                self.tasksCombo.addItem(new_task_name)
                self.tasksCombo_2.addItem(new_task_name)

    def showTasksList(self):

        data = utils.dbReader.fetch_jsonDB()
        task_list = utils.dbReader.get_subject_task_names(
            userEmail, pomodoroProjectName, pomodoroSubjectName, data)

        self.tasksCombo.addItems(task_list)
        self.tasksCombo_2.addItems(task_list)

    def saveSession(self):
        global pomodoro_currentTask
        # pomodoroProjectName
        # pomodoroSubjectName
        # pomodoro_currentTask

        if pomodoro_currentTask is None:
            pass
        else:
            utils.dbWriter.mark_task_as_completed(
                userEmail, pomodoroProjectName, pomodoroSubjectName, pomodoro_currentTask)

            UI = MainMenuUI()
            widget.addWidget(UI)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def backtoHomeScreen(self):

        home_screen = MainMenuUI()
        widget.addWidget(home_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)


class ShortBreakUI(QDialog):
    def __init__(self):
        super(ShortBreakUI, self).__init__()
        loadUi("./UI/shortBreak.ui", self)

        self.goToMainMenuButton.clicked.connect(self.backtoHomeScreen)

        self.startButton.clicked.connect(self.start_stop_timer)
        # Initialize the timer
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # each 1 second
        # run this fucntion  self.update_time
        self.timer.timeout.connect(self.update_time)
        self.remaining_time = QTime(0, 0, 3)  # 25 minutes QTime(0, 25, 0)

    def start_stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.startButton.setText("Start")
            # Finished the 1st pomodoro
            # self.pomodoro_count += 1

        else:
            # Re-initialize remaining_time to the correct value
            self.remaining_time = QTime(0, 0, 3)  # 25 minutes QTime(0, 25, 0)
            self.timer.start()
            self.startButton.setText("Stop")

    def update_time(self):
        self.remaining_time = self.remaining_time.addSecs(-1)

        if self.remaining_time.minute() == 0 and self.remaining_time.second() == 0:

            self.timer.stop()
            self.startButton.setText("Start")
            # Finished a short break
            UI = PomodoroUI()
            widget.addWidget(UI)
            widget.setCurrentIndex(widget.currentIndex()+1)

            # PomodoroUI()
            # widget.addWidget(back_to_pomodoro_screen)
            # widget.setCurrentIndex(widget.currentIndex()+1)

        self.timeLabel.setText(self.remaining_time.toString("mm:ss"))

    def backtoHomeScreen(self):
        home_screen = MainMenuUI()
        widget.addWidget(home_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)


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
