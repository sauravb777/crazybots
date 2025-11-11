from pyrosim.commonFunctions import Save_Whitespace


class JOINT: 
    def __init__(self,name,parent,child,type,position,jointAxis="0 1 0", limit_lower="-3.14159", limit_upper="3.14159"):
        self.name = name
        self.parent = parent
        self.child  = child
        self.type   = type
        self.position = position
        self.jointAxis = jointAxis
        self.limit_lower = limit_lower
        self.limit_upper = limit_upper
        self.depth = 1

    def Save(self,f):
        Save_Whitespace(self.depth,f)
        f.write('<joint name="' + self.name + '" type="' + self.type + '">' + '\n')
        Save_Whitespace(self.depth,f)
        f.write('   <parent link="' + self.parent + '"/>' + '\n')
        Save_Whitespace(self.depth,f)
        f.write('   <child  link="' + self.child  + '"/>' + '\n')
        Save_Whitespace(self.depth,f)
        originString = f"{self.position[0]} {self.position[1]} {self.position[2]}"
        f.write('   <origin rpy="0 0 0" xyz="' + originString + '" />\n')
        Save_Whitespace(self.depth,f)
        f.write(f'   <axis xyz="{self.jointAxis}"/>\n')
        Save_Whitespace(self.depth,f)
        f.write(f'   <limit effort="0.0" lower="{self.limit_lower}" upper="{self.limit_upper}" velocity="0.0"/>\n')
        Save_Whitespace(self.depth,f)
        f.write('</joint>' + '\n')