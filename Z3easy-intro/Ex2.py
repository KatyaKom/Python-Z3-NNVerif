from z3 import *

x = Real('x')
y = Real('y')
s = Solver()
s.add(x + y > 5, x > 2, y > 2)
print(s.check())
print(s.model())


