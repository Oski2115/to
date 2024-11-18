import math

class IVector:
    def getComponents(self):
        pass

    def abs(self):
        pass

    def cdot(self, ivector):
        pass
 
class Vector2D(IVector):
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
    
class Polar2DInheritance(Vector2D):
    def getAngle(self):
        return math.atan2(self.y, self.x)

class Polar2DAdapter(IVector):
    def __init__(self, srcVector):
        self.srcVector = srcVector

    def abs(self):
        return self.srcVector.abs()

    def cdot(self, param):
        return self.srcVector.cdot(param)

    def getComponents(self):
        return self.srcVector.getComponents()

    def getAngle(self):
        components = self.srcVector.getComponents()
        return math.atan2(components[1], components[0])

class Vector3DDecorator(IVector):
    def __init__(self, vector, z=0):
        self.vector = vector
        self.z = z

    def abs(self):
        components = self.getComponents()
        return math.sqrt(components[0]**2 + components[1]**2 + components[2]**2)

    def cdot(self, ivector):
        components1 = self.getComponents()
        components2 = ivector.getComponents()
        return components1[0] * components2[0] + components1[1] * components2[1] + components1[2] * components2[2]

    def getComponents(self):
        return self.vector.getComponents() + [self.z]

    def cross(self, ivector):
        components1 = self.getComponents()
        components2 = ivector.getComponents()
        x = components1[1] * components2[2] - components1[2] * components2[1]
        y = components1[2] * components2[0] - components1[0] * components2[2]
        z = components1[0] * components2[1] - components1[1] * components2[0]
        return [x, y, z]
    
    def getSrcV(self):
        return self.vector

class Vector3DInheritance(Vector2D):
    def __init__(self, x, y, z=0):
        super().__init__(x, y)
        self.z = z

    def abs(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def cdot(self, Ivector):
        return self.x * Ivector.x + self.y * Ivector.y + self.z * Ivector.z
    
    def getComponents(self):
        return [self.x, self.y, self.z]

    def cross(self, IVector):
        x = self.y * IVector.z - self.z * IVector.y
        y = self.z * IVector.x - self.x * IVector.z
        z = self.x * IVector.y - self.y * IVector.x
        return [x, y, z]
    
    def getSrcV(self):
        return self
    

 # Utworzenie trzech przykładowych wektorów

vectorA = Polar2DAdapter(Vector2D(4, 4))
vectorB = Vector3DDecorator(Vector2D(2, 1), 5)
vectorC = Vector3DDecorator(Vector2D(3, 7), 4)

print("\nWspółrzędne w układzie kartezjańsim:")
print("1. Wektor A -", vectorA.getComponents())
print("2. Wektor B -", vectorB.getComponents())
print("3. Wektor C -", vectorC.getComponents())

print("\nWspółrzędne biegunowe dla Wektora A")
print("Długość:", vectorA.abs())
print("Kąt: ", vectorA.getAngle())

print("\nIloczyny skalarne")
print("Wektor A ⋅ wektor B:", vectorA.cdot(vectorB))
print("Wektor B ⋅ wektor C:", vectorB.cdot(vectorC))
print("Wektor C ⋅ wektor A:", vectorA.cdot(vectorC))

print("\nIloczyny wektorowe (w formie współrzędnych kartezjańskich)")
vectorA3d = Vector3DDecorator(Vector2D(4, 4), 0)
print("Wektor A x wektor B:", vectorA3d.cross(vectorB))
print("Wektor B x wektor C:", vectorB.cross(vectorC))
print("Wektor C x wektor A:", vectorA3d.cross(vectorC))