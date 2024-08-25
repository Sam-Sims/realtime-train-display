from dataclasses import dataclass
from typing import Any
from rtt_api import api

@dataclass
class TrainService:
    """
    Represents a train service.

    Attributes:
        destination: The destination of the train service.
        departure_time: The actual departure time of the service.
        booked_departure_time: The scheduled departure time of the service.
        delayed: Indicates if the service is delayed.
        platform: The platform number for the service.
        operator: The train operator for the service.
        uid: Unique identifier for the service.
        date_departure: The date of departure for the service.
        calls: List of stations the service calls at.
    """
    destination: str | None = None
    departure_time: str | None  = None
    booked_departure_time: str | None  = None
    delayed: bool | None = None
    platform: str | None  = None
    operator: str | None  = None
    uid: str | None  = None
    date_departure: str | None  = None
    calls: list[str] | None= None

    @classmethod
    def _build_service(cls, service_data: dict[str, Any]) -> 'TrainService':
        """
        Builds a TrainService instance from a station search API call.

        Args:
            service_data: Dictionary containing service information.

        Returns:
            TrainService: An instance of TrainService populated with the provided data.
        """
        service = cls()
        service.destination = service_data['locationDetail']['destination'][0]['description']
        service.departure_time = service_data['locationDetail']['realtimeDeparture']
        service.booked_departure_time = service_data['locationDetail']['gbttBookedDeparture']
        service.delayed = service.departure_time != service.booked_departure_time
        service.platform = service_data['locationDetail']['platform']
        service.operator = service_data['atocName']
        service.uid = service_data['serviceUid']
        service.date_departure = service_data['runDate'].replace('-', '/')
        return service

    @staticmethod
    def get_train_services(response: dict[str, Any]) -> list['TrainService']:
        """
        Creates a list of TrainService instances from an API response.

        Args:
            response: Dictionary containing information about multiple train services
        Returns:
            A list of TrainService instances, each representing a train service.
        """
        return [TrainService._build_service(service) for service in response['services']]

    @staticmethod
    def _filter_stations_after(station_list: list[str], filter_station: str) -> list[str]:
        """
        Filters a list of stations to include only those after a specified station.

        Args:
            station_list: List of station names.
            filter_station: The station name to filter from.

        Returns:
            A list of station names that come after the filter_station in the original list.
            Returns an empty list if the filter_station is not found.
        """
        try:
            index = station_list.index(filter_station)
            return station_list[index + 1:]
        except ValueError:
            return []

    @staticmethod
    def _parse_calls(response: dict[str, Any], filter_station: str) -> list[str]:
        """
        Parses the service API response to extract station calls after a given filter station.

        Args:
            response: Dictionary containing service location information.

        Returns:
            List of station names the service calls at after Nottingham.
        """
        station_calls = [location['description'] for location in response['locations']]
        return TrainService._filter_stations_after(station_calls, filter_station)

    def update_station_calls(self, service_info: dict[str, Any], filter_station: str) -> None:
        """
        Retrieves and sets the list of station calls for this service

        Args:
            service_info: Dictionary containing detailed service information.
            filter_station: The station name to filter from when determining calls

        This method updates the 'calls' attribute of the TrainService instance.
        """
        self.calls = self._parse_calls(service_info, filter_station)

    def build_service_info(self) -> tuple[str, str]:
        """
        Builds a formatted string containing service information and calling points

        Returns:
            A tuple containing two strings:
            - The first string contains departure time, destination, platform, and status.
            - The second string lists the stations the service calls at, if available.
        """
        info = f'{self.departure_time} {self.destination}     Plat {self.platform}                 On time'
        calls = f"Calling at: {', '.join(self.calls)}" if self.calls else "No calling information available"
        return info, calls