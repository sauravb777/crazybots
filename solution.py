import os
import random
import subprocess
import time

import numpy as np

import pyrosim.pyrosim as pyrosim


class SOLUTION:
    def __init__(self, myID):
        self.myID = myID
        self.weights = np.random.rand(3, 2) * 2 - 1
        self.fitness = None
        self.proc = None

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
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

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
    
    def Start_Simulation(self, directOrGUI):
        if not os.path.exists("body.urdf"):
            self.Create_Body()
        if not os.path.exists("world.sdf"):
            self.Create_World()

        brainfile = f"brain{self.myID}.nndf"
        if not os.path.exists(brainfile):
            self.Create_Brain()

        cmd = ["python", "simulate.py", directOrGUI, str(self.myID)]

        if directOrGUI == "DIRECT":
            DEVNULL = open(os.devnull, "wb")
            self.proc = subprocess.Popen(
                cmd, stdout=DEVNULL, stderr=DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            subprocess.call(cmd)

    
     
    def Wait_For_Simulation_To_End(self):
        filename = f"fitness{self.myID}.txt"

        while not os.path.exists(filename):
            time.sleep(0.01)


        with open(filename, "r") as f:
            self.fitness = float(f.read().strip())
        os.remove(filename)
