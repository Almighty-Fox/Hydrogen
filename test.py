import numpy as np
from matplotlib import pyplot as plt


TTT = []
To = 20 + 273
To_end = 530 + 273
for t in range(15 * 60):
    # TTT.append(To + ((530 - 20) / np.pi * 2) * np.arctan(t/70))
    # TTT.append(To_end / (1 + np.exp(-t + np.log((To_end - To) / To))))  # сигмоида
    TTT.append(-2 * 0.6 / (200 + 273)**3 * t**3 + 3 * 0.6 / (200 + 273)**2 * t**2)
plt.figure()
plt.plot(range(15 * 60), TTT)
plt.show()