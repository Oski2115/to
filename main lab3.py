import math
import json
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from abc import ABC, abstractmethod
import matplotlib

matplotlib.use('TkAgg')


class FileHandling:
    def save_to_file(self, population, filename="state.json"):
        data = [p.to_dict() for p in population if not p.zniknięty]
        with open(filename, "w") as file:
            json.dump(data, file)
        print(f"Stan zapisany do pliku {filename}.")

    def restore_from_file(self, filename="state.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            print(f"Stan przywrócony z pliku {filename}.")
            return [self.create_person_from_dict(p) for p in data]
        except FileNotFoundError:
            print(f"Plik {filename} nie istnieje.")
            return []
        except Exception as e:
            print(f"Błąd podczas odczytu pliku: {e}")
            return []

    @staticmethod
    def create_person_from_dict(data):
        if data["type"] == "Healthy":
            return Healthy(data["x"], data["y"], data["id"])
        elif data["type"] == "Infected":
            person = Infected(data["x"], data["y"], data["id"])
            person.czas_zakażenia = data["czas_zakażenia"]
            person.objawy = data["objawy"]
            return person
        elif data["type"] == "Immune":
            return Immune(data["x"], data["y"], data["id"])


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def abs(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)


class Person(ABC):
    def __init__(self, x, y, id, velocity=None):
        self.x = x
        self.y = y
        self.id = id
        self.velocity = velocity or Vector2D(random.uniform(-2.5, 2.5), random.uniform(-2.5, 2.5))
        self.zniknięty = False

    def distance_to(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def move(self, grid_size):
        # Losowa zmiana prędkości i kierunku z 10% szans
        if random.random() < 0.1:
            new_velocity_x = random.uniform(-2.5, 2.5)
            new_velocity_y = random.uniform(-2.5, 2.5)
            new_velocity = Vector2D(new_velocity_x, new_velocity_y)
            self.velocity = new_velocity

        self.x += self.velocity.x
        self.y += self.velocity.y

        if self.x < 0 or self.x > grid_size[0]:
            if random.random() < 0.5:
                self.zniknięty = True
            else:
                self.velocity.x *= -1
        if self.y < 0 or self.y > grid_size[1]:
            if random.random() < 0.5:
                self.zniknięty = True
            else:
                self.velocity.y *= -1

    @abstractmethod
    def infect(self):
        pass

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "id": self.id,
            "type": self.__class__.__name__,
        }


class Healthy(Person):
    def infect(self):
        return Infected(self.x, self.y, self.id)


class Infected(Person):
    def __init__(self, x, y, id):
        super().__init__(x, y, id)
        self.czas_zakażenia = 0
        self.objawy = random.random() < 0.5
        self.max_czas_zakażenia = random.randint(20, 30) * 25  # 20-30 sekund (liczone w klatkach)

    def infect(self):
        self.czas_zakażenia += 1
        if self.czas_zakażenia >= self.max_czas_zakażenia:
            return Immune(self.x, self.y, self.id)
        return self  # Pozostaje zakażony

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "czas_zakażenia": self.czas_zakażenia,
            "objawy": self.objawy
        })
        return data


class Immune(Person):
    def infect(self):
        return self


def initialize_population(liczba_osobników, wymiary, odporni):
    population = []
    for i in range(liczba_osobników):
        if random.random() < odporni:
            person = Immune(random.uniform(0, wymiary[0]), random.uniform(0, wymiary[1]), i)
        else:
            person = Healthy(random.uniform(0, wymiary[0]), random.uniform(0, wymiary[1]), i)
        population.append(person)

    for _ in range(25):
        healthy_person = random.choice([p for p in population if isinstance(p, Healthy)])
        population.remove(healthy_person)
        population.append(healthy_person.infect())

    return population


def add_new_person(grid_size, id):
    edge = random.choice(["top", "bottom", "left", "right"])
    if edge == "top":
        x, y = random.uniform(0, grid_size[0]), 0
    elif edge == "bottom":
        x, y = random.uniform(0, grid_size[0]), grid_size[1]
    elif edge == "left":
        x, y = 0, random.uniform(0, grid_size[1])
    else:  # "right"
        x, y = grid_size[0], random.uniform(0, grid_size[1])

    # 10% szans na zakażenie
    if random.random() < 0.1:
        return Infected(x, y, id)
    else:
        return Healthy(x, y, id)


def update_population(population, grid_size, liczba_osobników):
    new_population = []
    contact_tracker = {}

    for person in population:
        person.move(grid_size)

        if isinstance(person, Healthy):
            for other in population:
                if isinstance(other, Infected) and not other.zniknięty:
                    distance = person.distance_to(other)
                    if distance <= 2:
                        contact_tracker[(person.id, other.id)] = contact_tracker.get((person.id, other.id), 0) + 1
                        if contact_tracker[(person.id, other.id)] >= 75:
                            if (other.objawy) or (not other.objawy and random.random() < 0.5):
                                person = person.infect()
                                break
                    else:
                        contact_tracker[(person.id, other.id)] = 0

        if isinstance(person, Infected):
            if person.zniknięty:
                # Osoba zakażona opuszcza obszar – staje się odporna
                new_population.append(Immune(person.x, person.y, person.id))
            else:
                # Aktualizuj czas zakażenia
                new_person = person.infect()
                new_population.append(new_person)

        elif not person.zniknięty:
            new_population.append(person)

    while len(new_population) < liczba_osobników:
        new_population.append(add_new_person(grid_size, len(new_population)))

    return new_population


def symulacja_animowana(liczba_osobników, wymiary, czas_symulacji, odporni):
    fileHandling = FileHandling()
    population = initialize_population(liczba_osobników, wymiary, odporni)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, wymiary[0])
    ax.set_ylim(0, wymiary[1])
    scatter = ax.scatter([], [], s=50)

    def update(frame):
        nonlocal population
        population = update_population(population, wymiary, liczba_osobników)

        scatter.set_offsets([(p.x, p.y) for p in population if not p.zniknięty])
        scatter.set_color(
            ["blue" if isinstance(p, Healthy) else "red" if isinstance(p, Infected) else "green" for p in population]
        )

    def on_key(event):
        nonlocal population
        if event.key == 'z':
            fileHandling.save_to_file(population)
        elif event.key == 'w':
            population = fileHandling.restore_from_file()

    fig.canvas.mpl_connect('key_press_event', on_key)

    anim = FuncAnimation(fig, update, frames=czas_symulacji, interval=40, repeat=False)
    plt.show()


symulacja_animowana(liczba_osobników=150, wymiary=(300, 300), czas_symulacji=1000, odporni=0.0)
