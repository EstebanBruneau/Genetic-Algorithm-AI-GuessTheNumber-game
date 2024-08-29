import numpy as np
import os

class humanPlayer:
    def __init__(self,limit=100):
        self.name = input("Name: ")

    def predict(self, calls):
        number = int(input("Enter number: "))
        return number
        
    def __str__(self):
        return f"HumanPlayer({self.name})"
    
    def __repr__(self):
        return f"HumanPlayer({self.name})"
        
