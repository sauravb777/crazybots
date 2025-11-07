import os

import numpy as np

import constants as c
from solution import SOLUTION


class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("del fitness*.txt 2>nul")
        os.system("del brain*.nndf 2>nul")

        self.parents = {}
        self.nextAvailableID = 0 

        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        print("Evaluating initial population (DIRECT)...")
        self.Evaluate(self.parents, "DIRECT")

        for g in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation(g)

        print("Final evolved population (GUI)...")
        self.Show_Best()

    def Evolve_For_One_Generation(self, gen):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children, "DIRECT")
        self.Select()
        self.Print(gen)

    def Spawn(self):
        self.children = {}
        for k in sorted(self.parents.keys()):
            parent = self.parents[k]
            child = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
            child.weights = np.copy(parent.weights)
            self.children[k] = child

    def Mutate(self):
        for k in self.children:
            self.children[k].Mutate()

    def Evaluate(self, solutions, mode):
        for k in sorted(solutions.keys()):
            solutions[k].Start_Simulation(mode)
        for k in sorted(solutions.keys()):
            solutions[k].Wait_For_Simulation_To_End()


    def Select(self):
        for k in sorted(self.parents.keys()):
            if self.children[k].fitness < self.parents[k].fitness:
                self.parents[k] = self.children[k]

    def Print(self, generationIndex):
        print(f"\nGeneration {generationIndex} fitnesses")
        for k in sorted(self.parents.keys()):
            pfit = self.parents[k].fitness
            cfit = self.children[k].fitness
            print(f"Parent {k}: {pfit:.6f}    Child {k}: {cfit:.6f}")
        print("\n")

    def Show_Best(self):
        best = min(self.parents.values(), key=lambda s: s.fitness)
        print(f"Best solution ID {best.myID} fitness: {best.fitness}")
        best.Start_Simulation("GUI")
