# This file is a Demo of a simple NN verification approach, a la
# Safety Verification of Deep Neural Networks?Xiaowei Huang, Marta Kwiatkowska, Sen Wang and Min Wu, https://arxiv.org/pdf/1610.06940.pdf

import pandas as pd
import numpy as np

## We First Define a Perceptron ###

class Perceptron(object):
    """Perceptron classifier.

    Parameters
    ------------
    eta : float
      Learning rate (between 0.0 and 1.0)
    n_iter : int
      Passes over the training dataset.
    random_state : int
      Random number generator seed for random weight
      initialization.

    Attributes
    -----------
    w_ : 1d-array
      Weights after fitting.
    errors_ : list
      Number of misclassifications (updates) in each epoch.

    """
    def __init__(self, eta=0.01, n_iter=50, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state

    def fit(self, X, y):
        """Fit training data.

        Parameters
        ----------
        X : {array-like}, shape = [n_samples, n_features]
          Training vectors, where n_samples is the number of samples and
          n_features is the number of features.
        y : array-like, shape = [n_samples]
          Target values.

        Returns
        -------
        self : object

        """
        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=1 + X.shape[1])
        self.errors_ = []

        for _ in range(self.n_iter):
            errors = 0
            for xi, target in zip(X, y):
                update = self.eta * (target - self.predict(xi))
                self.w_[1:] += update * xi
                self.w_[0] += update
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self

    def net_input(self, X):
        """Calculate net input"""
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def predict(self, X):
        """Return class label after unit step"""
        return np.where(self.net_input(X) >= 0.0, 1, -1)


""" Loading the "and" data set """

andp = pd.read_csv('andp.csv', header=None)
print("And Data set: ")
print(andp)
X = andp.iloc[0:4, [0, 1]].values
y = andp.iloc[0:4, [2]].values


print("We now train the Neuron:")
ppn = Perceptron(eta=0.1, n_iter=10)
res = ppn.fit(X,y)
print("Obtained model: ", res)
print("Weights after training: ", ppn.w_)


print("We now call Z3 to do verification: ")
""" Scenario: proving Perceptron is robust against "adversarial attacks".
We do this by defining a range of permissible inputs to the Perceptron, and then
showing that Perceptron is robust in this range 
 """

from z3 import *

""" We now start setting up verification conditions for Z3:

 1. X2 is a 2x2 array of reals: """

X2 = [ Real("x_%s" % (i+1)) for i in range(2) ]

"""  
 2. Elements of X2 are in the interval [0.5, 1.5] (conditions cond1 and cond2)
"""

x1 = X2[0]
x2 = X2[1]
cond1 = 0.4 <= X2[0], X2[0] <= 1.5
cond2 = 0.4 <= X2[1], X2[1] <= 1.5

"""
2.1. Another possibility: -- Eucledian distance from our ideal example [1,1] """

condd = (1 - X2[0])**2 + (1 - X2[1])**2 <= 0.5


""" 
  3. We explore a finite number of reals in the interval, by setting up a ladder. 
  In good papers, there are theorems showing why the defined ladder is "covering" for the interval
   epsilon is a ladder step: """

epsilon = 0.08
ladder = [x*0.1 for x in range(1,100)]
print("The ladder is: ", ladder)



""" Conditions cond5 and cond6 define the range of values for "adversarial attacks" """
cond5 = Or ([X2[0] == l * epsilon for l in ladder])
cond6 = Or ([X2[1] == l * epsilon for l in ladder])

"""Problem 1: weak connection between Python and Z3: The below will not work"""
#cond3 = ForAll ([x1,x2],  (ppn.predict((x1,x2)) == 1) )
"""  .Z3Exception: Symbolic expressions cannot be cast to concrete Boolean values.
 """

"""Problem 2: fragile Python types and Z3: check the work with decimals on
line 156!"""

set_option(rational_to_decimal=True)

"""We add all these conditions to the Z3 solver"""

s = Solver()
s.add(cond6)
s.add(cond5)
s.add(condd)
"s.add(cond1)"
"s.add(cond2)"


count = 0
while s.check() == sat:
    m = s.model()
    print(m)
    r3 = [simplify(m.evaluate(X2[i])).as_decimal(20) for i in range(2)]
    print_matrix(r3)
    pred3 = ppn.predict(list(map(float, r3)))
    print("Perceptron predicts: ", pred3)
    if pred3 == 1:
        print("all is ok")
    else:
        print("Counter-example found!")
        break
    s.add(Or(x1 != s.model()[x1], x2 != s.model()[x2])) # prevent next model from using the same assignment as a previous model
    count = count + 1
    print("Checked generated inputs: ", count)






