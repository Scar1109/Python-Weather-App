import unittest
from unittest.mock import patch, Mock
from weather import get_lat_lon, get_weather_data, WeatherData, main

class TestWeather(unittest.TestCase):
    
    @patch('weather.requests.get')
    def test_get_lat_lon_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "name": "Ambalangoda",
                "lat": 6.2359,
                "lon": 80.0539,
                "country": "LK"
            }
        ]
        mock_get.return_value = mock_response
        lat, lon = get_lat_lon("Ambalangoda", "Galle", "SriLanka", "fake_api_key")
        self.assertEqual(lat, 6.2359)
        self.assertEqual(lon, 80.0539)

    @patch('weather.requests.get')
    def test_get_lat_lon_failure(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        lat, lon = get_lat_lon("UnknownCity", "UnknownState", "UnknownCountry", "fake_api_key")
        self.assertIsNone(lat)
        self.assertIsNone(lon)

    @patch('weather.requests.get')
    def test_get_weather_data_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "weather": [
                {
                    "main": "Clouds",
                    "description": "overcast clouds",
                    "icon": "04d"
                }
            ],
            "main": {
                "temp": 28,
                "feels_like": 31,
                "humidity": 74
            }
        }
        mock_get.return_value = mock_response
        data = get_weather_data(6.2359, 80.0539, "fake_api_key")
        self.assertIsInstance(data, WeatherData)
        self.assertEqual(data.main, "Clouds")
        self.assertEqual(data.description, "overcast clouds")
        self.assertEqual(data.icon, "04d")
        self.assertEqual(data.temperature, 28)
        self.assertEqual(data.feels_like, 31)
        self.assertEqual(data.humidity, 74)

    @patch('weather.requests.get')
    def test_get_weather_data_failure(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        data = get_weather_data(0, 0, "fake_api_key")
        self.assertIsNone(data)

    @patch('weather.get_lat_lon')
    @patch('weather.get_weather_data')
    def test_main_success(self, mock_get_weather_data, mock_get_lat_lon):
        mock_get_lat_lon.return_value = (6.2359, 80.0539)
        mock_get_weather_data.return_value = WeatherData(
            main="Clouds", description="overcast clouds", icon="04d",
            temperature=28, feels_like=31, humidity=74
        )
        data = main("Ambalangoda", "Galle", "SriLanka")
        self.assertIsInstance(data, WeatherData)
        self.assertEqual(data.main, "Clouds")

    @patch('weather.get_lat_lon')
    @patch('weather.get_weather_data')
    def test_main_failure(self, mock_get_weather_data, mock_get_lat_lon):
        mock_get_lat_lon.return_value = (None, None)
        mock_get_weather_data.return_value = None
        data = main("UnknownCity", "UnknownState", "UnknownCountry")
        self.assertIsNone(data)

if __name__ == '__main__':
    unittest.main()
