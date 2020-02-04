print("Hello World!")

# from z3 import *

# solve(x > 2, y < 10, x + 2*y == 7) #the solve function belongs to z3
# without it, Python cannot really parse the constraint satisfaction problems:

x = 3
y = 2
print(x > 2)
print(y < 10)
print(x + 2*y == 7)
print (x > 2, y < 10, (x + 2*y == 7))

# that is, if I remove the assignment to x and y, none of the above will work
