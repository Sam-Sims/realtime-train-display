import os
import sys
import time
from dataclasses import dataclass

from luma.core import cmdline, error
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1322
from dotenv import load_dotenv

from rtt_api import api, rtt_parser
from rtt_api.trainservice import TrainService


def load_env_variables() -> tuple[str, str, str]:
    load_dotenv()
    return os.getenv('RTT_USER'), os.getenv('RTT_PASS'), os.getenv('STATION')


def get_train_services(connection: api.RttConnection, station: str, num_services: int = 2) -> list[TrainService]:
    # fetch the station departures from RTT API
    departures = connection.fetch_station_departures(station)
    # transform into a list of TrainService objects
    services = TrainService.get_train_services(departures)
    # fetch the station calls only for the number of services requested
    # this is to avoid making unnecessary API calls
    for service in services[:num_services]:
        # get the details of each individual service
        service_info = connection.fetch_service(service.uid, service.date_departure)
        # update the service with the station calls
        service.update_station_calls(service_info, "Nottingham")
    # return only the requested number of services
    return services[:num_services]

def display_services(device: ssd1322, services: list[TrainService]):
    current_time = time.strftime('%H:%M:%S')

    with canvas(device) as draw:
        draw.text((110, 50), current_time, fill='yellow')
        for i, service in enumerate(services):
            info, calls = service.build_service_info()
            draw.text((1, 1 + i * 30), info, fill='yellow')
            draw.text((1, 10 + i * 30), calls, fill='yellow')

def main():
    user, passw, station = load_env_variables()

    serial = spi(port=0)
    device = ssd1322(serial, mode='1')

    connection = api.RttConnection(user, passw)
    try:
        while True:
            services = get_train_services(connection, station)
            display_services(device, services)

            for _ in range(60):
                time.sleep(1)
                display_services(device, services)
    except KeyboardInterrupt:
        print("Terminated")
    finally:
        device.cleanup()