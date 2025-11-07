
import os
import sys

import pybullet as p

import constants as c
import pyrosim.pyrosim as pyrosim
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR


class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)

        myID = int(sys.argv[2])
        nndf_file = f"brain{myID}.nndf"
        self.nn = NEURAL_NETWORK(nndf_file)

        self.sensors = {}
        self.motors = {}
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    
    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
            
    def Sense(self,t):
        for sensor in self.sensors.values():
            sensor.Get_Value(t)
    
    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
            
    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
        
    
    def Think(self):
        self.nn.Update()
        
    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        x = basePositionAndOrientation[0][0]  
        y = basePositionAndOrientation[0][1] 

        fitness_value = -x - y 
        
        myID = int(sys.argv[2])
        tmp = f"tmp{myID}.txt"
        final = f"fitness{myID}.txt"

        with open(tmp, "w") as f:
            f.write(str(fitness_value))
        os.replace(tmp, final)

