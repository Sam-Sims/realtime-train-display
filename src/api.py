import requests
from requests.auth import HTTPBasicAuth

class Service:
    def __init__(self):
        self.destination = None
        self.departure_time = None
        self.booked_departure_time = None
        self.delayed = None
        self.platform = None
        self.operator = None
        self.uid = None
        self.date_depature = None
        self.calls = None

class Rtt:
    def __init__(self, username, password):
        self.base = "https://api.rtt.io/api/v1/"
        self.username = username
        self.password = password

    def request(self, url):
        auth = HTTPBasicAuth(self.username, self.password)
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            return response.json()
        else:
            raise requests.HTTPError(response.status_code)

    def fetch_station_departures(self, query):
        url = f"{self.base}/json/search/{query}"
        return self.request(url)
    
    def fetch_service(self, uid, date):
        url = f"{self.base}/json/service/{uid}/{date}"
        return self.request(url)