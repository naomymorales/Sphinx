import math

def Cartersian_To_Polar(x_Coordinate, y_Coordinate):
    x = x_Coordinate
    y = y_Coordinate
    r = math.sqrt(x * x + y * y)
    theta = math.atan2(y, x)
    return r, theta

def Polar_To_Cartersian(r_Coordenate, theta_Coordenate):
    r = r_Coordenate
    theta = theta_Coordenate
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y

def Magnitude(x, y):
    return math.sqrt((x * x) + (y * y))

def Magnitude_With_3_Variables(x, y, z):
    return math.sqrt((x * x) + (y * y) + (z * z))