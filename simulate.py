import sys

from simulation import SIMULATION

if __name__ == "__main__":
    directOrGUI = sys.argv[1]
    solutionID = int(sys.argv[2])
    
    simulation = SIMULATION(directOrGUI, solutionID)
    simulation.Run()
    simulation.Get_Fitness()