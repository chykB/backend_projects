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

    # Ensure client_ip is a string
    if isinstance(client_ip, list):
        client_ip = client_ip[0]
    client_ip = str(client_ip)
    
    private_ip_ranges = {
        '10.': True,
        '172.16.': True, '172.17.': True, '172.18.': True, '172.19.': True,
        '172.20.': True, '172.21.': True, '172.22.': True, '172.23.': True,
        '172.24.': True, '172.25.': True, '172.26.': True, '172.27.': True,
        '172.28.': True, '172.29.': True, '172.30.': True, '172.31.': True,
        '192.168.': True
    }
    for prefix in private_ip_ranges:
        if client_ip.startswith(prefix) or client_ip == '127.0.0.1':
            client_ip = '8.8.8.8'
            break
    
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