import numpy as np

y = [2.57, 2.85, 2.08, 1.30, 1.88, 2.26, 2.19, 2.64, 1.67, 1.48]
y.sort()
x = [-1.28, -0.84, -0.52, -0.25, 0, 0.25, 0.52, 0.84, 1.28, 3]

xbar = np.mean(x)
ybar = np.mean(y)

numerator = 0
for i in range(len(x)):
    numerator = numerator + ((x[i] - xbar) * (y[i] - ybar))

denominator = 0
for i in range(len(x)):
    denominator = denominator + ((x[i] - xbar) ** 2)

b1 = numerator / denominator

print(b1)
print(ybar - (b1 * xbar))