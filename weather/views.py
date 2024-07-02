import os
import requests
from django.http import JsonResponse
from django.views import View


class GreetingView(View):
    def get(self, request):
        your_name = request.GET.get('your_name')
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get('REMOTE_ADDR')

        if client_ip in ('127.0.0.1', 'localhost'):
            location = 'Nigeria'
        else:
            location = self.get_location(client_ip)

        if location == 'Unknown':
            return JsonResponse({
                'clientIp': client_ip,
                'location': 'Unknown',
                'greeting': 'Failed to resolve location'
            })

        weather_api_key = os.getenv('OPENWEATHER_API_KEY')
        if not weather_api_key:
            return JsonResponse({
                'clientIp': client_ip,
                'location': 'Unknown',
                'greeting': 'API Key not set!'
            })

        temperature = self.get_temperature(location, weather_api_key)
        if temperature == 'N/A':
            return JsonResponse({
                'clientIp': client_ip,
                'location': location,
                'greeting': 'Failed to get temperature'
            })

        return JsonResponse({
            'clientIp': client_ip,
            'location': location,
            'greeting': f'Hello, {your_name}!, the temperature is {temperature} in {location}'
        })

    def get_location(self, client_ip):
        url = f'https://freegeoip.app/json/{client_ip}'
        try:
            response = requests.get(url)
            response_data = response.json()
            return response_data.get('city', 'Unknown')
        except requests.RequestException:
            return 'Unknown'

    def get_temperature(self, location, api_key):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}'
        try:
            response = requests.get(url)
            response_data = response.json()
            if response.status_code == 200:
                return f"{response_data['main']['temp']} degrees Celsius"
            return 'N/A'
        except requests.RequestException:
            return 'N/A'
