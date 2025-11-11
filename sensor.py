import pyrosim.pyrosim as pyrosim


class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = []
    
    def Get_Value(self, t):
        value = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        if len(self.values) <= t:
            self.values.append(value)
        else:
            self.values[t] = value