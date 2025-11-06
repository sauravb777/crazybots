import copy
import random

import constants as c
from solution import SOLUTION


class HILL_CLIMBER:
    def __init__(self):
        self.parent = SOLUTION()

    def Evolve(self):
        print("Evaluating initial random solution...")
        self.parent.Evaluate("GUI") 
        
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation(currentGeneration)
        

    def Evolve_For_One_Generation(self, generationIndex):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")  
        self.Select()
        self.Print(generationIndex)

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        if self.child.fitness < self.parent.fitness:  
            self.parent = self.child

    def Print(self, generationIndex):
        print(f"Generation {generationIndex}: parent fitness = {self.parent.fitness}, child fitness = {self.child.fitness}")

    def Show_Best(self):
        print("Final evolved solution (GUI)...")
        self.parent.Evaluate("GUI")
