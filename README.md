[![Django application](https://github.com/thorungb/ku-polls/actions/workflows/django-app.yml/badge.svg?branch=main)](https://github.com/thorungb/ku-polls/actions/workflows/django-app.yml)
## KU Polls: Online Survey Questions
An application for conducting a poll with multiple-choice questions, written in Python using Django. It is based on the [Django tutorial project](https://docs.djangoproject.com/en/4.1/intro/tutorial01/), and adds additional functionality.

A polls application for [Individual Software Process](https://cpske.github.io/ISP) course at [Kasetsart University](https://ku.ac.th).

## Requirements

Required Python and Django packages are listed in [requirements.txt](./requirements.txt). 

## Installation the Application
Read and follow the instructions in [Installation the Application](Installation.md).

## Running the Application

1. Start the server in the virtual environment. <br>
  Activate the virtualenv for this project
   * On Windows:
   ``` 
   venv\Scripts\activate
   ```
   * On macOS and Linux:
   ``` 
   source venv/bin/activate
   ```
   Start the django server:
   ```
   python manage.py runserver
   ```
   This starts a web server listening on port 8000.

2. You should see this message printed in the terminal window:
   ```
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.
   ```
   If you get a message that the port is unavailable, then run the server on a different port (1024 thru 65535) such as:
   ```
   python manage.py runserver 12345
   ```

2. In a web browser, navigate to <http://localhost:8000>

3. To stop the server, press CTRL-C in the terminal window. Exit the virtual environment by closing the window or by typing:
   ```
   deactivate
   ```

## Demo User Accounts

Sample polls and user data are included.

### Admin Account

* `admin` password `adminadmin`

### User Accounts
* `harry` password `hackme22`
* `jane` password `janejane`

## Project Documents

All project-related documents are in the [Project Wiki](https://github.com/thorungb/ku-polls/wiki)

- [Vision Statement](https://github.com/thorungb/ku-polls/wiki/Vision-Statement)
- [Requirements](https://github.com/thorungb/ku-polls/wiki/Requirements)
- [Development Plan](https://github.com/thorungb/ku-polls/wiki/Development-Plan)
- [Iteration 1 Plan](https://github.com/thorungb/ku-polls/wiki/Iteration-1-Plan)
- [Iteration 2 Plan](https://github.com/thorungb/ku-polls/wiki/Iteration-2-Plan)
- [Iteration 3 Plan](https://github.com/thorungb/ku-polls/wiki/Iteration-3-Plan)
- [Task Board](https://github.com/users/thorungb/projects/6)
