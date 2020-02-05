from z3 import *

"""This file illustrates the use of Z3 to find satisfiable assignments"""

x = Int('x')
y = Int('y')
solve(x > 2, y < 10, x + 2*y == 7)

z = Real('z')
solve(z > 4, z < 0)
