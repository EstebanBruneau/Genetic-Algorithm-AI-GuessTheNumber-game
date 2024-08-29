from genAI import GuessTheNumberAI
from training import *


# Constants
upper_bound = 100
startingGen = 412

# parameters
episodes = 1000
populationSize = 10000
fitnessViability = 10
mutationRate = 0.01
# crossoverRate = 0.1
eliteProportion = 0.001

# booleans
deletePreviousGenerations = False

def main():
    # initpopulation = createInitialPopulation(populationSize)
    population = loadPopulation(f"gen{startingGen}.csv")
    
    # trainingLoop(population, upper_bound, populationSize, startingGen, episodes, eliteProportion, mutationRate, fitnessViability, deletePreviousGenerations)


    population = loadPopulation(f"gen200.csv")
    population2 = loadPopulation(f"gen412.csv")

    nb = 0
    
    print(population[nb].name)
    # print(population[nb].fitness)
    playAGame(population[nb], upper_bound)
    
    # print(population2[nb].name)
    # # print(population2[nb].fitness)
    # playAGame(population2[nb], upper_bound)
    
    
if __name__ == "__main__":
    main()