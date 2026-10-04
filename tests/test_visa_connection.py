from app.instrument.communication.visa_connection import VisaConnection


class FakeInstrument:

    def __init__(self):
        self.timeout = None
        self.closed = False
        self.commands = []

    def write(self, command):
        self.commands.append(
            ("write", command)
        )
        return 1

    def read(self):
        self.commands.append(
            ("read", None)
        )
        return "FAKE RESPONSE"

    def query(self, command):
        self.commands.append(
            ("query", command)
        )
        return "FAKE RESPONSE"

    def close(self):
        self.closed = True


class FakeResourceManager:

    def __init__(self):
        self.instrument = FakeInstrument()
        self.opened_resource = None
        self.closed = False

    def open_resource(self, resource_name):
        self.opened_resource = resource_name
        return self.instrument

    def close(self):
        self.closed = True


def create_fake_resource_manager():
    manager = FakeResourceManager()
    create_fake_resource_manager.manager = manager
    return manager


def test_connect():

    connection = VisaConnection(
        resource_name="GPIB0::22::INSTR",
        resource_manager_factory=create_fake_resource_manager
    )

    result = connection.connect()

    manager = create_fake_resource_manager.manager

    assert result is True
    assert manager.opened_resource == "GPIB0::22::INSTR"
    assert manager.instrument.timeout == 5000


def test_query():

    connection = VisaConnection(
        resource_name="TCPIP0::192.168.1.100::inst0::INSTR",
        resource_manager_factory=create_fake_resource_manager
    )

    connection.connect()

    response = connection.query("*IDN?")

    assert response == "FAKE RESPONSE"

    manager = create_fake_resource_manager.manager

    assert manager.instrument.commands == [
        ("query", "*IDN?")
    ]


def test_write_and_read():

    connection = VisaConnection(
        resource_name="ASRL3::INSTR",
        resource_manager_factory=create_fake_resource_manager
    )

    connection.connect()

    connection.write("TEST")

    response = connection.read()

    assert response == "FAKE RESPONSE"

    manager = create_fake_resource_manager.manager

    assert manager.instrument.commands == [
        ("write", "TEST"),
        ("read", None)
    ]


def test_disconnect():

    connection = VisaConnection(
        resource_name="GPIB0::22::INSTR",
        resource_manager_factory=create_fake_resource_manager
    )

    connection.connect()

    manager = create_fake_resource_manager.manager

    connection.disconnect()

    assert manager.instrument.closed is True
    assert manager.closed is True
    assert connection.instrument is None
    assert connection.resource_manager is None


def test_query_without_connection():

    connection = VisaConnection(
        resource_name="GPIB0::22::INSTR",
        resource_manager_factory=create_fake_resource_manager
    )

    try:
        connection.query("*IDN?")
        assert False
    except RuntimeError as error:
        assert str(error) == "Instrument belum terhubung."