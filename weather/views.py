import os
import requests
import logging
from django.http import JsonResponse
from django.views import View

logger = logging.getLogger(__name__)


class GreetingView(View):
    def get(self, request):
        visitor_name = request.GET.get('name', 'Guest')
        client_ip = self.get_client_ip(request)
        location = self.get_location(client_ip)

        if location == 'Unknown':
            logger.error(f"Failed to resolve location for IP: {client_ip}")
            return JsonResponse({
                'clientIp': client_ip,
                'location': 'Unknown',
                'greeting': 'Failed to resolve location'
            })

        weather_api_key = os.getenv('OPENWEATHER_API_KEY')
        if not weather_api_key:
            logger.error("API Key not set!")
            return JsonResponse({
                'clientIp': client_ip,
                'location': 'Unknown',
                'greeting': 'API Key not set!'
            })

        temperature = self.get_temperature(location, weather_api_key)
        if temperature == 'N/A':
            logger.error(f"Failed to get temperature for location: {location}")
            return JsonResponse({
                'clientIp': client_ip,
                'location': location,
                'greeting': 'Failed to get temperature'
            })

        return JsonResponse({
            'clientIp': client_ip,
            'location': location,
            'greeting': f'Hello, {visitor_name}! The temperature is {temperature} in {location}'
        })

    def get_client_ip(self, request):
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if client_ip:
            client_ip = client_ip.split(',')[0]
        else:
            client_ip = request.META.get('REMOTE_ADDR')
        logger.info(f"Resolved client IP: {client_ip}")
        return client_ip

    def get_location(self, client_ip):
        if client_ip in ('127.0.0.1', 'localhost'):
            logger.info("Localhost detected, defaulting location to 'Nigeria'")
            return 'Nigeria'

        latitude, longitude = '0', '0'
        if client_ip != 'Unknown':

            latitude, longitude = '6.5244', '3.3792'

        return self.get_city_from_coords(latitude, longitude)

    def get_city_from_coords(self, latitude, longitude):
        weather_api_key = os.getenv('OPENWEATHER_API_KEY')
        url = f'http://api.openweathermap.org/geo/1.0/reverse?lat={latitude}&lon={longitude}&limit=1&appid={weather_api_key}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            try:
                response_data = response.json()
                logger.info(f"Geocoding response data: {response_data}")
                if response_data:
                    return response_data[0].get('name', 'Unknown')
                return 'Unknown'
            except ValueError as e:
                logger.error(f"Error decoding JSON from {url}: {e}")
                logger.error(f"Response content: {response.content}")
                return 'Unknown'
        except requests.RequestException as e:
            logger.error(f"Error fetching location from {url}: {e}")
            return 'Unknown'

    def get_temperature(self, location, api_key):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            try:
                response_data = response.json()
                logger.info(f"Weather API response data: {response_data}")
                return f"{response_data['main']['temp']} degrees Celsius"
            except ValueError as e:
                logger.error(f"Error decoding JSON from {url}: {e}")
                logger.error(f"Response content: {response.content}")
                return 'N/A'
        except requests.RequestException as e:
            logger.error(f"Error fetching temperature from {url}: {e}")
            return 'N/A'