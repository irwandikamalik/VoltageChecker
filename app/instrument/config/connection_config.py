class DMMConnectionConfig:

    def __init__(
        self,
        communication_type,
        resource_name,
        timeout=5000,
        visa_backend=None
    ):
        self.communication_type = communication_type
        self.resource_name = resource_name
        self.timeout = timeout
        self.visa_backend = visa_backend

    def is_valid(self):

        valid_types = [
            "SERIAL",
            "GPIB",
            "TCPIP"
        ]

        if self.communication_type not in valid_types:
            return False

        if not self.resource_name:
            return False

        if self.timeout <= 0:
            return False

        return True