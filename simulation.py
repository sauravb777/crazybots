import os
import time

import pybullet as p
import pybullet_data

import constants as c
import pyrosim.pyrosim as pyrosim
from robot import ROBOT
from world import WORLD


class SIMULATION:
    def __init__(self, directOrGUI):
        self.directOrGUI = directOrGUI
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setGravity(0,0,-9.8)
        self.world = WORLD()
        
        self.robots = []
        for i in range(c.swarmSize):
            robot = ROBOT(robot_id=i)
            self.robots.append(robot)
        
    def Run(self):
        steps = 2000
        for t in range(steps):
            p.stepSimulation()
            for robot in self.robots:
                robot.Sense(t)
                robot.Think()
                robot.Act()
            if self.directOrGUI == "GUI":
                time.sleep(1/120)
            
    def Get_Fitness(self):
        best_fitness = -float('inf')
        
        for robot in self.robots:
            robot.Get_Fitness()
        
        import sys
        myID = int(sys.argv[2])
        for i in range(len(self.robots)):
            tmp_file = f"tmp{myID}_robot{i}.txt"
            if os.path.exists(tmp_file):
                with open(tmp_file, "r") as f:
                    fitness = float(f.read().strip())
                    if fitness > best_fitness:
                        best_fitness = fitness
                os.remove(tmp_file)
        
        with open(f"fitness{myID}.txt", "w") as f:
            f.write(str(best_fitness))
    
    def __del__(self):
        p.disconnect()