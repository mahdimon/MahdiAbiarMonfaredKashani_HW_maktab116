import requests
import json
from datetime import datetime
import pytz
from functools import cached_property
from http.server import BaseHTTPRequestHandler, HTTPServer
from ssl import PROTOCOL_TLS_SERVER, SSLContext
from urllib.parse import parse_qsl, urlparse
import os
from database import WeatherDatabase


def get_city_weather(city_name: str) -> dict:
    """
Retrieve weather data from an external API for a given city.
Args:
- city_name (str): The name of the city to retrieve weather data for.
Returns:
- dict: A dictionary containing weather information for the city, including
temperature, feels like temperature, and last updated time.
"""

    API_KEY = os.getenv("openweathermap_api")
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
    unit = "metric"
    URL_PARAMS = {'q': city_name, 'appid': API_KEY, "units": unit}

    try:
        response = requests.get(BASE_URL, params=URL_PARAMS, timeout=10)
        data = dict(response.json())
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(data)
    else:
        api_city_name = data['name']
        temp = data['main']['temp']
        real_feel = data['main']['feels_like']
        last_update_timestamp = data['dt']
        last_update_datetime = datetime.fromtimestamp(
            last_update_timestamp, tz=TIMEZONE)
        last_update_str = last_update_datetime.strftime(TIME_FORMAT)
        return {"name": api_city_name, "temp": temp, "feels_like": real_feel, "last_updated_time": last_update_str}


def start_server() -> None:

    certificate = "/etc/letsencrypt/live/checkweather.zapto.org/fullchain.pem"
    private_key = "/etc/letsencrypt/live/checkweather.zapto.org/privkey.pem"
    ssl_context = SSLContext(PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certificate, private_key)
    server = HTTPServer(("checkweather.zapto.org", 2424), MyRequestHandler)
    server.socket = ssl_context.wrap_socket(server.socket, server_side=True)
    server.serve_forever()


class MyRequestHandler(BaseHTTPRequestHandler):
    @cached_property
    def parsed_url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.parsed_url.query))

    def do_GET(self):
        if self.parsed_url.path == '/openweathermap-by-mahdimon':
            city = self.query_data.get('city')
            fetch_log = self.query_data.get('fetch_log')

            if city:
                request_time = datetime.now(TIMEZONE).strftime(TIME_FORMAT)
                database.save_request_data(city, request_time)
                try:
                    response = get_city_weather(self.query_data.get('city'))
                    database.save_response_data(response)
                except ValueError as e:
                    e = e.args[0]
                    self.send_error(int(e["cod"]), e['message'])
            elif fetch_log.lower() == "true":
                response = {"rq": database.get_request_count(),
                            "src": database.get_successful_request_count(),
                            "lhr": database.get_last_hour_requests(),
                            "crc": database.get_city_request_count()}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
TIMEZONE_STR = 'Asia/Tehran'
TIMEZONE = pytz.timezone(TIMEZONE_STR)
TIME_FORMAT = r'%Y-%m-%d %H:%M:%S'
if __name__ == "__main__":

    database = WeatherDatabase()
    start_server()
