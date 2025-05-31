import random
import string

class GeneticAlgorithmGuesser:

    def __init__(self,
                 target_word: str,
                 population_size: int = 20,
                 mutation_rate: float = 0.1,
                 max_generations: int = 1000):
        self.target_word = target_word.lower()
        self.word_length = len(self.target_word)
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations

        self.population = []
        self.best_guess = None
        self.best_cost = float('inf')
        self.generation = 0

    def random_word(self) -> str:
        return ''.join(random.choice(string.ascii_lowercase)
                       for _ in range(self.word_length))

    def compute_cost(self, guess: str) -> int:
        return sum(1 for g_char, t_char
                   in zip(guess, self.target_word)
                   if g_char != t_char)

    def select_parents(self) -> (str, str):
        tournament = random.sample(self.population, 3)
        costs = [(ind, self.compute_cost(ind)) for ind in tournament]
        costs.sort(key=lambda x: x[1])
        return costs[0][0], costs[1][0]

    def crossover(self, parent1: str, parent2: str) -> str:
        if self.word_length < 2:
            return parent1
        point = random.randint(1, self.word_length - 1)
        return parent1[:point] + parent2[point:]

    def mutate(self, word: str) -> str:
        chars = list(word)
        for i in range(self.word_length):
            if random.random() < self.mutation_rate:
                chars[i] = random.choice(string.ascii_lowercase)
        return ''.join(chars)

    def initialize_population(self):
        self.population = [self.random_word()
                           for _ in range(self.population_size)]
        self.generation = 0

        best = None
        best_cost = float('inf')
        for individual in self.population:
            c = self.compute_cost(individual)
            if c < best_cost:
                best, best_cost = individual, c

        self.best_guess = best
        self.best_cost = best_cost

    def step(self) -> (int, str, int, bool):
        if self.best_cost == 0 or self.generation >= self.max_generations:
            return self.generation, self.best_guess, self.best_cost, False

        new_population = [self.best_guess]
        perfect_found = False

        while len(new_population) < self.population_size and not perfect_found:
            p1, p2 = self.select_parents()
            child = self.crossover(p1, p2)
            child = self.mutate(child)

            child_cost = self.compute_cost(child)
            new_population.append(child)
            if child_cost == 0:
                perfect_found = True

        self.population = new_population
        self.generation += 1

        gen_best = None
        gen_best_cost = float('inf')
        for individual in self.population:
            c = self.compute_cost(individual)
            if c < gen_best_cost:
                gen_best, gen_best_cost = individual, c

        improved_flag = False
        if gen_best_cost < self.best_cost:
            self.best_cost = gen_best_cost
            self.best_guess = gen_best
            improved_flag = True

        return self.generation, self.best_guess, self.best_cost, improved_flag
