# np.save("data/targetAngles_back.npy", c.targetAngles_back)
# np.save("data/targetAngles_front.npy", c.targetAngles_front)

# np.save("data/backLegSensorValues.npy", backLegSensorValues)
# np.save("data/frontLegSensorValues.npy", frontLegSensorValues)

from simulation import SIMULATION
simulation = SIMULATION()
simulation.Run()