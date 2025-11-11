import time

import pybullet as p
import pybullet_data

from robot import ROBOT
from world import WORLD


class SIMULATION:
    def __init__(self, directOrGUI, myID):
        self.directOrGUI = directOrGUI
        self.myID = myID
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
            p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)
        self.world = WORLD()
        self.robot = ROBOT(myID)
        
    def Run(self):
        steps = 5000
        for t in range(steps):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act()
            if self.directOrGUI == "GUI":
                time.sleep(1/120)
            
    def Get_Fitness(self):
        self.robot.Get_Fitness()
    
    def __del__(self):
        p.disconnect()
