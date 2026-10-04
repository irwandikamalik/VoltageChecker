from app.instrument.dmm.base_dmm import BaseDMM


class GenericDMM(BaseDMM):

    def __init__(
        self,
        connection,
        command_config
    ):
        self.connection = connection
        self.command_config = command_config

    def connect(self):
        return self.connection.connect()

    def disconnect(self):
        self.connection.disconnect()

    def identify(self):

        response = self.connection.query(
            self.command_config.identify_command
        )

        return response.strip()

    def read_voltage(self):

        response = self.connection.query(
            self.command_config.voltage_command
        )

        return float(response)

    def read_current(self):

        response = self.connection.query(
            self.command_config.current_command
        )

        return float(response)