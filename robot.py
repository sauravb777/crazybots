import os
import sys

import pybullet as p

import constants as c
import pyrosim.pyrosim as pyrosim
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR


class ROBOT:
    def __init__(self, robot_id=0):
        body_file = f"body{robot_id}.urdf"
        self.robotId = p.loadURDF(body_file)
        self.robot_id = robot_id
        
        pyrosim.Prepare_To_Simulate(self.robotId)

        myID = int(sys.argv[2])
        nndf_file = f"brain{myID}.nndf"
        self.nn = NEURAL_NETWORK(nndf_file)

        self.sensors = {}
        self.motors = {}
        self.initial_position = p.getBasePositionAndOrientation(self.robotId)[0]
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
            
    def Sense(self, t):
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
        current_position = basePositionAndOrientation[0]
        
        distance_traveled = current_position[0] - self.initial_position[0]
        
        myID = int(sys.argv[2])
        tmp_file = f"tmp{myID}_robot{self.robot_id}.txt"
        with open(tmp_file, "w") as f:
            f.write(str(distance_traveled))