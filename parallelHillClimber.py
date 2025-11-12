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
            self.Evolve_For_One_Generation(currentGeneration)

        self.Show_Best()

    def Evolve_For_One_Generation(self, generationIndex):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children, "DIRECT")
        self.Select()
        self.Print(generationIndex)

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

    def Print(self, generationIndex):
        for k in sorted(self.parents.keys()):
            parent_fitness = self.parents[k].fitness
            child_fitness = self.children[k].fitness
            print(f"  Parent: {parent_fitness:.4f}  Child: {child_fitness:.4f}")
        print("\n")

    def Show_Best(self):
        best_parent = max(self.parents.values(), key=lambda x: x.fitness)
        print(f"Best solution: ID {best_parent.myID}, Fitness: {best_parent.fitness:.4f}")
        best_parent.Start_Simulation("GUI")