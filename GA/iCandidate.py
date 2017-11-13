class ICandidate:
    def __eq__(self, other):
        raise NotImplementedError

    def diversity(self, other):
        raise NotImplementedError

    @classmethod
    def generate_random_candidate(cls):
        raise NotImplementedError

    @property
    def cost(self):
        raise NotImplementedError