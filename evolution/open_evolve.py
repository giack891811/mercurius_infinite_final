class OpenEvolve:
    def __init__(self):
        self.name = "OpenEvolve"

    def evolve(self, population: list, generations: int = 10) -> list:
        return [f"{indiv}_gen{generations}" for indiv in population]
