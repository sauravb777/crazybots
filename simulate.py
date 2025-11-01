import pybullet as p
import numpy as np
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time 

amplitude_back, frequency_back, phaseOffset_back = np.pi/4, 6, np.pi/3
amplitude_front, frequency_front, phaseOffset_front = np.pi/4, 1000, 0

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

p.setGravity(0,0,-9.8)

robotId = p.loadURDF("body.urdf")
planeId = p.loadURDF("plane.urdf")
p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = np.zeros(1000)
frontLegSensorValues = np.zeros(1000)

steps = 1000
i_values = np.linspace(0, 2 * np.pi, steps)
targetAngles_back = amplitude_back * np.sin(frequency_back * i_values + phaseOffset_back)
targetAngles_front = amplitude_back * np.sin(frequency_back * i_values + phaseOffset_front)

np.save("data/targetAngles_back.npy", targetAngles_back)
np.save("data/targetAngles_front.npy", targetAngles_front)

for i in range(1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b'Torso_BackLeg', controlMode=p.POSITION_CONTROL, targetPosition=targetAngles_back[i], maxForce=25)   
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b'Torso_FrontLeg', controlMode=p.POSITION_CONTROL, targetPosition=targetAngles_front[i], maxForce=25)          
    time.sleep(1/180)

np.save("data/backLegSensorValues.npy", backLegSensorValues)
np.save("data/frontLegSensorValues.npy", frontLegSensorValues)

p.disconnect()

print(backLegSensorValues)
print(frontLegSensorValues)