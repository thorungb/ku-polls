# KU Polls: Online Survey Questions
An application for conducting a poll or survey with multiple-choice questions, written in Python using Django. It is based on the [Django tutorial project](https://docs.djangoproject.com/en/4.1/intro/tutorial01/), and adds additional functionality.

A polls application for [Individual Software Process](https://cpske.github.io/ISP) course at [Kasetsart University](https://ku.ac.th).

## Requirements

Required Python and Django packages are listed in [requirements.txt](./requirements.txt). 

## Install and Configure the Application

See [Installation](../../wiki/Installation) in the project wiki.


## Running the Application

1. Start the server in the virtual environment. 
   ```
   # activate the virtualenv for this project. On Linux or MacOS:
   source env/bin/activate
   # on MS Windows:
   env\Scripts\activate

   # start the django server
   python3 manage.py runserver
   ```
   This starts a web server listening on port 8000.

2. You should see this message printed in the terminal window:
   ```
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.
   ```
   If you get a message that the port is unavailable, then run the server on a different port (1024 thru 65535) such as:
   ```
   python3 manage.py runserver 12345
   ```

3. In a web browser, navigate to <http://localhost:8000>

4. To stop the server, press CTRL-C in the terminal window. Exit the virtual environment by closing the window or by typing:
   ```
   deactivate
   ```

## Demo User Accounts

Sample polls and user data are included. 

* `admin` password `adminadmin`

## Project Documents

All project-related documents are in the [Project Wiki](https://github.com/thorungb/ku-polls/wiki)

- [Vision Statement](https://github.com/thorungb/ku-polls/wiki/Vision-Statement)
- [Requirements](https://github.com/thorungb/ku-polls/wiki/Requirements)
- [Development Plan](https://github.com/thorungb/ku-polls/wiki/Development-Plan)
- [Iteration 1 Plan](https://github.com/thorungb/ku-polls/wiki/Iteration-1-Plan)
- [Task Board](https://github.com/users/thorungb/projects/6)
