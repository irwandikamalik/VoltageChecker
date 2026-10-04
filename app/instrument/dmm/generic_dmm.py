from app.instrument.dmm.base_dmm import BaseDMM


class GenericDMM(BaseDMM):

    def __init__(
        self,
        connection,
        identify_command="*IDN?",
        voltage_command="MEAS:VOLT?",
        current_command="MEAS:CURR?"
    ):
        self.connection = connection

        self.identify_command = identify_command
        self.voltage_command = voltage_command
        self.current_command = current_command

    def connect(self):
        return self.connection.connect()

    def disconnect(self):
        self.connection.disconnect()

    def identify(self):

        response = self.connection.query(
            self.identify_command
        )

        return response.strip()

    def read_voltage(self):

        response = self.connection.query(
            self.voltage_command
        )

        return float(response)

    def read_current(self):

        response = self.connection.query(
            self.current_command
        )

        return float(response)