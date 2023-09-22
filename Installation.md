# Installation the Application

### Clone or Download code from Github

You can clone the repository using this command:
   ``` 
   git clone https://github.com/thorungb/ku-polls.git
   ```

### Create a virtual environment and install dependencies
1. Change directory to KU Polls:
   ``` 
   cd ku-polls
   ```
2. Create a virtual environment by running the following command:
   ``` 
   python -m venv venv
   ```
3. Activate the virtual environment
   * On Windows:
        ``` 
        venv\Scripts\activate
        ```
    * On macOS and Linux:
        ``` 
        source venv/bin/activate
        ```
4. Install Dependencies for required python modules:
    ``` 
    pip install -r requirements.txt
    ```
### Set values for externalized variables
Create the .env by copying the sample.env
* On Windows:
  ``` 
  copy sample.env .env
  ```
* On macOS and Linux:
  ``` 
  cp sample.env .env
  ```
### Run migrations
Run migrations to apply database migrations:
  ``` 
  python manage.py migrate
  ```

### Run tests
Run tests to verify the correctness of the above installations:
  ``` 
  python manage.py test
  ```
### Install data from the data fixtures
  ``` 
  python manage.py loaddata data/users.json data/polls.json
  ```

More detailt of how to running the application is in [readme.md](README.md)