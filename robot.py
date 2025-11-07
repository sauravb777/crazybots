import os
import sys

import pybullet as p

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

        if os.path.exists(nndf_file):
            os.remove(nndf_file)

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
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
        
    
    def Think(self):
        self.nn.Update()
        self.nn.Print()
        
    def Get_Fitness(self):
        x = p.getLinkState(self.robotId, 0)[0][0]
        myID = int(sys.argv[2])
        tmp = f"tmp{myID}.txt"
        final = f"fitness{myID}.txt"

        with open(tmp, "w") as f:
            f.write(str(x))
        os.replace(tmp, final)
