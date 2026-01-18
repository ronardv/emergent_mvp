class Observer:
    def __init__(self):
        self.snapshots = []

    def record(self, state):
        self.snapshots.append(state)
