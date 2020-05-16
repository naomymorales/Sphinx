#@authors: Anel Martinez, Naomy Morales, Julibert Diaz, Angel Hernandez
#Sphinx Programming Language

import string

from sympy import *
import numpy as np
import math

#Math Functions


#Transforms cartesian coordinates to polar coordinates
def Cartersian_To_Polar(x_Coordinate, y_Coordinate):
    x = x_Coordinate
    y = y_Coordinate
    r = math.sqrt(x * x + y * y)
    theta = math.atan2(y, x)
    return r, theta

#Transforms polar coordinates to cartesian coordinates
def Polar_To_Cartersian(r_Coordenate, theta_Coordenate):
    r = r_Coordenate
    theta = theta_Coordenate
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y

#Converts degrees to radians
def Degrees_To_Radians(degrees):
    radians = degrees * (math.pi/180)
    return radians
#Converts radians to degrees
def Radians_To_Degrees(radians):
    degrees = radians * (180/math.pi)
    return degrees

#Calculates the magnitude of a 2d vector
def Magnitude(x, y):
    return math.sqrt((x * x) + (y * y))

#Calculates the magnitude of a 3d vector
def Magnitude_With_3_Variables(x, y, z):
    return math.sqrt((x * x) + (y * y) + (z * z))

#The distance between two points
def Distance_Between_Two_Points(x1, y1, x2, y2):
    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))

#Evaluates a polynomial
def Polynomial(a, b, c, x):
    return np.polyval((a, b, c), x)

#Quadratic function
def Quadratic(a, b, c):
    inerSQRT = (b * b) - 4 * a * c
    result1 = (-b + math.sqrt(inerSQRT)) // (2 * a)
    result2 = (-b - math.sqrt(inerSQRT)) // (2 * a)
    return result1, result2

# Calculates summations
def Summation(n, a, b, c):
    # np.polyval([a, b, c], x)
    # np.polyval([3,0,1], 5)
    # 3 * 5**2 + 0 * 5**1 + 1
    summation = 0
    for i in range(1, n + 1):
        summation += Polynomial((a, b, c), i)  # shorthand for summation = summation + i
    return summation

#Calculates a factorial
def Factorial(n):
    if n == 1:
        return 1
    else:
        return Factorial(n - 1) * n

# Calculates the volumeof different shapes
def Volume(shape, a, b, c):
    if shape.tolower() == "sphere":
        return (4 * math.pi * a**3)/3
    elif shape.tolower() == "cone":
        return (math.pi * a**2 * b)/3
    elif shape.tolower() == "cube":
        return a**3
    elif shape.tolower() == "cylinder":
        return math.pi * a**2 *b
    elif shape.tolower() == "square pyramid":
        return (a**2 * b)/3
    elif shape.tolower() == "tube":
        return (math.pi * (a**2 - b**2))/4
    elif shape.tolower() == "capsule":
        return (4 * math.pi * a**3)/3 + (math.pi * a**2 * b)

# sphere, a is radius
# cone, a is base radius, b is height
# cube, a is edge length
# cylinder, a is base radius, b is height
# square pyramid, a is base edge, b is height
# tube, a is outer diameter, b is inner diameter, c is length
# square capsule, a is base radius, b is height

#Calculates surface area of a shape
def SurfaceArea(shape, a, b, c):
    if shape.tolower() == "ball":
        return 4 * math.pi * a**2
    elif shape.tolower() == "cone":
        return (math.pi * a) + (math.pi * math.sqrt(a**2 + b**2))
    elif shape.tolower() == "cube":
        return 6 * a ** 2
    elif shape.tolower() == "cylinder":
        return (math.pi * a ** 2) * 2 + (2 * math.pi * a * b)
    elif shape.tolower() == "square pyramid":
        return (a ** 2) + (2 * a * math.sqrt((a / 2) ** 2 + b ** 2))
    elif shape.tolower() == "tube":
        return (2 * math.pi * (a**2 - b**2)) + (2 * math.pi * c * (a + b))
    elif shape.tolower() == "capsule":
        return (2 * math.pi * a ** 2) * 2 + (2 * math.pi * a * b)
# ball, a is radius
# cone, a is base radius, b is height
# cube, a is length
# cylinder, a is radius, b is height
# square pyramid, a is base edge, b is height
# tube, a is big radius, b is small radius, c is height
# square capsule, a is base radius, b is height

#Derivative of an equation
def newderivative(eq, *args):

    if len(args) == 0:
        eq = diff(eq)
    for sym in args:
        eq = diff(eq, sym)
    return eq

#Integration of an equation
def newintegration(eq, *args):
    if len(args) == 0:
        eq = integrate(eq)
    for tups in args:
        eq = integrate(eq, tups)
    return eq

#Formating an equation
def formateq(eq):
    if isinstance(eq, str):
        tired = str(eq)
        tired.replace("^", "**")
        return str(tired)
#Reformatting an equation
def reformateq(eq):
    if isinstance(eq, str):
        tired = str(eq)
        tired = tired.replace("**", "^")
        return tired

#Summations
def summation(eq, lower, upper, sym):
    sumtotal = 0
    sumexpr = sympify(eq)
    while lower <= upper:
        newexpr = sumexpr.subs(sym, lower)
        sumtotal = sumtotal + newexpr
        lower += 1
    return sumtotal

#Defining a product
def productnotation(eq, lower, upper, sym):
    prodtotal = 1
    sumexpr = sympify(eq)
    while lower <= upper:
        newexpr = sumexpr.subs(sym, lower)
        prodtotal = prodtotal * newexpr
        lower += 1
    return prodtotal

#Calculates de limits
def limits(eq, sym, sym0, side=None):
    if side is None:
        return limit(eq, sym, sym0)
    else:
        return limit(eq, sym, sym0, side)

#For testing purposes
'''
print("derivations testing\n")
# parameters: equation, *symbols
print(newderivative('1/(x**2)'))
# If there's more than one variable in the exp, the variable(s) of differentiation must be supplied to differentiate
print(newderivative('4*x*2*y*2', symbols('x')))
print('\nIntegrating testing\n')
# parameters: equation, *symbols
print('indefinite integral ', newintegration('2',symbols('x')))
# parameters: equation, *tuple(symbol, lowerbound, upperbound)
print('definite integral ', newintegration('2*x', (symbols('x'), 0, 2)))
# If the integrand contains more than one free symbol, an integration variable should be supplied explicitly
# parameters: equation, *symbols
print('indefinite integral ', newintegration('2*x*2*y + 2*x*y*2', symbols('x'), symbols('y')))
# parameters: equation, *tuple(symbol, lowerbound, upperbound)
print('definite integral ', newintegration('2*x*2*y + 2*x*y*2', (symbols('x'), 0, 2), (symbols('y'), 0, 2)))
# variable to be replaced must be initialized as a symbol and sent as a parameter for these methods to work
# parameters: equation, lowerbound, upperbound, symbol
print('\ntesting summation\n')
print(summation('x**2', 0, 6, symbols('x')))
print('\ntesting product notation\n')
print(productnotation('x**2', 1, 6, symbols('x')))
print('\ntesting limits\n')
# parameters: equation, x, x0, side to evaluate
print(limits('1/x', symbols('x'), 0, '+'))
print(limits('1/x', symbols('x'), 'inf'))
# testing string replacing for exponent
print('\ntesting formatting\n')
str1 = "4x^2"
print(str1.replace("^", "**"))
print(formateq("4x^2"))
'''