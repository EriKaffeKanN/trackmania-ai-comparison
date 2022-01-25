import neat

class WinDiesel:
    nInputs = 12
    nOutputs = 4
    def __init__(self) -> None:
        self.config = 0
        self.loadConfig("./config-file")
        self.population = neat.Population(self.config)


    def loadConfig(self, configFile) -> None:
        self.config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            configFile
        )
    
    def evalGenomes(self, genomes, inputs, outputs):
        for genome_id, genome in genomes:
            genome.fitness = 4.0
            net = neat.nn.FeedForwardNetwork.create(genome, self.config)
            for i, o in zip(self.inputs, self.outputs):
                output = net.activate(i)
                genome.fitness -= (output[0] - o[0]) ** 2