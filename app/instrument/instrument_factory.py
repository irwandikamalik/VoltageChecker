from app.instrument.communication.visa_connection import (
    VisaConnection
)
from app.instrument.dmm.generic_dmm import GenericDMM


class InstrumentFactory:

    @staticmethod
    def create_dmm(config):

        if not config.is_valid():
            raise ValueError(
                "Konfigurasi DMM tidak valid."
            )

        connection = VisaConnection(
            resource_name=config.resource_name,
            visa_backend=config.visa_backend,
            timeout=config.timeout
        )

        return GenericDMM(
            connection=connection
        )