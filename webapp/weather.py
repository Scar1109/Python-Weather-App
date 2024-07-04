import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('WEATHER_API_KEY')

def get_lat_lon(city_name, state_code, country_code, API_key):
    try:
        response = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}'
        ).json()
        
        if not response:
            raise ValueError("No data found for the specified location.")
        
        data = response[0]
        lat, lon = data.get('lat'), data.get('lon')
        return lat, lon
    except (IndexError, ValueError, KeyError) as e:
        print(f"Error occurred: {e}")
        return None, None
    
def get_weather_data(lat, lon, API_key):
    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}'
        ).json()
        
        if not response:
            raise ValueError("No data found for the specified location.")
        
        print(response)
        return response
    except (IndexError, ValueError, KeyError) as e:
        print(f"Error occurred: {e}")
        return None
    
if __name__ == '__main__':
    lat, lon = get_lat_lon('Ambalangoda', 'Galle', 'SriLanka', api_key)
    get_weather_data(lat, lon, api_key)