import os

import constants as c
from solution import SOLUTION


class PARALLEL_HILL_CLIMBER:
    def __init__(self):
      
        os.system("del fitness*.txt 2>nul")
        os.system("del brain*.nndf 2>nul")
        os.system("del body.urdf 2>nul")
        os.system("del world.sdf 2>nul")

        self.parents = {}
        self.nextAvailableID = 0

        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents, "DIRECT")

        for currentGeneration in range(c.numberOfGenerations):
            print(f"Generation {currentGeneration}")
            self.Evolve_For_One_Generation()

        self.Show_Best()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children, "DIRECT")
        self.Select()
        self.Print()

    def Spawn(self):
        self.children = {}
        for k in self.parents:
            self.children[k] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
            self.children[k].weights = self.parents[k].weights.copy()

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Evaluate(self, solutions, mode):
        for solution in solutions.values():
            solution.Start_Simulation(mode)
        for solution in solutions.values():
            solution.Wait_For_Simulation_To_End()

    def Select(self):
        for k in self.parents:
            if self.children[k].fitness > self.parents[k].fitness:
                self.parents[k] = self.children[k]

    def Print(self):
        print("Fitness values:")
        for k in self.parents:
            print(f"  Parent: {self.parents[k].fitness:.4f}")

    def Show_Best(self):
        best_parent = max(self.parents.values(), key=lambda x: x.fitness)
        print(f"Best fitness: {best_parent.fitness:.4f}")
        best_parent.Start_Simulation("GUI")