
# This file illustrates the use of quantifiers in Z3 Theories

# Given a supply of 5 and 7 cent stamps. Is there a lower bound, after which all denominations of stamps can be produced?

from z3 import *

# Firstly, we can specify the Z3 theories we want to call
s = SolverFor("LRA") # Quantified Linear Real Arithmetic
x = Int('x')
y = Int('y')
u = Int('u')
v = Int('v')
a = 5.0
b = 7.0

#Then we can use quantifiers to reason in those theories: 

s.add(ForAll(u, Implies(u >= v,
                        Exists([x,y], And(x >= 0, y >= 0, u == a*x + b*y)))))
print(s.check())
print(s.model())

