class DMMCommandConfig:

    def __init__(
        self,
        identify_command="*IDN?",
        voltage_command="MEAS:VOLT?",
        current_command="MEAS:CURR?"
    ):
        self.identify_command = identify_command
        self.voltage_command = voltage_command
        self.current_command = current_command

    def is_valid(self):

        if not self.identify_command:
            return False

        if not self.voltage_command:
            return False

        if not self.current_command:
            return False

        return True