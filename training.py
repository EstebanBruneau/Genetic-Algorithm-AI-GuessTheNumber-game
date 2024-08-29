import numpy as np
import os

from printColored import printColored
from genAI import GuessTheNumberAI

def calculateFeedback(guess, target):
    if guess < target:
        return 1
    elif guess > target:
        return -1
    else:
        return 0
            
def CalcFitness(fitnessViability, ai, upper_bound, lower_bound=1, maxGuesses=100):
    fitness = 0
    for _ in range(fitnessViability):
        target = np.random.randint(lower_bound, upper_bound)
        ai.reset()  # Reset the AI's state for each new target

        for guess_count in range(maxGuesses):
            guess = ai.predict((lower_bound, upper_bound))
            feedback = calculateFeedback(guess, target)
            ai.guessArray.append([guess, feedback])

            # Penalize for large deviations from the bounds
            if guess < lower_bound:
                fitness -= 20 * (lower_bound - guess)
            if guess > upper_bound:
                fitness -= 20 * (guess - upper_bound)
            
            # Penalize for repeated guesses, count the number of times the same guess is repeated
            if ai.guessArray.count([guess, feedback]) > 1:
                fitness -= ai.guessArray.count([guess, feedback]) * 10

            # Penalize for consecutive guesses that give the same feedback
            if len(ai.guessArray) > 5:
                consecutive_count = 1
                for i in range(len(ai.guessArray) - 5, len(ai.guessArray) - 1):
                    if ai.guessArray[i][1] == ai.guessArray[i + 1][1]:
                        consecutive_count += 1
                    else:
                        break
                if consecutive_count >= 3:
                    fitness -= consecutive_count * 4

            if feedback == 0:
                break

    return fitness  

def playAGame(ai, upper_bound=100, lower_bound = 1, maxGuesses = 100, printGuesses = True, printTarget = True):
    
    target = np.random.randint(lower_bound, upper_bound)
    
    if printGuesses: printColored(f"AI {ai.name} starts playing", "blue")
    if printTarget: printColored(f"Target: {target}", "green")
    
    for i in range(maxGuesses):
        guess = ai.predict((lower_bound, upper_bound))
        
        if printGuesses: printColored(f"{i+1}. {ai.name} guesses: {guess}", "cyan")
        
        feedback = calculateFeedback(guess, target)
        
        if printGuesses:
            if feedback == 1:
                color = "yellow"
            elif feedback == -1:
                color = "magenta"
            else:
                color = "green"
            message = "Target is higher\n" if feedback == 1 else "Target is lower\n" if feedback == -1 else "wtf gg\n"
            printColored(message, color)
            
        ai.guessArray.append([guess, feedback])
        if feedback == 0:
            break
    
    if len(ai.guessArray) >= maxGuesses:
        printColored(f"{ai.name}=noob (number was {target})", "red")
    else:    
        printColored(f"{ai.name} guessed the number in {len(ai.guessArray)} guesses", "green")

def playEachNumber(ai, upper_bound=100, lower_bound=1, max_guesses=100, printResults=False):

    sum_guesses = 0
    total_targets = upper_bound - lower_bound + 1

    for target in range(lower_bound, upper_bound + 1):
        
        ai.reset()
        ai.guessArray = []

        for i in range(max_guesses):
            guess = ai.predict((lower_bound, upper_bound))
            
            feedback = calculateFeedback(guess, target)
                
            ai.guessArray.append([guess, feedback])
            if feedback == 0:
                break
        sum_guesses += len(ai.guessArray)
    
    average_guesses = sum_guesses / total_targets
    if printResults:
        printColored(f"{ai.name} average guesses: {average_guesses}", "green")
    
    return average_guesses

def CalcFitness2(ai, upper_bound=100, lower_bound=1, max_guesses=100, printResults=False):

    sum_guesses = 0
    total_targets = upper_bound - lower_bound + 1
    fitness = 0

    for target in range(lower_bound, upper_bound + 1):
        ai.reset()
        ai.guessArray = []
        
        for i in range(max_guesses):
            guess = ai.predict((lower_bound, upper_bound))
            
            feedback = calculateFeedback(guess, target)
                
            ai.guessArray.append([guess, feedback])

            # Penalize for large deviations from the bounds
            if guess < lower_bound:
                fitness -= (lower_bound - guess)
            if guess > upper_bound:
                fitness -= (guess - upper_bound)
            
            # Penalize for repeated guesses, count the number of times the same guess is repeated
            if ai.guessArray.count([guess, feedback]) > 1:
                fitness -= ai.guessArray.count([guess, feedback]) * 2

            # Penalize for consecutive guesses that give the same feedback
            if len(ai.guessArray) > 5:
                consecutive_count = 1
                for i in range(len(ai.guessArray) - 5, len(ai.guessArray) - 1):
                    if ai.guessArray[i][1] == ai.guessArray[i + 1][1]:
                        consecutive_count += 1
                    else:
                        break
                if consecutive_count >= 3:
                    fitness -= consecutive_count * 3.5
                    
            if feedback == 0:
                break
        sum_guesses += len(ai.guessArray)
        
    average_guesses = sum_guesses / total_targets
    fitness /= total_targets
    
    fitness += 1 / average_guesses * 1000
     
    if printResults:
        printColored(f"{ai.name} average guesses: {average_guesses}", "green")
    
    return fitness

