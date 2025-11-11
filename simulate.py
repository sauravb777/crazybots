import sys

from simulation import SIMULATION

if __name__ == "__main__":
    if len(sys.argv) > 2:
        directOrGUI = sys.argv[1]
        myID = int(sys.argv[2])
    else:
        directOrGUI = "GUI"
        myID = 0
        
    simulation = SIMULATION(directOrGUI, myID)
    simulation.Run()
    simulation.Get_Fitness()