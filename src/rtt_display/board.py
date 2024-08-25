import os
import sys
import time

from luma.core import cmdline, error
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1322
from dotenv import load_dotenv

from realtime_train_display import rtt_parser
from rtt_api import api

load_dotenv()
user = os.getenv("RTT_USER")
passw = os.getenv("RTT_PASS")
station = os.getenv("STATION")


def build_service(service):
    info = f'{service.departure_time} {service.destination}     Plat {service.platform}                 On time'
    calls = f"Calling at: {', '.join(service.calls)}"
    return info, calls


def main():
    serial = spi(port=0)
    device = ssd1322(serial, mode='1')
    # device = get_device()

    rtt = api.Rtt(user, passw)
    departures = rtt.fetch_station_departures(station)
    services = rtt_parser.parse_station_search(departures)
    service = services[0]
    service_info = rtt.fetch_service(service.uid, service.date_departure)
    service.calls = rtt_parser.parse_calls(service_info)

    print(f'{service.departure_time} {service.destination} Plat {service.platform} On time')
    info1, calls1 = build_service(service)
    currenttime = time.strftime('%H:%M:%S')

    # get next service
    service = services[1]
    service_info = rtt.fetch_service(service.uid, service.date_departure)
    service.calls = rtt_parser.parse_calls(service_info)
    info2, calls2 = build_service(service)

    with canvas(device) as draw:
        draw.text((110, 50), currenttime, fill='yellow')
        draw.text((1, 1), info1, fill='yellow')
        draw.text((1, 10), calls1, fill='yellow')
        draw.text((1, 30), info2, fill='yellow')

    time.sleep(10)
