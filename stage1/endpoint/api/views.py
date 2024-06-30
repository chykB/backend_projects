from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .serializers import GreetingSerializer
import requests

# Create your views here.

OPENWEATHER_API_KEY = "727ccf37ec07d9c535a70e5d5f6914dd"
@require_GET
def hello(request):
    visitor_name = request.GET.get("visitor_name", "Guest")
    client_ip = request.META.get("REMOTE_ADDR")
    if client_ip == '127.0.0.1':
        client_ip = '8.8.8.8'
    location_response = requests.get(f'http://ip-api.com/json/{client_ip}')
    if location_response.status_code==200:
        location_data = location_response.json()
        print(location_data)
        city = location_data.get("city", "Unknown")
        lat = location_data.get('lat', None)
        lon = location_data.get('lon', None)
    else:
        city = "Unknown"
        lat, lon = None, None

    if lat is not None and lon is not None:
        weather_response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={OPENWEATHER_API_KEY}')
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            temperature = weather_data['main']['temp']
        else:
            temperature = 'Unknown'
    else:
        temperature = 'Unknown'



    data = {
        "client_ip": client_ip,
        "location": city,
        "greeting": f"Hello {visitor_name}! the temperature is {temperature} degree Celsius in the {city}"

    }
    serializer = GreetingSerializer(data=data)
    if serializer.is_valid():
        return JsonResponse(serializer.data)
    else:
        return JsonResponse(serializer.errors, status=400)