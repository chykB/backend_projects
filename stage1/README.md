# Django Weather Greeting API
This Django project provides an API endpoint that greets visitors based on their location and provides current weather information.

## Features
* Get visitor's IP address and location using IP-API.
* Fetches current weather data based on the visitor's location using OpenWeatherMap API.
* Serializes and returns a JSON response with greeting, location, and temperature information.

## Technologies Used
* Python 3
* Django
* Requests library for API calls
* PythonAnywhere for deployment

## Prerequisites
* Python 3.x installed on your system.
* Python virtual environment

## Usage
### Access the API endpoint:
    * Base URL: https://chyka.pythonanywhere.com/api/hello
    * Query Parameters: visitor_name (optional)
    * Example: https://chyka.pythonanywhere.com/api/hello?visitor_name=John