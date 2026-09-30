class InstrumentSimulator:

    def __init__(
        self,
        voltage=24.00,
        current=0.150
    ):

        self.voltage = voltage
        self.current = current


    def connect(self):

        print("Instrument connected.")

        return True


    def disconnect(self):

        print("Instrument disconnected.")


    def read_voltage(self):

        return self.voltage


    def read_current(self):

        return self.current