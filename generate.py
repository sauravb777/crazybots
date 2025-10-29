import pyrosim.pyrosim as pyrosim

x,y,z = 0, 0, 0.5

pyrosim.Start_SDF("boxes.sdf")

for k in range(5):
    x=0
    for j in range(5):
        length,width,height = 1,1,1
        z=0.5
        for i in range(10):
            pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length, width, height])
            length,width,height = 0.9 * length, 0.9 * width, 0.9 * height
            z=z+1
        x=x+1
    y=y+1
            
pyrosim.End()