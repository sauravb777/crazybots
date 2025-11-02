import numpy as np
import pyrosim.pyrosim as pyrosim 

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = []
    
    def Get_Value(self, t):
        values = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        if len(self.values) <= t:
            self.values.append(values)
        else:
            self.values[t] = values
        
    def Save_Values(self):
        np.save(f"data/{self.linkName}_SensorValues.npy", self.values)