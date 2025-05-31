from guesser import GeneticAlgorithmGuesser

class GameMaster:

    def __init__(self,
                 population_size: int = 20,
                 mutation_rate: float = 0.1,
                 max_generations: int = 1000):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations

        self.engine: GeneticAlgorithmGuesser = None

    def start(self, target_word: str) -> (int, str, int, bool):
        self.engine = GeneticAlgorithmGuesser(
            target_word=target_word,
            population_size=self.population_size,
            mutation_rate=self.mutation_rate,
            max_generations=self.max_generations
        )
        self.engine.initialize_population()
        gen0 = self.engine.generation
        best0 = self.engine.best_guess
        cost0 = self.engine.best_cost
        return gen0, best0, cost0, True

    def step(self) -> (int, str, int, bool):
        if self.engine is None:
            raise RuntimeError("Call start() before step().")
        gen, best, cost, improved = self.engine.step()
        return gen, best, cost, improved

    def is_finished(self) -> bool:
        if self.engine is None:
            return True
        return (self.engine.best_cost == 0
                or self.engine.generation >= self.engine.max_generations)

    def get_best(self) -> (str, int):
        if self.engine is None:
            return None, None
        return self.engine.best_guess, self.engine.best_cost
