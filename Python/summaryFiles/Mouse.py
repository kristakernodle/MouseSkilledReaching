class Mouse:
    def __init__(self, eartag_number, genotype, experiments):
        self.etNum = str(eartag_number)
        self.genotype = str(genotype)
        self.experiments = set(experiments)
