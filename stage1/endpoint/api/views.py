from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .serializers import GreetingSerializer
import requests

# Create your views here.

OPENWEATHER_API_KEY = "727ccf37ec07d9c535a70e5d5f6914dd"
@require_GET
def hello(request):
    visitor_name = request.GET.get("visitor_name", "Guest")
    client_ip = request.META.get("HTTP_X_FORWARDED_FOR")
    if client_ip:
        client_ip = client_ip.split("," [0])
    else:
        client_ip = request.META.get("REMOTE_ADDR")
    
    private_ip_ranges = [
        '10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.', '172.21.', 
        '172.22.', '172.23.', '172.24.', '172.25.', '172.26.', '172.27.', '172.28.', 
        '172.29.', '172.30.', '172.31.', '192.168.'
    ]
    if any(client_ip.startswith("range") for range in private_ip_ranges) or client_ip == "127.0.0.1":
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