
# Given a supply of 5 and 7 cent stamps. Is there a lower bound, after which all denominations of stamps can be produced?

from z3 import *

s = SolverFor("LRA") # Quantified Linear Integer Arithmetic
x = Real('x')
y = Real('y')
u = Real('u')
v = Real('v')
a = 5.0
b = 7.0
s.add(ForAll(u, Implies(u >= v,
                        Exists([x,y], And(x >= 0, y >= 0, u == a*x + b*y)))))
print(s.check())
print(s.model())