def CalcAndSetPopulationFitness(population, upper_bound, fitnessViability):
    for ai in population:
        CalcAndSetFitness(fitnessViability, ai, upper_bound)
    return population

def CalcAndSetPopulationFitness2(population, upper_bound):
    for ai in population:
        fitness = CalcFitness2(ai, upper_bound)
        ai.fitness = fitness
    return population

def createInitialPopulation(population_size):
    population = []
    for i in range(population_size):
        ai = GuessTheNumberAI()
        population.append(ai)
    return population
        
def printPopulation(population):
    for ai in population:
        print(ai)
        
def completePopulation(population, newSize):
    while len(population) < newSize:
        ai = GuessTheNumberAI()
        population.append(ai)
    return population
    
def selectBest(population, n=1):
    population = sorted(population, key=lambda x: x.fitness, reverse=True)
    if n > len(population):
        return population
    elif n < 0:
        return []
    elif n == 1:
        return population[0]
    else:
        return population[:n]
    
def selectRoulette(population):
    fitnesses = [ai.fitness for ai in population]
    min_fitness = min(fitnesses)
    shift = abs(min_fitness) + 1  # Shift to make all fitness values non-negative
    shifted_fitnesses = [fitness + shift for fitness in fitnesses]
    total_fitness = sum(shifted_fitnesses)
    probabilities = [fitness / total_fitness for fitness in shifted_fitnesses]
    ai = np.random.choice(population, p=probabilities)
    return ai
    
def crossover(ai1, ai2):
    new_ai = GuessTheNumberAI()
    mask = np.random.rand(23) < 0.5
    new_ai.weights = np.where(mask, ai1.weights, ai2.weights)
    return new_ai

def mutate(ai, mutation_rate=0.1):
    for i in range(23):
        if np.random.rand() < mutation_rate:
            ai.weights[i] = np.random.rand() * 2 - 1
    return ai

def evolve(population, elite_proportion=0.1, mutation_rate=0.1):
    new_population = selectBest(population, int(len(population) * elite_proportion))
    
    while len(new_population) < len(population):
        ai1 = selectRoulette(population)
        ai2 = selectRoulette(population)
        
        new_ai = crossover(ai1, ai2)
        new_ai = mutate(new_ai, mutation_rate)
        
        new_population.append(new_ai)
        
    return new_population

def savePopulation(population, filename):
    with open(filename, 'w') as f:
        for ai in population:
            f.write(f"{ai.name}, {ai.fitness}, {ai.weights.tolist()}\n")

def loadPopulation(filename):
    population = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split(", ", 2)
            if len(parts) != 3:
                print(f"Skipping malformed line: {line.strip()}")
                continue
            name, fitness, weights_str = parts
            ai = GuessTheNumberAI()
            ai.name = name
            ai.fitness = float(fitness)
            weights = np.fromstring(weights_str.strip('[]'), sep=', ')
            ai.weights = weights
            population.append(ai)
    return population

def saveAI(ai, filename):
    with open(filename, 'w') as f:
        f.write(f"{ai.name}, {ai.fitness}, {ai.weights.tolist()}\n")
        
def loadAI(filename):
    with open(filename, 'r') as f:
        line = f.readline().strip()
        parts = line.split(", ", 2)
        if len(parts) != 3:
            raise ValueError(f"Malformed line: {line.strip()}")
        name, fitness, weights_str = parts
        ai = GuessTheNumberAI()
        ai.name = name
        ai.fitness = float(fitness)
        weights = np.fromstring(weights_str.strip('[]'), sep=' ')
        ai.weights = weights
    return ai

def trainingLoop(population, upper_bound, population_size, starting_gen, generations, elite_proportion, mutation_rate, fitnessViability, BOOLdeletePreviousGenerations):
    if BOOLdeletePreviousGenerations == True:
        deletePreviousGenerations(starting_gen)
    
    if len(population) < population_size:
        population = completePopulation(population, population_size)
    
    for i in range(generations):
        
        population = evolve(population, elite_proportion, mutation_rate)
        
        population = CalcAndSetPopulationFitness2(population, upper_bound)
        population = sorted(population, key=lambda x: x.fitness, reverse=True)
        savePopulation(population, f"gen{starting_gen + i + 1}.csv")
        
        printColored(f"\nGeneration {starting_gen + i + 1}", "yellow")
        printColored(f"Average fitness: {np.average([ai.fitness for ai in population])}", "green")
        printColored(f"Top 50 average fitness: {np.average([ai.fitness for ai in population[:50]])}", "green")
        printColored(f"Top fitness: {population[0].fitness}", "green")
                
    return population
    
def deletePreviousGenerations(generation):
    for i in range(generation):
        try:
            os.remove(f"gen{i}.csv")
        except FileNotFoundError:
            pass
    return