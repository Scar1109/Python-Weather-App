import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()
api_key = os.getenv('WEATHER_API_KEY')

@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: int
    feels_like : int
    humidity : int

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
            f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric'
        ).json()
        
        if not response:
            raise ValueError("No data found for the specified location.")
        
        data = WeatherData(
            main = response.get('weather')[0].get('main'),
            description= response.get('weather')[0].get('description'),
            icon = response.get('weather')[0].get('icon'),
            temperature= int(response.get('main').get('temp')),
            feels_like= int(response.get('main').get('feels_like')),
            humidity= response.get('main').get('humidity')
        )
        return data
    
    except (IndexError, ValueError, KeyError) as e:
        print(f"Error occurred: {e}")
        return None
    
def main(city_name, state_name, country_name):
    lat, lon = get_lat_lon(city_name, state_name, country_name, api_key)
    weather_data = get_weather_data(lat, lon, api_key)
    return weather_data
    
    
if __name__ == '__main__':
    print(main('Ambalangoda', 'Galle', 'SriLanka'))