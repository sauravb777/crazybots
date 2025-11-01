import numpy as np
import pyrosim.pyrosim as pyrosim 
import pybullet as p
import constants as c


class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.motorValues = []
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.amplitude
        # self.frequency = c.frequency
        self.phaseOffset = c.phaseOffset
        
        if self.jointName == b'Torso_BackLeg':
            self.frequency = c.frequency
        else:
            self.frequency = c.frequency/2
        
        i = np.linspace(0, 2 * np.pi, 1000) 
        self.motorValues = self.amplitude * np.sin(self.frequency * i + self.phaseOffset)
    
    def Set_Value(self, robot, t):
        pyrosim.Set_Motor_For_Joint(bodyIndex=robot.robotId, jointName=self.jointName, controlMode=p.POSITION_CONTROL, targetPosition=self.motorValues[t], maxForce=50)
    
    def Save_Values(self):
        np.save(f"data/{self.jointName}_MotorValues.npy", self.motorValues)
    
            