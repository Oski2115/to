import random
from typing import List, Iterator
from abc import ABC, abstractmethod

#area boundaries
LAT_MIN, LAT_MAX = 49.95855025648944, 50.154564013341734
LON_MIN, LON_MAX = 19.688292482742394, 20.02470275868903

# Incident probabilities
INCIDENT_TYPES = ["PZ", "AF", "MZ"]
INCIDENT_PROBABILITIES = [0.7, 0.05, 0.25]


# State pattern for Vehicle
class VehicleState(ABC):
    @abstractmethod
    def handle(self, vehicle):
        pass

class FreeState(VehicleState):
    def handle(self, vehicle):
        vehicle.state = "Free"


class InRouteState(VehicleState):
    def handle(self, vehicle):
        vehicle.state = "In Route"


class BusyState(VehicleState):
    def handle(self, vehicle):
        vehicle.state = "Busy"

# Strategy pattern for Incident Handling
class IncidentHandlingStrategy(ABC):
    @abstractmethod
    def handle_incident(self, vehicles: List['Vehicle']):
        pass


class FireStrategy(IncidentHandlingStrategy):
    def handle_incident(self, vehicles: List['Vehicle']):
        return vehicles[:3]


class OtherStrategy(IncidentHandlingStrategy):
    def handle_incident(self, vehicles: List['Vehicle']):
        return vehicles[:2]


# Observer
class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass


class SKKM:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    def notify(self, data):
        for observer in self.observers:
            observer.update(data)


# Iterator for Fire Station
class FireStationIterator:
    def __init__(self, stations):
        self.stations = stations
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.stations):
            station = self.stations[self.index]
            self.index += 1
            return station
        raise StopIteration


# Vehicle class
class Vehicle:
    def __init__(self, id):
        self.id = id
        self.state = "Free"

    def change_state(self, state: VehicleState):
        state.handle(self)


# FireStation class (Observer)
class FireStation(Observer):
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.vehicles = [Vehicle(f"{name}-{i}") for i in range(5)]

    def update(self, data):
        print(f"Station {self.name} received incident: {data}")


# Incident class
class Incident:
    def __init__(self, type_, latitude, longitude):
        self.type = type_
        self.latitude = latitude
        self.longitude = longitude


# Simulation setup
def generate_random_incident():
    incident_type = random.choices(INCIDENT_TYPES, INCIDENT_PROBABILITIES)[0]
    latitude = random.uniform(LAT_MIN, LAT_MAX)
    longitude = random.uniform(LON_MIN, LON_MAX)
    return Incident(incident_type, latitude, longitude)


def create_fire_stations():
    return [
        FireStation("JRG-1", 50.05, 19.95),
        FireStation("JRG-2", 50.10, 19.90),
        FireStation("JRG-3", 50.00, 20.00),
    ]


# Main simulation
def simulate():
    skkm = SKKM()
    fire_stations = create_fire_stations()

    for station in fire_stations:
        skkm.add_observer(station)

    incidents = [generate_random_incident() for _ in range(10)]
    for incident in incidents:
        skkm.notify(vars(incident))


simulate()
