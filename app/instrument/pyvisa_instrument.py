import pyvisa

from app.instrument.base import BaseInstrument


class PyVISAInstrument(BaseInstrument):

    def __init__(
        self,
        resource_name,
        visa_backend=None,
        resource_manager_factory=None
    ):
        self.resource_name = resource_name
        self.visa_backend = visa_backend

        self.resource_manager_factory = (
            resource_manager_factory
            or pyvisa.ResourceManager
        )

        self.resource_manager = None
        self.instrument = None

    def connect(self):

        if self.visa_backend:
            self.resource_manager = self.resource_manager_factory(
                self.visa_backend
            )
        else:
            self.resource_manager = self.resource_manager_factory()

        self.instrument = self.resource_manager.open_resource(
            self.resource_name
        )

        return True

    def disconnect(self):

        if self.instrument is not None:
            self.instrument.close()
            self.instrument = None

        if self.resource_manager is not None:
            self.resource_manager.close()
            self.resource_manager = None

    def read_voltage(self):

        if self.instrument is None:
            raise RuntimeError(
                "Instrument belum terhubung."
            )

        response = self.instrument.query(
            "MEAS:VOLT?"
        )

        return float(response)

    def read_current(self):

        if self.instrument is None:
            raise RuntimeError(
                "Instrument belum terhubung."
            )

        response = self.instrument.query(
            "MEAS:CURR?"
        )

        return float(response)