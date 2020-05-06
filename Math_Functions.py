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

def Degrees_To_Radians(degrees):
    radians = degrees * (math.pi/180)
    return radians

def Radians_To_Degrees(radians):
    degrees = radians * (180/math.pi)
    return degrees

def Magnitude(x, y):
    return math.sqrt((x * x) + (y * y))

def Magnitude_With_3_Variables(x, y, z):
    return math.sqrt((x * x) + (y * y) + (z * z))

def Distance_Between_Two_Points(x1, y1, x2, y2):
    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
