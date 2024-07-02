# Weather Greeting App

This is a Django-based web application that provides a personalized greeting along with the current weather information based on the user's IP address.

## Features

- Personalized greeting message.
- Current temperature based on the user's location.


## Prerequisites

- Python 3.7 or higher
- Django 5.0.6
- Gunicorn 22.0.0
- Clever Cloud account for deployment

## Live server
## URL https://ancestor.cleverapps.io/
## [GET] https://ancestor.cleverapps.io/api/greeting?your_name=YOUR_NAME

## Installation and Running Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/waveGuide1/hello-api-app.git
   cd hello-api
   ```
## Create and activate a virtual environment:
```
   python3 -m venv venv
   source venv/bin/activate # Might differ for window os
   ```
## Install the dependencies:
```
   pip install -r requirements.txt
   ```
## Create a .env file in the root directory of your project and add the following variables:
```
OPENWEATHER_API_KEY=YOUR_API_KEY
```
## Apply the migrations and run the server:
```
python manage.py migrate
python manage.py runserver
```
## Run the App locally
```
[GET] http://localhost:8080/api/greeting?your_name=YOUR_NAME
```

   
   