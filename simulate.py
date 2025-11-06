import sys

from simulation import SIMULATION

directOrGUI = sys.argv[1] if len(sys.argv) > 1 else "GUI"
simulation = SIMULATION(directOrGUI)
simulation.Run()
simulation.Get_Fitness()