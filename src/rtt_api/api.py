import requests
from requests.auth import HTTPBasicAuth


class Rtt:
    def __init__(self, username, password):
        self.base = 'https://api.rtt.io/api/v1/'
        self.username = username
        self.password = password

    def request(self, url) -> dict[str, any]:
        auth = HTTPBasicAuth(self.username, self.password)
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            return response.json()
        else:
            raise requests.HTTPError(response.status_code)

    def fetch_station_departures(self, query) -> dict[str, any]:
        url = f'{self.base}/json/search/{query}'
        return self.request(url)

    def fetch_service(self, uid, date) -> dict[str, any]:
        url = f'{self.base}/json/service/{uid}/{date}'
        return self.request(url)
