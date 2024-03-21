import api, rtt_parser
import os

user = os.getenv("RTT_USER")
passw = os.getenv("RTT_PASS")
station = os.getenv("STATION")

def main():
    rtt = api.Rtt(user, passw)
    departures = rtt.fetch_station_departures(station)
    services = rtt_parser.parse_station_search(departures)
    for service in services:
        if service.delayed:
            print(f"{service.booked_depature_time} {service.destination} Plat {service.platform} Exp: {service.departure_time}")
        else:
            print(f"{service.departure_time} {service.destination} Plat {service.platform} On time")
        service_info = rtt.fetch_service(service.uid, service.date_depature)
        service.calls = rtt_parser.parse_calls(service_info)
        print(f"Calling at: {', '.join(service.calls)}")

if __name__ == "__main__":
    main()
