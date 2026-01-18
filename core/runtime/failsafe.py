class FailSafe:
    def __init__(self):
        self.armed = True

    def check(self, condition):
        if self.armed and condition:
            return False
        return True
