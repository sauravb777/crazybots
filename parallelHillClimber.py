import os

import constants as c
from solution import SOLUTION


class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        self.cleanup_files()
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def cleanup_files(self):
        for file in os.listdir('.'):
            if file.startswith('fitness') and file.endswith('.txt'):
                try: os.remove(file)
                except: pass
            if file.startswith('brain') and file.endswith('.nndf'):
                try: os.remove(file)
                except: pass
        for file in ['body.urdf', 'world.sdf']:
            if os.path.exists(file):
                try: os.remove(file)
                except: pass

    def Evolve(self):
        print("Initial evaluation...")
        self.Evaluate(self.parents, "DIRECT")
        for generation in range(c.numberOfGenerations):
            print(f"Generation {generation}")
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
        for key in self.parents:
            self.children[key] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
            self.children[key].weights = self.parents[key].weights.copy()

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Evaluate(self, solutions, mode):
        for solution in solutions.values():
            solution.Start_Simulation(mode)
        for solution in solutions.values():
            solution.Wait_For_Simulation_To_End()

    def Select(self):
        for key in self.parents:
            if self.children[key].fitness > self.parents[key].fitness:
                self.parents[key] = self.children[key]

    def Print(self):
        print("Fitness values:")
        for key in sorted(self.parents.keys()):
            print(f"  Parent: {self.parents[key].fitness:.1f}  Child: {self.children[key].fitness:.1f}")

    def Show_Best(self):
        best_key = max(self.parents.keys(), key=lambda k: self.parents[k].fitness)
        best_solution = self.parents[best_key]
        print(f"Best solution - Flight duration: {best_solution.fitness} steps")
        best_solution.Start_Simulation("GUI")