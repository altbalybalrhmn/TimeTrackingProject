import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

############################
global db_filename
db_filename = 'db.json'
############################


def fetch_jsonDB():
    """Reads the json file and returns its contents."""
    with open(db_filename, 'r') as f:
        return json.load(f)


# fetch_jsonDB
# read_json


def user_exists(email, data):
    """Checks if a user with a specific email exists in the database."""
    for user in data['PomodorosApp']['Users']:
        if user['Email'] == email:
            return True
    return False


def get_username_from_email(email, data):
    # return user's email
    for user in data['PomodorosApp']['Users']:
        if user['Email'] == email:
            return user['Name']
    return False


def get_user_projects(email, data=fetch_jsonDB()):
    """Returns a list of a user's projects."""
    for user in data['PomodorosApp']['Users']:
        if user['Email'] == email:
            return [project['ProjectName'] for project in user['Projects']]
    return []


def get_project_subjects(email, project_name, data=fetch_jsonDB()):
    """Returns a list of subjects under a specific project for a user."""
    for user in data['PomodorosApp']['Users']:
        if user['Email'] == email:
            for project in user['Projects']:
                if project['ProjectName'] == project_name:
                    return [subject['SubjectName'] for subject in project['Subjects']]
    return []


def get_subject_total_time(email, project_name, subject_name, data):
    """Returns the total tracked time for a specific subject."""
    for user in data['PomodorosApp']['Users']:
        if user['Email'] == email:
            for project in user['Projects']:
                if project['ProjectName'] == project_name:
                    for subject in project['Subjects']:
                        if subject['SubjectName'] == subject_name:
                            return int(subject['SubjectTotalTrackedTime'])
    return 0


def get_subject_task_names(email, project_name, subject_name, data):
    """Returns the task names for each task under a specific subject."""
    for user in data['PomodorosApp']['Users']:
        if user['Email'] == email:
            for project in user['Projects']:
                if project['ProjectName'] == project_name:
                    for subject in project['Subjects']:
                        if subject['SubjectName'] == subject_name:
                            return [task['TaskName'] for session in subject['PomodoroSessions'] for task in session['Tasks']]
    return []


def get_user_recipients(email, data=fetch_jsonDB()):
    """Returns a list of a user's recipients."""
    for user in data['PomodorosApp']['Users']:
        if user['Email'] == email:
            return user['Recipients']
    return []


def get_project_total_time(email, project_name, data):
    """Returns the total tracked time for a specific project."""
    for user in data['PomodorosApp']['Users']:
        if user['Email'] == email:
            for project in user['Projects']:
                if project['ProjectName'] == project_name:
                    return int(project['ProjectTotalTrackedTime'])
    return 0


def is_task_completed(email, project_name, subject_name, task_name, data):
    """Returns True if a specific task is marked as completed, and False otherwise."""
    for user in data['PomodorosApp']['Users']:
        if user['Email'] == email:
            for project in user['Projects']:
                if project['ProjectName'] == project_name:
                    for subject in project['Subjects']:
                        if subject['SubjectName'] == subject_name:
                            for session in subject['PomodoroSessions']:
                                for task in session['Tasks']:
                                    if task['TaskName'] == task_name:
                                        return task['Completed'] == 'True'
    return False


def get_session_details(email, project_name, subject_name, data):
    """Returns details about each PomodoroSession for a specific subject."""
    for user in data['PomodorosApp']['Users']:
        if user['Email'] == email:
            for project in user['Projects']:
                if project['ProjectName'] == project_name:
                    for subject in project['Subjects']:
                        if subject['SubjectName'] == subject_name:
                            session_details = []
                            for session in subject['PomodoroSessions']:
                                completed_tasks = [
                                    task['TaskName'] for task in session['Tasks'] if task['Completed'] == 'True']
                                uncompleted_tasks = [
                                    task['TaskName'] for task in session['Tasks'] if task['Completed'] != 'True']
                                session_details.append({
                                    'StartTimestamp': session['StartTimestamp'],
                                    'EndTimestamp': session['EndTimestamp'],
                                    'CompletedTasks': completed_tasks,
                                    'UncompletedTasks': uncompleted_tasks
                                })
                            return session_details
    return []


def sendSummaryEmail(emailTable, recipients):

    # recipients

    emailList = recipients  # ['@ddd']

    with open('UI/email-template.html', 'r') as f:
        html_body = f.read()

    # Replace the "{pomodoro}" in the html
    html_body = html_body.replace('{pomodoro}', emailTable)

    msg = MIMEMultipart()
    msg['Subject'] = 'PomodoroApp - Summary Report'
    msg['From'] = 'PomodoroApp-Group3 <report@PomodoroApp.com>'
    msg['To'] = ', '.join(emailList)

    body = MIMEText(html_body, 'html')
    msg.attach(body)

    # using sendinblue instead of google SMTP
    with smtplib.SMTP('smtp-relay.sendinblue.com', 587) as smtp:
        smtp.starttls()
        smtp.login('pomodoro250530@gmail.com', '2zPrxDQYZk1GgqBt')
        smtp.send_message(msg)


##########################################################
##########################################################
# Reading data
##########################################################
##########################################################


# data = read_json('db.json')


# # Check if user exists
# if user_exists('ramy@ramy.nl', data):
#     print('User exists!')
# else:
#     print('User does not exist.')

# # Get user's recipients
# recipients = get_user_recipients('ramy@ramy.nl', data)
# print(f"User's recipients: {recipients}")

# # Get user's projects
# projects = get_user_projects('ramy@ramy.nl', data)
# print(f"User's projects: {projects}")

# # Get project total tracked time
# total_time = get_project_total_time('ramy@ramy.nl', 'Project01', data)
# print(f"Total tracked time for Project01: {total_time}")


# # Get project subjects
# subjects = get_project_subjects('ramy@ramy.nl', 'Project01', data)
# print(f"Project subjects: {subjects}")

# # Get subject total tracked time
# total_time = get_subject_total_time(
#     'ramy@ramy.nl', 'Project01', 'Subject01', data)
# print(f"Total tracked time for Subject01: {total_time}")

# # Get subject task names
# task_names = get_subject_task_names(
#     'ramy@ramy.nl', 'Project01', 'Subject01', data)
# print(f"Task names for Subject01: {task_names}")

# # Check if task is completed
# completed = is_task_completed(
#     'ramy@ramy.nl', 'Project01', 'Subject01', 'Task01', data)
# print(f"Is Task01 completed? {completed}")

# data = read_json('db.json')
# # Get session details
# session_details = get_session_details(
#     'ramy@ramy.nl', 'Project01', 'Subject01', data)
# print("Session details:")
# for session in session_details:
#     print(f"- StartTimestamp: {session['StartTimestamp']}")
#     print(f"  EndTimestamp: {session['EndTimestamp']}")
#     print(f"  CompletedTasks: {session['CompletedTasks']}")
#     print(f"  UncompletedTasks: {session['UncompletedTasks']}")
