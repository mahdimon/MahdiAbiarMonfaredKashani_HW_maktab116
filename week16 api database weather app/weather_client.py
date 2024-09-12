import requests
from tabulate import tabulate


def start_client() -> None:
    """
Start the weather client command-line interface.
"""
    BASE_URL = 'https://checkweather.zapto.org:2424/openweathermap-by-mahdimon'

    while True:
        command = input(
            '''\nenter city name the see the weather or enter 0 to check the log: ''')
        if command == '0':
            URL_PARAMS = {"fetch_log": True}
        else:
            URL_PARAMS = {"city": command}

        try:
            response = requests.get(BASE_URL, params=URL_PARAMS)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
            continue

        data = dict(response.json())
        if command == '0':
            print(f"""
            Request count: {data['rq']}
            Successful request count: {data["src"]}
            Last hour requests:
            {tabulate(data["lhr"], headers=["city", "time"], tablefmt="grid")}
            City request counts:
            {tabulate(data["crc"], headers=["city", "count"], tablefmt="grid")}
            """)
        else:
            print(f"""
            Temperature: {data["temp"]}
            Feels like: {data["feels_like"]}
            Last updated: {data["last_updated_time"]}""")


start_client()
