from z3 import *

"""This file illustrates the use of models and direct reference to solvers"""

x = Real('x')
y = Real('y')
s = Solver()
s.add(x + y > 5, x > 2, y > 2)
print(s.check())
print(s.model())

# Now lets talk about quantifiers...

#s.add(ForAll( x, x < x+1))
#print(s.check())
#print(s.model())

