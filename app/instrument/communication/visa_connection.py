import pyvisa

from app.instrument.communication.base_connection import BaseConnection


class VisaConnection(BaseConnection):

    def __init__(
        self,
        resource_name,
        visa_backend=None,
        timeout=5000,
        resource_manager_factory=None
    ):
        self.resource_name = resource_name
        self.visa_backend = visa_backend
        self.timeout = timeout

        self.resource_manager_factory = (
            resource_manager_factory
            or pyvisa.ResourceManager
        )

        self.resource_manager = None
        self.instrument = None

    def connect(self):

        if self.instrument is not None:
            return True

        if self.visa_backend:
            self.resource_manager = self.resource_manager_factory(
                self.visa_backend
            )
        else:
            self.resource_manager = self.resource_manager_factory()

        self.instrument = self.resource_manager.open_resource(
            self.resource_name
        )

        self.instrument.timeout = self.timeout

        return True

    def disconnect(self):

        if self.instrument is not None:
            self.instrument.close()
            self.instrument = None

        if self.resource_manager is not None:
            self.resource_manager.close()
            self.resource_manager = None

    def write(self, command):

        self._check_connection()

        return self.instrument.write(command)

    def read(self):

        self._check_connection()

        return self.instrument.read()

    def query(self, command):

        self._check_connection()

        return self.instrument.query(command)

    def _check_connection(self):

        if self.instrument is None:
            raise RuntimeError(
                "Instrument belum terhubung."
            )