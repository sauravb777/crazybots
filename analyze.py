import numpy as np
import matplotlib.pyplot as plt

# backLegSensorValues = np.load("data/backLegSensorValues.npy")
# frontLegSensorValues = np.load("data/frontLegSensorValues.npy")

# plt.plot(backLegSensorValues, label = "Back Leg", linewidth = 3)
# plt.plot(frontLegSensorValues, label = "Front Leg")

plt.xlabel("Time step")
plt.ylabel("Target angle (radians)")

targetAngles_back = np.load("data/targetAngles_back.npy")
targetAngles_front = np.load("data/targetAngles_front.npy")


plt.plot(targetAngles_front, label="Front leg motor values", linewidth=5)  
plt.plot(targetAngles_back, label="Back leg motor values", linewidth=1) 

plt.legend()
plt.show()