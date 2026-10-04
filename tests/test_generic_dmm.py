from app.instrument.dmm.generic_dmm import GenericDMM


class FakeConnection:

    def __init__(self):
        self.connected = False
        self.disconnected = False
        self.commands = []

    def connect(self):
        self.connected = True
        return True

    def disconnect(self):
        self.disconnected = True

    def query(self, command):

        self.commands.append(command)

        responses = {
            "*IDN?": "FAKE,DMM,12345,1.0",
            "MEAS:VOLT?": "24.0",
            "MEAS:CURR?": "0.150"
        }

        return responses[command]


def test_connect():

    connection = FakeConnection()

    dmm = GenericDMM(
        connection=connection
    )

    result = dmm.connect()

    assert result is True
    assert connection.connected is True


def test_disconnect():

    connection = FakeConnection()

    dmm = GenericDMM(
        connection=connection
    )

    dmm.connect()
    dmm.disconnect()

    assert connection.disconnected is True


def test_identify():

    connection = FakeConnection()

    dmm = GenericDMM(
        connection=connection
    )

    result = dmm.identify()

    assert result == "FAKE,DMM,12345,1.0"

    assert connection.commands == [
        "*IDN?"
    ]


def test_read_voltage():

    connection = FakeConnection()

    dmm = GenericDMM(
        connection=connection
    )

    voltage = dmm.read_voltage()

    assert voltage == 24.0

    assert connection.commands == [
        "MEAS:VOLT?"
    ]


def test_read_current():

    connection = FakeConnection()

    dmm = GenericDMM(
        connection=connection
    )

    current = dmm.read_current()

    assert current == 0.150

    assert connection.commands == [
        "MEAS:CURR?"
    ]


def test_custom_commands():

    connection = FakeConnection()

    connection.query = lambda command: {
        "*IDN?": "CUSTOM,DMM,001",
        "READ:VOLT?": "25.0",
        "READ:CURR?": "0.200"
    }[command]

    dmm = GenericDMM(
        connection=connection,
        voltage_command="READ:VOLT?",
        current_command="READ:CURR?"
    )

    assert dmm.identify() == "CUSTOM,DMM,001"
    assert dmm.read_voltage() == 25.0
    assert dmm.read_current() == 0.200