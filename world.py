import pybullet as p
import pyrosim.pyrosim as pyrosim

class WORLD:
    def __init__(self):
        self.planeId = p.loadURDF("plane.urdf")
        #later you might have t remove self.worldId and rather just load it 
        self.worldId = p.loadSDF("world.sdf")