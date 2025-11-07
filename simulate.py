import sys

from simulation import SIMULATION

directOrGUI = sys.argv[1] 
myID = int(sys.argv[2])
simulation = SIMULATION(directOrGUI)
simulation.Run()
simulation.Get_Fitness()