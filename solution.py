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
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[0.4, 0.2, 0.8])
        
        pyrosim.Send_Joint(name="Torso_LeftThigh", parent="Torso", child="LeftThigh", 
                          type="revolute", position=[0.1, 0, 1.1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LeftThigh", pos=[0, 0, -0.3], size=[0.15, 0.15, 0.6])
        
        pyrosim.Send_Joint(name="LeftThigh_LeftShin", parent="LeftThigh", child="LeftShin", 
                          type="revolute", position=[0, 0, -0.6], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LeftShin", pos=[0, 0, -0.3], size=[0.12, 0.12, 0.6])
        
        pyrosim.Send_Joint(name="LeftShin_LeftFoot", parent="LeftShin", child="LeftFoot", 
                          type="revolute", position=[0, 0, -0.6], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LeftFoot", pos=[0, -0.2, 0], size=[0.15, 0.4, 0.1])
        

        pyrosim.Send_Joint(name="Torso_RightThigh", parent="Torso", child="RightThigh", 
                          type="revolute", position=[-0.1, 0, 1.1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="RightThigh", pos=[0, 0, -0.3], size=[0.15, 0.15, 0.6])
        
        pyrosim.Send_Joint(name="RightThigh_RightShin", parent="RightThigh", child="RightShin", 
                          type="revolute", position=[0, 0, -0.6], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="RightShin", pos=[0, 0, -0.3], size=[0.12, 0.12, 0.6])
        
        pyrosim.Send_Joint(name="RightShin_RightFoot", parent="RightShin", child="RightFoot", 
                          type="revolute", position=[0, 0, -0.6], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="RightFoot", pos=[0, -0.2, 0], size=[0.15, 0.4, 0.1])
        
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        sensor_links = ["Torso", "LeftThigh", "LeftShin", "LeftFoot", 
                       "RightThigh", "RightShin", "RightFoot"]
        
        for i, linkName in enumerate(sensor_links):
            pyrosim.Send_Sensor_Neuron(name=i, linkName=linkName)

        motor_joints = ["Torso_LeftThigh", "LeftThigh_LeftShin", "LeftShin_LeftFoot",
                       "Torso_RightThigh", "RightThigh_RightShin", "RightShin_RightFoot"]
        
        for i, jointName in enumerate(motor_joints):
            pyrosim.Send_Motor_Neuron(name=i + len(sensor_links), jointName=jointName)

        for currentRow in range(len(sensor_links)):
            for currentColumn in range(len(motor_joints)):
                pyrosim.Send_Synapse(
                    sourceNeuronName=currentRow,
                    targetNeuronName=currentColumn + len(sensor_links),
                    weight=self.weights[currentRow][currentColumn]
                )
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