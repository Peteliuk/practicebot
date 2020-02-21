# practicebot
## Telegram bot with Django back-end

### Description:
This is task-manager telegram bot, created by [*Liubomyr Peteliuk*](https://github.com/Peteliuk) as practice project for [*BVBlogic*](https://bvblogic.com/).

Versions:
* Python version: 3.8.1
* Django version: 3.0.2
* pyTelegramBotApi: 3.6.7

### Installation
Before using project you must have install some modules:
* [**virtualenv**](https://pypi.org/project/virtualenv/) (optionaly, but recommended)
* [**Python**](https://www.python.org/downloads/) (necessarily, last version recommended)
* [**pip**](https://pip.pypa.io/en/stable/installing/) (necessarily, last version recommended)
* [**pyTelegramBotApi**](https://pypi.org/project/pyTelegramBotAPI/) (necessarily, last version necessarily)
* [**Django**](https://pypi.org/project/Django/) (necessarily, last version recommended)
* [**Django Rest Framework**](https://pypi.org/project/djangorestframework/) (necessarily for this project)

### Usage:
Download this project by `git clone` command in your terminal or download it from this page and extract it.
1. (optionaly, but highly recommended) Activate your virtual enviorement;
2. In terminal open project folder and type `manage.py` to see if it works (on linux: `python3 manage.py`);
3. If no errors, type `pip install -r requirements.txt` (on linux: `python3 pip install -r requirements.txt`);
4. Type `manage.py createsuperuser` to create admin (on linux: `python3 manage.py createsuperuser`);
5. To run project, type `manage.py runserver` (on linux `python3 manage.py runserver`);
6. Open this URL in your browser: `localhost:8000/admin`;
7. To run bot, open new terminal window and type `manage.py runbot` (on linux: `python3 manage.py runbot`);
8. Enjoy this s@@t :)

#### This project is under development!

**Now you can:** 
* create user from admin panel
* sign in from telegram bot
* create tasks for users and change its information
* see tasks from telegram bot and accept or reject them