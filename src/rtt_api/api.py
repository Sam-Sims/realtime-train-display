from typing import Any

import requests
from requests.auth import HTTPBasicAuth


class RttConnection:
    BASE_URL = 'https://api.rtt.io/api/v1/json'

    def __init__(self, username: str, password: str):
        self.auth = HTTPBasicAuth(username, password)

    def _request(self, endpoint: str) -> dict[str, Any]:
        url = f'{self.BASE_URL}/{endpoint}'
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def fetch_station_departures(self, station: str) -> dict[str, Any]:
        return self._request(f'search/{station}')

    def fetch_service(self, uid: str, date: str) -> dict[str, Any]:
        return self._request(f'service/{uid}/{date}')
