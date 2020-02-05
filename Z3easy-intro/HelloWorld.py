print("Hello World!")

# So, this is your standard Python. You can write things like this:


x = 3
y = 2
print(x > 2)
print(y < 10)
print(x + 2*y == 7)
print (x > 2, y < 10, (x + 2*y == 7))


#But what if you wanted to 
# solve(x > 2, y < 10, x + 2*y == 7)
# for a bunch of values? Moreover, you wanted to find out for which values it holds...
#the solve function belongs to z3
# without it, Python cannot really parse the constraint satisfaction problems:

# that is, if I remove the assignment to x and y, none of the above will work
