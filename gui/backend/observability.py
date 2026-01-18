# Stage 10: Observability Only Layer (Skeleton Only)

class Observability:
    """
    Read-only observability interface.
    No command authority.
    """

    def snapshot(self):
        raise NotImplementedError("Observability is structural only")
