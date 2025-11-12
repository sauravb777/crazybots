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
        
        self.initialPosition = p.getBasePositionAndOrientation(self.robotId)[0]

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
                desiredAngle = self.nn.Get_Value_Of(neuronName) * 0.4
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)

    def Get_Fitness(self):
        basePosition, baseOrientation = p.getBasePositionAndOrientation(self.robotId)
        
        euler = p.getEulerFromQuaternion(baseOrientation)
        roll, pitch, yaw = euler
    
        forward_distance = basePosition[0] - self.initialPosition[0]
        
        backward_penalty = 0
        if forward_distance < 0:  
            backward_penalty = abs(forward_distance) * 20  
        
        stability_penalty = abs(roll) + abs(pitch)
        
        height_penalty = abs(basePosition[2] - self.initialPosition[2])
        
        foot_contact_bonus = 0
        if "LeftFoot" in self.sensors and len(self.sensors["LeftFoot"].values) > 0:
            left_foot_contact = sum(1 for val in self.sensors["LeftFoot"].values[-100:] if val == 1)
            right_foot_contact = sum(1 for val in self.sensors["RightFoot"].values[-100:] if val == 1)
            foot_contact_bonus = (left_foot_contact + right_foot_contact) * 0.01
        
        fitness = (forward_distance * 10) - backward_penalty - (stability_penalty * 5) - (height_penalty * 2) + foot_contact_bonus
        
        if forward_distance > 0.5:  
            fitness += 20
        
        if basePosition[2] < 0.5:  
            fitness -= 50
        
        fitness = max(fitness, 0.1)
        
        tmp = f"tmp{self.myID}.txt"
        final = f"fitness{self.myID}.txt"
        with open(tmp, "w") as f:
            f.write(str(fitness))
        os.replace(tmp, final)
        return fitness