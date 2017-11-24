from hippie.interfaces import BaseCandidate

class TSPAnt(BaseCandidate):
    """Represents problem as list of cities to visit in order."""

    def __init__(self, distance_matrix):
        pass

    def find_path(self):
        """Construct solution."""
        pass

    @property
    def cost(self):
        pass

    def __getitem__(self, item):
        pass

    def __len__(self):
        pass
