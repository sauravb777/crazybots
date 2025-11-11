import os
import random
import subprocess
import time

import numpy as np

import constants as c
import pyrosim.pyrosim as pyrosim


class SOLUTION:
    def __init__(self, myID):
        self.myID = myID
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2 - 1
        self.fitness = 0

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[0, 4, 0.5], size=[1,1,1])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0, 0.5, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0, -0.5, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[0.5, 0, 1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[-0.5, 0, 1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute", position=[0, 1.0, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute", position=[0, -1.0, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute", position=[1.0, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute", position=[-1.0, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        sensor_links = ["Torso", "FrontLeg", "BackLeg", "LeftLeg", "RightLeg", "FrontLowerLeg", "BackLowerLeg", "LeftLowerLeg", "RightLowerLeg"]
        for i, linkName in enumerate(sensor_links):
            pyrosim.Send_Sensor_Neuron(name=i, linkName=linkName)
        motor_joints = ["Torso_FrontLeg", "Torso_BackLeg", "Torso_LeftLeg", "Torso_RightLeg", "FrontLeg_FrontLowerLeg", "BackLeg_BackLowerLeg", "LeftLeg_LeftLowerLeg", "RightLeg_RightLowerLeg"]
        for i, jointName in enumerate(motor_joints):
            pyrosim.Send_Motor_Neuron(name=i + len(sensor_links), jointName=jointName)
        for currentRow in range(len(sensor_links)):
            for currentColumn in range(len(motor_joints)):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn + len(sensor_links), weight=self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):
        row = random.randint(0, c.numSensorNeurons - 1)
        col = random.randint(0, c.numMotorNeurons - 1)
        self.weights[row, col] = random.random() * 2 - 1
    
    def Start_Simulation(self, directOrGUI):
        self.Create_Body()
        self.Create_World()
        self.Create_Brain()
        cmd = ["python", "simulate.py", directOrGUI, str(self.myID)]
        if directOrGUI == "DIRECT":
            self.proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(cmd)
    
    def Wait_For_Simulation_To_End(self):
        if hasattr(self, 'proc'):
            self.proc.wait()
        filename = f"fitness{self.myID}.txt"
        waited = 0
        while not os.path.exists(filename):
            time.sleep(0.1)
            waited += 0.1
            if waited > 15:
                self.fitness = 0
                return
        try:
            with open(filename, "r") as f:
                self.fitness = float(f.read().strip())
            os.remove(filename)
        except:
            self.fitness = 0