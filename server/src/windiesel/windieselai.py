import neat

class WinDiesel:
    def __init__(self) -> None:
        self.LoadConfig("./config-file")
    def LoadConfig(self, configFile) -> None:
        self.config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            configFile
        )