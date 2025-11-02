import numpy as np
import pyrosim.pyrosim as pyrosim 
import pybullet as p
import constants as c


class MOTOR:
    def __init__(self, jointName):
        if isinstance(jointName, bytes):
            jointName = jointName.decode("utf-8")
        self.jointName = jointName
        self.motorValues = []
    
    def Set_Value(self, robotId, desiredAngle):
        pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=self.jointName, controlMode=p.POSITION_CONTROL, targetPosition=desiredAngle, maxForce=50)

    
            