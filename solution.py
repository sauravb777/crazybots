import os
import random

import numpy as np

import pyrosim.pyrosim as pyrosim


class SOLUTION:
    def __init__(self):
        self.weights = np.random.rand(3, 2) * 2 - 1
        self.fitness = None

    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

        os.system(f"python simulate.py {directOrGUI}")

        fitnessFile = open("fitness.txt", "r")
        fitnessString = fitnessFile.read().strip()
        fitnessFile.close()
        self.fitness = float(fitnessString)

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[0, 4, 0.5], size=[1,1,1])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[1.5, 0, 1.5], size=[1,1,1])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[1.0,0,1.0])
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0,-0.5], size=[1,1,1])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2.0,0,1.0])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5], size=[1,1,1])
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")

        for i, link in enumerate(["Torso", "BackLeg", "FrontLeg"]):
            pyrosim.Send_Sensor_Neuron(name=i, linkName=link)

        for i, joint in enumerate(["Torso_BackLeg", "Torso_FrontLeg"]):
            pyrosim.Send_Motor_Neuron(name=i+3, jointName=joint)

        for currentRow in range(3):
            for currentColumn in range(2):
                pyrosim.Send_Synapse(
                    sourceNeuronName=currentRow,
                    targetNeuronName=currentColumn + 3,
                    weight=self.weights[currentRow][currentColumn]
                )
        pyrosim.End()

    def Mutate(self):
        row = random.randint(0, 2)
        col = random.randint(0, 1)
        self.weights[row, col] = random.random() * 2 - 1
        row = random.randint(0, 2)
        col = random.randint(0, 1)
        self.weights[row, col] = random.random() * 2 - 1
