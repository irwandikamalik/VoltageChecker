class DMMConnectionConfig:

    VALID_COMMUNICATION_TYPES = [
        "SERIAL",
        "GPIB",
        "TCPIP"
    ]

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

        if self.communication_type not in (
            self.VALID_COMMUNICATION_TYPES
        ):
            return False

        if not self.resource_name:
            return False

        if self.timeout <= 0:
            return False

        if not self._is_resource_type_valid():
            return False

        return True

    def _is_resource_type_valid(self):

        resource_name = self.resource_name.upper()

        if self.communication_type == "SERIAL":

            return resource_name.startswith(
                "ASRL"
            ) or resource_name.startswith(
                "COM"
            )

        if self.communication_type == "GPIB":

            return resource_name.startswith(
                "GPIB"
            )

        if self.communication_type == "TCPIP":

            return resource_name.startswith(
                "TCPIP"
            )

        return False