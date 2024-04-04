import numpy as np
import matplotlib.pyplot as plt

x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
wer_tiny_flash = np.array([0.20104, 0.22087, 0.47024, 0.43111, 0.14902, 0.2, 0.45222, 0.11304, 0.13365, 0.19693])

plt.plot(x, wer_tiny_flash, label='Tiny Flash')
plt.show()