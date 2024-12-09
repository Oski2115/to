import math
import time
import random
from functools import partial
from typing import List, Iterator
from abc import ABC, abstractmethod

#area boundaries
LAT_MIN, LAT_MAX = 49.95855025648944, 50.154564013341734
LON_MIN, LON_MAX = 19.688292482742394, 20.02470275868903

# Incident probabilities
INCIDENT_TYPES = ["PZ", "AF", "MZ"]
INCIDENT_PROBABILITIES = [0.7, 0.05, 0.25]


class VehicleState(ABC):
    @abstractmethod
    def handle(self, vehicle):
        pass


class FreeState(VehicleState):
    def handle(self, vehicle):
        vehicle.state = "Free"

class OnTheWayState(VehicleState):
    def handle(self, vehicle):
        vehicle.state = "Driving"

class BusyState(VehicleState):
    def handle(self, vehicle):
        vehicle.state = "Busy"


# Strategy
class IncidentHandlingStrategy(ABC):
    @abstractmethod
    def handle_incident(self, vehicles):
        pass

class FireStrategy(IncidentHandlingStrategy):
    def handle_incident(self, vehicles):
        return vehicles[:3]

class OtherStrategy(IncidentHandlingStrategy):
    def handle_incident(self, vehicles):
        return vehicles[:2]


# Iterator
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

    def notify_all(self, data):
        for observer in self.observers:
            observer.update(data)

class Vehicle:
    def __init__(self, id):
        self.id = id
        self.state = "Free"

    def change_state(self, state):
        state.handle(self)


# (Observer)
class FireStation(Observer):

    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.vehicles = [Vehicle(f"{name}-{i + 1}") for i in range(5)]

    def update(self, data):
        print(f"Jednostka {self.name} została powiadomiona o {data['type']} w ({data['width']}, {data['height']})")

    def dispatch_vehicles(self, num_vehicles):
        free_vehicles = [v for v in self.vehicles if v.state == "Free"]
        dispatched = free_vehicles[:num_vehicles]
        for vehicle in dispatched:
            vehicle.change_state(OnTheWayState())
        return dispatched


class Incident:
    def __init__(self, category, width, height):
        self.category = category
        self.width = width
        self.height = height


def generate_random_incident():
    type = random.choices(INCIDENT_TYPES, INCIDENT_PROBABILITIES)[0]
    width = random.uniform(LAT_MIN, LAT_MAX)
    height = random.uniform(LON_MIN, LON_MAX)
    return Incident(type, width, height)


def distance(station, incident):
    return math.sqrt((station.width - incident.width) ** 2 + (station.height - incident.height) ** 2)


def free_busy_vehicles(busy_vehicles, current_time):
    for vehicle, release_time in busy_vehicles.copy():
        if current_time >= release_time:
            vehicle.change_state(FreeState())
            busy_vehicles.remove((vehicle, release_time))
            print(f"Pojazd {vehicle.id} jest już wolny")

def simulate_continuous():
    skkm = SKKM()
    fire_stations = [
        FireStation("JRG-1", 50.06005865507538, 19.943145813490625),
        FireStation("JRG-2", 50.033434183133245, 19.93583717116354),
        FireStation("JRG-3", 50.07575650438391, 19.887307269218),
        FireStation("JRG-4", 50.037805782280415, 20.00578765767291),
        FireStation("JRG-5", 50.09189416281071, 19.919920411635406),
        FireStation("JRG-6", 50.016264155373, 20.015574698144782),
        FireStation("JRG-7", 50.0941607799504, 19.977372355817707),
        FireStation("JRG SAPSP", 50.077233691472934, 20.03280947908853),
        FireStation("SKA", 49.96843060535878, 19.799578173018755),
        FireStation("LSP", 50.077249280379306, 19.786397563318232)
    ]

    fire_station_iterator = FireStationIterator(fire_stations)

    for station in fire_station_iterator: 
        skkm.add_observer(station)

    busy_vehicles = []

    while True:
        incident = generate_random_incident()
        current_time = time.time()
        free_busy_vehicles(busy_vehicles, current_time)        

        print(f"Nowe zdarzenie '{incident.category}' w ({incident.width}, {incident.height})")

        skkm.notify_all({"type": incident.category, "width": incident.width, "height": incident.height})

        by_distance = partial(distance, incident=incident)
        stations_by_distance = sorted(fire_stations, key=by_distance)

        if incident.category == "PZ":
            vehicles_needed = 3
        else:
            vehicles_needed = 2

        dispatched_vehicles = []

        for station in stations_by_distance:
            if len(dispatched_vehicles) >= vehicles_needed:
                break
            dispatched_vehicles += station.dispatch_vehicles(vehicles_needed - len(dispatched_vehicles))

        if dispatched_vehicles:
            print(f"Przydzielono {len(dispatched_vehicles)} pojazdy:")
            for vehicle in dispatched_vehicles:
                    print(f"{vehicle.id}")
        else:
            print("Brak pojazdów do przydzielenia")

        response_time = random.uniform(0, 3)
        false_alarm = random.random() < 0.05

        print(f"Dojechano na miejsce zdarzenia po {response_time:.2f}s")

        if false_alarm:
            print("Alarm okazał się fałszywy")
        else:
            action_time = random.uniform(5, 25)
            print(f"Działania trwały {action_time:.2f}s")

        action_end_time = current_time + action_time
        for vehicle in dispatched_vehicles:
            busy_vehicles.append((vehicle, action_end_time))

        time.sleep(0.5)

simulate_continuous()
