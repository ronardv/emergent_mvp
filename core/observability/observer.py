class ObservationFrame:
    pass

class Observer:
    def snapshot(self) -> ObservationFrame:
        raise NotImplementedError

    def export(self) -> dict:
        raise NotImplementedError
