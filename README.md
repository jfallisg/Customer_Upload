# Customer Upload

## Overview
  - A web app allowing `.tsv` file upload via form submission of new/updated customer subscriber data, ingested in to a MySQL database for analysis and reporting.
  - Built in Flask
  - Boilerplate based on CoreyMSchafer's Flask tutorials: https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog

## Project Installation

### Prerequisites

This procedure assumes you have the following already installed on your machine:
  - python3
  - pip
  - virtualenv
  - mysql

### Install Python dependencies

```bash
// from the root project directory
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

#### Create the database for the webapp
```bash
mysql -u<username> -p
mysql> CREATE DATABASE customers;
quit

python3
python> from customerupload import db
python> db.create_all()
quit()
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
