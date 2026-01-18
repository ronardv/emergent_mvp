class AuditEvent:
    pass

class AuditTrail:
    def record(self, event: AuditEvent):
        raise NotImplementedError

    def verify_integrity(self) -> bool:
        raise NotImplementedError
