# Customer Upload

## Overview
  - A web app allowing `.tsv` file upload via form submission of new/updated customer subscriber data, ingested in to a MySQL database for analysis and reporting.
  - Built with Python, Flask, MySQL
  - Boilerplate based on CoreyMSchafer's Flask tutorials: https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog

## Screenshots
![Main Page Screenshot](https://user-images.githubusercontent.com/1594436/52749524-6ca84b00-2fb7-11e9-95fa-6ceb2e2cfd16.png "Main Page Screenshot")
![Completed Text Screenshot](https://user-images.githubusercontent.com/1594436/52749523-6ca84b00-2fb7-11e9-8df8-078c2ac97b26.png "Completed Text Screenshot")

## Database Schema
![Database Schema](https://user-images.githubusercontent.com/1594436/52749985-e260e680-2fb8-11e9-9d4c-d738de1fb802.png "Database Schema")

## Project Installation

### Prerequisites

This procedure assumes you have the following already installed on your machine:
  - python3
  - pip
  - virtualenv
  - mysql

### Install Python dependencies

```bash
# from the root project directory
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

### Get the database running

#### Make a user for the webapp
```bash
mysql -uroot -p
mysql> CREATE USER '<username>'@'localhost' IDENTIFIED BY '<password>';
mysql> GRANT ALL PRIVILEGES ON *.* TO '<username>'@'localhost' WITH GRANT OPTION;
quit
```

#### Create the database
```bash
mysql -u<username> -p
mysql> CREATE DATABASE customers;
quit
```

#### Create all the tables
```
# you need to be in the root project directory
mysql -u<username> customers < db_install.sql
```

#### Modify local environment config

`./customerupload/config.py` assumes you have environment variables set for:
  - `SECRET_KEY`
  - `SQLALCHEMY_DATABASE_URI`

Set them like this:

```bash
# generate a SECRET_KEY for Flask config
python3
import secrets
secrets.token_hex(16)
# copy result
quit()

# edit bash config
nano ~/.bash_profile
# append these two lines
export SECRET_KEY="<copied_hex"
export SQLALCHEMY_DATABASE_URI="mysql://<username>:<password>@localhost/customers"
```

### Run the Flask python server

```bash
python run.py
```

## Using the Webapp

Visit `https://localhost:5000/` on your web browser.
