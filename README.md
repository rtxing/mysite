# Interview Project

An example of Django project with basic user and items cart functionality.

## Functionality

- Log in
    - via username & password
    - via email & password
    - via email or username & password
    - with a remember me checkbox (optional)
- Create an account
- Log out
- Profile activation via email
- Reset password
- Change password
- Change email
- Change profile
- Show Items
- Show Summary


## Installing

### Clone the project

```bash
git clone https://github.com/rtxing/mysite.git
cd mysite
```

### Install dependencies & activate virtualenv

#### Create a virtualenv using conda (optional)

```bash
pip3 install virtualenv
export PATH=$PATH:~/.local/bin
virtualenv -p python3 my_virtual_env
cd my_virtual_env
source bin/activate
```

#### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure the settings (connection to the database, connection to an SMTP server, and other options)

1. Edit `mysite/mysite/conf/development/settings.py` if you want to develop the project.

2. Edit `mysite/mysite/conf/production/settings.py` if you want to run the project in production.

### Apply migrations

```bash

python3 mysite/manage.py makemigrations
python3 mysite/manage.py migrate
```

### Collect static files (only on a production server)

```bash
python3 mysite/manage.py collectstatic
```

### Running

#### A development server

Just run this command:

```bash
python3 mysite/manage.py runserver
```

#### Live demo

The application can be viewed at : http://rtrao9999.pythonanywhere.com/

Login email.com : hh@gg.com
Password : zxcvbnm99