class InstrumentSimulator:

    def __init__(
        self,
        measurements=None,
        fail_on_read=False
    ):

        if measurements is None:

            measurements = [
                {
                    "voltage": 24.00,
                    "current": 0.150
                }
            ]

        self.measurements = measurements
        self.attempt_index = 0
        self.fail_on_read = fail_on_read


    def connect(self):

        print("Instrument connected.")

        return True


    def disconnect(self):

        print("Instrument disconnected.")


    def read_voltage(self):
        if self.fail_on_read:

            raise RuntimeError(
                "Simulasi instrument error."
            )
        
        return self.measurements[
            self.attempt_index
        ]["voltage"]

    def read_current(self):

        return self.measurements[
            self.attempt_index
        ]["current"]


    def next_measurement(self):

        if self.attempt_index < len(
            self.measurements
        ) - 1:

            self.attempt_index += 1