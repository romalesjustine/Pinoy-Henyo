# guesser.py
import random
import string

class GeneticAlgorithmGuesser:
    def __init__(self, target_word, population_size=20, mutation_rate=0.1, max_generations=1000):
        # === Initialization of GA Parameters ===
        self.target_word = target_word.lower()
        self.word_length = len(self.target_word)
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations

        # === State Variables ===
        self.population = []  # Current population
        self.best_guess = None  # Best individual so far
        self.best_cost = float('inf')  # Cost of best guess
        self.generation = 0  # Current generation index

    def random_word(self):
        # === Generate a Random Word ===
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(self.word_length))

    def compute_cost(self, guess):
        # === Fitness Function: Count mismatched letters ===
        return sum(1 for g, t in zip(guess, self.target_word) if g != t)

    def initialize_population(self):
        # === Start a New Population ===
        self.population = [self.random_word() for _ in range(self.population_size)]
        self.generation = 0

        # Find initial best guess in the population
        self.best_guess = min(self.population, key=self.compute_cost)
        self.best_cost = self.compute_cost(self.best_guess)

    def select_parents(self):
        # === Roulette Wheel Selection Based on Inverse Cost ===
        weights = [1 / (self.compute_cost(ind) + 1) for ind in self.population]
        return random.choices(self.population, weights=weights, k=2)

    def crossover(self, p1, p2):
        # === One-Point Crossover ===
        if self.word_length < 2:
            return p1  # No crossover if word is too short
        point = random.randint(1, self.word_length - 1)
        return p1[:point] + p2[point:]

    def mutate(self, word):
        # === Apply Mutation to a Word ===
        chars = list(word)
        for i in range(self.word_length):
            if random.random() < self.mutation_rate:
                chars[i] = random.choice(string.ascii_lowercase)
        return ''.join(chars)

    def step(self):
        # === One GA Generation Step ===
        if self.best_cost == 0 or self.generation >= self.max_generations:
            return self.generation, self.best_guess, self.best_cost, False

        # Elitism: carry forward best individuals
        elites = sorted(self.population, key=self.compute_cost)[:2]
        new_population = elites.copy()

        # Fill rest of population with children
        while len(new_population) < self.population_size:
            p1, p2 = self.select_parents()
            child = self.mutate(self.crossover(p1, p2))
            new_population.append(child)

        self.population = new_population
        self.generation += 1

        # Evaluate new population for best individual
        gen_best = min(self.population, key=self.compute_cost)
        gen_best_cost = self.compute_cost(gen_best)

        improved = gen_best_cost < self.best_cost
        if improved:
            self.best_guess = gen_best
            self.best_cost = gen_best_cost

        return self.generation, self.best_guess, self.best_cost, improved
