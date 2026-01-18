class FailSafeSignal:
    pass

class FailSafeRuntime:
    def trigger(self, signal: FailSafeSignal):
        raise NotImplementedError

    def is_safe_state(self) -> bool:
        raise NotImplementedError
