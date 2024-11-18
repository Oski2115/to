import random
import math

class Vector2D():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getComponents(self):
        return [self.x, self.y]

    def abs(self):
        return math.sqrt(self.x ** 2 + self.y **2)
    
    def cdot(self, ivector):
        values = ivector.getComponents()
        return self.x * values[0] + self.y * values[1]
    
#klasa ziutka
class Osobnik:
    def __init__(self, x, y, odpornosc=False):
        self.x = x
        self.y = y
        self.xspeed = random.uniform(-2.5, 2.5)
        self.yspeed = random.uniform(-2.5, 2.5)
        self.w_obszarze = True
        self.czas_zakażenia = 0




        self.odporny = odpornosc
        self.zdrowy = not odpornosc
        self.zakazony = False
        self.objawy = False

    def move(self, n, m, dt):
        self.x += self.xspeed * dt
        self.y += self.yspeed * dt

        if self.x <= 0 or self.x >= n or self.y <= 0 or self.y >= m:
            self.decyzja_na_granicy(self, n, m)


    def zawroc(self, n, m):
        if self.x <= 0:
            self.xspeed = -1.0 * self.xspeed
        elif self.x >= n:
            self.xspeed = -1.0 * self.xspeed 
        if self.y <= 0:
            self.yspeed = -1.0 * self.yspeed 
        elif self.y >= m:
            self.yspeed = -1.0 * self.yspeed 

    def opuść_obszar(self):
        self.w_obszarze = False

    def decyzja_na_granicy(self, n, m):
        if random.random() < 0.5:
            self.zawróć(n, m)
        else:
            self.opuść_obszar()