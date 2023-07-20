class CompressedGene:
    def __init__(self, gene:str)->None:
        self.compress(gene)

    def compress(self, gene:str)->None:
        known_chars = []