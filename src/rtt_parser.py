from api import Service

def parse_station_search(response):
    """
    Parses the response from the "Location Line-Up" rtt API and returns a list of service objects.

    Args:
        response (dict): The response containing depature information.

    Returns:
        list: A list of service objects generated from the response.
    """
    services = [s for s in generate_services(response)]
    return services

def parse_calls(response):
    """
    Parses the response from the "Service Information" rtt API and extracts the stations a train is calling at.

    Args:
        response (dict): The response from the service search.

    Returns:
        list: A list of stations the train is calling at.
    """
    station_calls = [c for c in generate_calls(response)]
    calls = filter_after_nottingham(station_calls)
    return calls

def generate_services(response):
    """
    Generate Service objects from the given response.

    Args:
        response (dict): The response containing depature information.

    Yields:
        Service: A Service object representing a train service.

    """
    for service in response["services"]:
        s = Service()
        s.destination = service["locationDetail"]["destination"][0]["description"]
        s.departure_time = service["locationDetail"]["realtimeDeparture"]
        s.booked_depature_time = service["locationDetail"]["gbttBookedDeparture"]
        s.delayed = service["locationDetail"]["realtimeDeparture"] != service["locationDetail"]["gbttBookedDeparture"]
        s.platform = service["locationDetail"]["platform"]
        s.operator = service["atocName"]
        s.uid = service["serviceUid"]
        s.date_depature = service["runDate"]
        s.date_depature = s.date_depature.replace("-", "/")
        yield s

def generate_calls(response):
    """
    Generate station calls from the given response.

    Args:
        response (dict): The response containing locations of stations the train will call at.

    Yields:
        str: The description (Name) of each location.

    """
    for location in response["locations"]:
        yield location["description"]

def filter_after_nottingham(station_list):
    """
    Filters the given station_list to include only the stations after 'Nottingham'.

    Args:
        station_list (list): A list of station names.

    Returns:
        list: A new list containing the stations after 'Nottingham'.

    """
    try:
        index = station_list.index('Nottingham')
        return station_list[index + 1:]
    except ValueError:
        return []
