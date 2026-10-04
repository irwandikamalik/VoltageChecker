from app.instrument.communication.visa_connection import (
    VisaConnection
)

from app.instrument.dmm.generic_dmm import (
    GenericDMM
)


class InstrumentFactory:

    @staticmethod
    def create_dmm(
        connection_config,
        command_config
    ):

        if not connection_config.is_valid():
            raise ValueError(
                "Konfigurasi koneksi DMM tidak valid."
            )

        if not command_config.is_valid():
            raise ValueError(
                "Konfigurasi command DMM tidak valid."
            )

        connection = VisaConnection(
            resource_name=(
                connection_config.resource_name
            ),
            visa_backend=(
                connection_config.visa_backend
            ),
            timeout=(
                connection_config.timeout
            )
        )

        return GenericDMM(
            connection=connection,
            command_config=command_config
        )