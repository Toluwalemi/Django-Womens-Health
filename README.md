# `Women's Health` service

`Women's health` service is a Python library that estimate a woman’s period cycles within a specific timeframe and 
determine what period of a monthly cycle the lady is currently in.

## RESTFUL ROUTES
```text
|Endpoint                   |HTTP Method   |CRUDMethod   |Result   |
|---------------------------|--------------|-------------|---------|
|api/create-cycle           |    POST      |     CREATE  | add period cycle data
|api/create-cycle/:id       |    PUT       |     UPDATE  | update data
|api/cycle-event/?date=date |    GET       |     READ    | get cycle event
```
## Requirements
```text
djangorestframework==3.12.4
Django==3.2.8
pytest-django==4.4.0
pytest==6.2.4
```

## Structure
A brief overview of project structure
```text
├── config
│   │── settings.py
│   │── urls.py
├── api
│   ├── helpers
│   ├── tests
│   │   ├── test_foo.py
│   │   ├── api
│   │       ├── test_period_cycle_view.py
│   │       ├── test_cycle_events_view.py
│   ├── helpers.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
├── .README.md
├── .requirements.txt
```

## General Usage

* Clone the repository
* Create a virtual environment in the folder. (If you are on linux, use the command below):
```bash
 python3.9 -m venv venv
```
* Activate the virtual environment (If you are on linux, use the command below):
```bash
 source venv/bin/activate
```
* Install the requirements:
```bash
 pip install -r requirements.txt
```
* Make migrations:
```bash
 python manage.py makemigrations api
 python manage.py migrate
```
* Set the pytest environment in your terminal:
```bash
 export DJANGO_SETTINGS_MODULE=config.settings
```
* Run the command below to run the tests
```
 pytest
```
* Run the DJANGO's server and access the endpoints
```
 python manage.py runserver
```
