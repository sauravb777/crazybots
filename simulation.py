import time

import pybullet as p
import pybullet_data

from robot import ROBOT


class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI
        self.solutionID = solutionID
        
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
            p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
            
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        
        self.planeId = p.loadURDF("plane.urdf")
        
        
        self.robot = ROBOT(solutionID)
        
    def Run(self):
        for t in range(1000):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act()
            if self.directOrGUI == "GUI":
                time.sleep(1/60)
            
    def Get_Fitness(self):
        self.robot.Get_Fitness()
    
    def __del__(self):
        p.disconnect()