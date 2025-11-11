import os

import numpy as np
import pybullet as p

import pyrosim.pyrosim as pyrosim
from motor import MOTOR
from sensor import SENSOR


class ROBOT:
    def __init__(self, myID):
        self.myID = myID
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        
        from pyrosim.neuralNetwork import NEURAL_NETWORK
        self.nn = NEURAL_NETWORK(f"brain{myID}.nndf")
        
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for sensor in self.sensors.values():
            sensor.Get_Value(t)

    def Think(self):
        self.nn.Update()

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * 0.5 
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)

    def Get_Fitness(self):
        lower_legs = ["FrontLowerLeg", "BackLowerLeg", "LeftLowerLeg", "RightLowerLeg"]
        
        if not all(leg in self.sensors for leg in lower_legs):
            fitness = 0
        else:
            min_length = min(len(self.sensors[leg].values) for leg in lower_legs)
            if min_length == 0:
                fitness = 0
            else:
                coordinated_jumps = 0
                for t in range(min_length):
                    all_airborne = all(self.sensors[leg].values[t] == -1 for leg in lower_legs)
                    if all_airborne:
                        coordinated_jumps += 1
                
                base_position, base_orientation = p.getBasePositionAndOrientation(self.robotId)
                max_height = base_position[2]
                
                torso_touching = 0
                if "Torso" in self.sensors and len(self.sensors["Torso"].values) > 0:
                    torso_touching = sum(1 for val in self.sensors["Torso"].values if val == 1)
                

                euler_angles = p.getEulerFromQuaternion(base_orientation)
                roll, pitch, yaw = euler_angles
                stability_penalty = abs(roll) + abs(pitch) 
                
                fitness = (coordinated_jumps * 10) + (max_height * 5) - (torso_touching * 2) - (stability_penalty * 3)
        
        tmp = f"tmp{self.myID}.txt"
        final = f"fitness{self.myID}.txt"
        with open(tmp, "w") as f:
            f.write(str(fitness))
        os.replace(tmp, final)
        return fitness