import numpy as np
from matplotlib import pyplot as plt


TTT = []
To = 20 + 273
for t in range(15 * 60):
    TTT.append(To + ((530 - 20) / np.pi * 2) * np.arctan(t/70))

plt.figure()
plt.plot(range(15 * 60), TTT)
plt.show()