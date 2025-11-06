import matplotlib.pyplot as plt
import numpy as np

plt.xlabel("Time step")
plt.ylabel("Target angle (radians)")

targetAngles_back = np.load("data/targetAngles_back.npy")
targetAngles_front = np.load("data/targetAngles_front.npy")


plt.plot(targetAngles_front, label="Front leg motor values", linewidth=5)  
plt.plot(targetAngles_back, label="Back leg motor values", linewidth=1) 

plt.legend()
plt.show()