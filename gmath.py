import math
from display import *
from matrix import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    # a = calculate_ambient(ambient, areflect) + calculate_diffuse(light, dreflect, normal) + calculate_specular(light, sreflect, view, normal)
    # if (a > 255):
    #     return 255
    # return a
    a = calculate_ambient(ambient, areflect)
    b = calculate_diffuse(light, dreflect, normal)
    c = calculate_specular(light, sreflect, view, normal)
    d = [int(a[0] + b[0] + c[0]), int(a[1] + b[1] + c[1]), int(a[2] + b[2] + c[2])]
    return limit_color(d)

def calculate_ambient(alight, areflect):
    # m = alight
    # matrix_mult(areflect, m)
    # return m
    return [alight[0] * areflect[0], alight[1] * areflect[1], alight[2] * areflect[2]]

def calculate_diffuse(light, dreflect, normal):
    m = light[0]
    normalize(m)
    n = normal
    normalize(n)
    costheta = dot_product(m, n)
    # o = dreflect
    # matrix_mult(light[1], o)
    # matrix_mult(costheta, o)
    # return o
    return [dreflect[0] * light[1][0] * costheta, dreflect[1] * light[1][1] * costheta, dreflect[2] * light[1][2] * costheta] #unsure if this is correct

def calculate_specular(light, sreflect, view, normal):
    x, y, z = normal, light[0], view
    normalize(x)
    normalize(y)
    normalize(z)
    a = dot_product(x, y)
    #b = normalize(normal) #replace b with x
    c = [x[0] * a, x[1] * a, x[2] * a]
    #d = normalize(light) #replace d with y
    e = [2 * c[0] - y[0], 2 * c[1] - y[1], 2 * c[2] - y[2]]
    #print(e)
    #print(z)
    #f = [(dot_product(e[0], z[0])) ** 2, (dot_product(e[1], z[1])) ** 2, (dot_product(e[2], z[2])) ** 2]
    f = dot_product(e, z) ** 2
    return [sreflect[0] * light[1][0] * f, sreflect[1] * light[1][1] * f, sreflect[2] * light[1][2] * f]
    #return [sreflect[0] * light[1][0] * f[0], sreflect[1] * light[1][1] * f[1], sreflect[2] * light[1][2] * f[2]]
    # matrix_mult(dot_product(t, normalize(light[0])), t)
    # s = dot_product(2 * t - normalize(light[0]), normalize(view)) ** 2
    # u = sreflect
    # matrix_mult(light[1], u)
    # matrix_mult(s, u)
    # return u

def limit_color(color):
    final = color
    for x in final:
        if x > 255:
            x = 255
    return final

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N