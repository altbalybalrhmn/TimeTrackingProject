import json
import time
import utils.dbReader

############################
global db_filename
db_filename = 'db.json'
############################


def load_data():

    return utils.dbReader.fetch_jsonDB()
    # with open(db_filename, 'r') as f:
    #    return json.load(f)


def save_data(data):
    with open(db_filename, 'w') as f:
        json.dump(data, f)


def create_user(email, name):
    data = load_data()
    new_user = {
        "Email": email,
        "Name": name,
        "Recipients": [email],
        "Projects": []
    }
    data["PomodorosApp"]["Users"].append(new_user)
    save_data(data)


def add_project(user_email, project_name):

    data = load_data()
    user = next((u for u in data["PomodorosApp"]
                ["Users"] if u["Email"] == user_email), None)
    if user is None:
        return (f"No user found with email {user_email}")
    elif any(p["ProjectName"] == project_name for p in user["Projects"]):
        return (f"Already exists.")
    elif project_name == "":
        return ("invalid entry")
    else:
        new_project = {
            "ProjectName": project_name,
            "ProjectTotalTrackedTime": "0",
            "Subjects": []
        }
        user["Projects"].append(new_project)
        save_data(data)
        return "Added"


def delete_project(user_email, project_name):
    data = load_data()
    user = next((u for u in data["PomodorosApp"]
                ["Users"] if u["Email"] == user_email), None)
    if user is None:
        return (f"No user found with email {user_email}")
    else:
        projects = user["Projects"]
        project_index = next((i for i, p in enumerate(
            projects) if p["ProjectName"] == project_name), None)
        if project_index is None:
            return False  # (f"No project found with name {project_name}")
        else:
            projects.pop(project_index)
            save_data(data)
            return True  # "Deleted"


def add_recipient(userEmail, recipientEmail):

    data = load_data()

    for user in data["PomodorosApp"]["Users"]:
        if user['Email'] == userEmail:
            if recipientEmail in user['Recipients']:
                return False
            else:
                user['Recipients'].append(recipientEmail)
                save_data(data)
                return True

    for user in data["PomodorosApp"]["Users"]:
        if user["Email"] == userEmail:
            user["Recipients"].remove(email_to_remove())
            break


def add_subject(user_email, project_name, subject_name):
    data = load_data()
    user = next((u for u in data["PomodorosApp"]
                ["Users"] if u["Email"] == user_email), None)
    if user is None:
        exit(f"No user found with email {user_email}")

    project = next((p for p in user["Projects"]
                   if p["ProjectName"] == project_name), None)

    if project is None:
        return False  # (f"No project found with name {project_name}")
    else:
        for subject in project["Subjects"]:
            if subject["SubjectName"] == subject_name:
                return ("subject already exists")
            elif subject_name == "":
                return ("invalid entry")
            else:
                new_subject = {
                    "SubjectName": subject_name,
                    "SubjectTotalTrackedTime": "0",
                    "PomodoroSessions": []
                }
                project["Subjects"].append(new_subject)
                save_data(data)
                return True


def delete_subject(user_email, project_name, subject_name):
    data = load_data()
    user = next((u for u in data["PomodorosApp"]
                ["Users"] if u["Email"] == user_email), None)
    if user is None:
        exit(f"No user found with email {user_email}")

    project = next((p for p in user["Projects"]
                   if p["ProjectName"] == project_name), None)

    if project is None:
        return False  # (f"No project found with name {project_name}")

    subjects = project["Subjects"]
    subject_index = next((i for i, s in enumerate(
        subjects) if s["SubjectName"] == subject_name), None)
    if subject_index is None:
        return False
    else:
        subjects.pop(subject_index)
        save_data(data)
        return True


def add_task(user_email, project_name, subject_name, task_name, completed="False"):
    data = load_data()
    user = next((u for u in data["PomodorosApp"]
                ["Users"] if u["Email"] == user_email), None)
    if user is None:
        raise ValueError(f"No user found with email {user_email}")
    project = next((p for p in user["Projects"]
                   if p["ProjectName"] == project_name), None)
    if project is None:
        raise ValueError(f"No project found with name {project_name}")
    subject = next(
        (s for s in project["Subjects"] if s["SubjectName"] == subject_name), None)
    if subject is None:
        raise ValueError(f"No subject found with name {subject_name}")

    new_task = {
        "TaskName": task_name,
        "Completed": completed
    }
    last_session = subject["PomodoroSessions"][-1] if len(
        subject["PomodoroSessions"]) > 0 else None
    if last_session is None or last_session["EndTimestamp"] is not None:
        new_session = {
            "StartTimestamp": str(time.time()),
            "EndTimestamp": None,
            "Tasks": [new_task]
        }
        subject["PomodoroSessions"].append(new_session)
    else:
        last_session["Tasks"].append(new_task)
    save_data(data)


def mark_task_as_completed(email, project_name, subject_name, task_name):
    data = load_data()

    for user in data["PomodorosApp"]["Users"]:
        if user["Email"] == email:
            for project in user["Projects"]:
                if project["ProjectName"] == project_name:
                    for subject in project["Subjects"]:
                        if subject["SubjectName"] == subject_name:
                            for session in subject["PomodoroSessions"]:
                                for task in session["Tasks"]:
                                    if task["TaskName"] == task_name:
                                        task["Completed"] = "True"
                                        session["EndTimestamp"] = time.time()

                                        save_data(data)

                                        return True


def mark_task_as_NOTcompleted(email, project_name, subject_name, task_name):
    data = load_data()

    for user in data["PomodorosApp"]["Users"]:
        if user["Email"] == email:
            for project in user["Projects"]:
                if project["ProjectName"] == project_name:
                    for subject in project["Subjects"]:
                        if subject["SubjectName"] == subject_name:
                            for session in subject["PomodoroSessions"]:
                                for task in session["Tasks"]:
                                    if task["TaskName"] == task_name:
                                        task["Completed"] = "False"
                                        session["EndTimestamp"] = None

                                        save_data(data)

                                        return True


def delete_Recipient(userEmail, email_to_remove):
    # Read JSON data from file

    data = load_data()

    for user in data["PomodorosApp"]["Users"]:
        if user["Email"] == userEmail:
            user["Recipients"].remove(email_to_remove)
            break

    # Write the modified JSON data back to the file
    save_data(data)

    return True
