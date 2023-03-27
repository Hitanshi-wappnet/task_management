# Task Management

Task management is used to manage tasks.

## Requirements

To run this files makes sure Python, Python-Django, django REST Framework and environ installed first. To install them use following command.

```bash
pip install -r requirements.txt
```

## Features

1. This app contains  authentication API in which User can register, login , forget password, set new password API using Token authentication.

2. There are 2 types of users-Employee and Manager. Only Manager can add , update and delete task and Employee can View Task.

3. API available are Add Task, Update Task, Delete Task For Managers.

4. Employee can view Task using ViewTask API.

5. Employee can serach Task by title.

6. Manager can assign Task for Employees.

7. Employee receives notification via email whenever Task is added or updated.

## Quick Start

1. Run ``python manage.py migrate`` to migrate tables.

2. Run this files using ``python manage.py runserver`` command.
