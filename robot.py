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
        
        # Store initial position for distance calculation
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
        # Get current position and orientation
        basePosition, baseOrientation = p.getBasePositionAndOrientation(self.robotId)
        
        # Convert quaternion to Euler angles for stability measurement
        euler = p.getEulerFromQuaternion(baseOrientation)
        roll, pitch, yaw = euler
        
        # Calculate forward movement (x-direction)
        forward_distance = basePosition[0] - self.initialPosition[0]
        
        # HEAVILY PENALIZE BACKWARD MOVEMENT
        backward_penalty = 0
        if forward_distance < 0:  # If moving backwards
            backward_penalty = abs(forward_distance) * 20  # Heavy penalty
        
        # Calculate stability (penalize tilting)
        stability_penalty = abs(roll) + abs(pitch)
        
        # Calculate height penalty (should stay around initial height)
        height_penalty = abs(basePosition[2] - self.initialPosition[2])
        
        # Check if feet are making contact (good for walking)
        foot_contact_bonus = 0
        if "LeftFoot" in self.sensors and len(self.sensors["LeftFoot"].values) > 0:
            # Reward if feet are touching ground
            left_foot_contact = sum(1 for val in self.sensors["LeftFoot"].values[-100:] if val == 1)
            right_foot_contact = sum(1 for val in self.sensors["RightFoot"].values[-100:] if val == 1)
            foot_contact_bonus = (left_foot_contact + right_foot_contact) * 0.01
        
        # Combined fitness function - REWARD FORWARD, PENALIZE BACKWARD
        fitness = (forward_distance * 10) - backward_penalty - (stability_penalty * 5) - (height_penalty * 2) + foot_contact_bonus
        
        # Additional forward progress bonus
        if forward_distance > 0.5:  # If moved forward significantly
            fitness += 20
        
        # Penalize falling over completely
        if basePosition[2] < 0.5:  # If torso is too low
            fitness -= 50
        
        # Ensure minimum fitness
        fitness = max(fitness, 0.1)
        
        tmp = f"tmp{self.myID}.txt"
        final = f"fitness{self.myID}.txt"
        with open(tmp, "w") as f:
            f.write(str(fitness))
        os.replace(tmp, final)
        return fitness