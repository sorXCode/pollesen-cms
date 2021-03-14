# FLASK USER MANAGEMENT APP

## Create and Activate Virtual Environment

```shell
python3 -m venv venv
source venv/bin/activate
```

## Install dependencies

```shell
pip install -r requirements.txt
```

## Database Requirement

PostgreSQL database url should be specified in the `.env` file
If the url is absent, Sqlite3 would be used

NOTE: To run website, create a local `.env` file from the `.env.example` file at the application root.

### Run application

```shell
export FLASK_APP=app
flask run
```

### Endpoints

```txt
Admin/Management: /cms
All contents: /contents
Content details: /contents/<content_id: int>
```

### **ps: Perform databases migration**

To run application for the first time, perform database migration using the commands below at the root folder

```shell
flask db init
flask db migrate
flask db upgrade
```
