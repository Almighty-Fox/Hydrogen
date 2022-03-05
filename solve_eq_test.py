from scipy.optimize import fsolve


def my_function(h, b, k):
    return h ** 2 - 3 * h - b + k


b = 1
k = 2
a = fsolve(my_function, [-4, 33, 8], args=(b, k))
print(a)
print(1e-5*100000)

# print(fsolve(my_function, 1))
