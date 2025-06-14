# game_master.py
from guesser import GeneticAlgorithmGuesser

class GameMaster:
    def __init__(self, population_size=20, mutation_rate=0.1, max_generations=1000):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.engine = None

    def start(self, target_word):
        self.engine = GeneticAlgorithmGuesser(
            target_word,
            self.population_size,
            self.mutation_rate,
            self.max_generations
        )
        self.engine.initialize_population()
        return self.engine.generation, self.engine.best_guess, self.engine.best_cost, True

    def step(self):
        return self.engine.step()

    def is_finished(self):
        return self.engine.best_cost == 0 or self.engine.generation >= self.max_generations

    def get_best(self):
        return self.engine.best_guess, self.engine.best_cost
