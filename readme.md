## How to install

1. Install python3, pip and postgresql. Make sure to install python3-dev as well.
2. It's good to have virtualenv installed to isolate the environment. To install virtualenv, refer to [this link](https://www.pythoncentral.io/how-to-install-virtualenv-python/).
3. Install all requirements in the requirements.txt by typing "pip install requirements.txt"
4. Modify SQLALCHEMY_DATABASE_URI with postgresql URL, username andpassword. Then set BASE_URL with base url.
5. After all requirements are set, set environment variable by "export FLASK_CONFIG=development"
6. Upgrade DB by "python3 migrate.py db upgrade"
7. Run the app by "python3 run.py"