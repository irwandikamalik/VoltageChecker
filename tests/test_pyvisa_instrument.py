from app.instrument.pyvisa_instrument import PyVISAInstrument


class FakeVISAInstrument:

    def __init__(self):
        self.closed = False
        self.queries = []

    def query(self, command):

        self.queries.append(command)

        if command == "MEAS:VOLT?":
            return "24.0"

        if command == "MEAS:CURR?":
            return "0.150"

        return "0"

    def close(self):
        self.closed = True


class FakeResourceManager:

    def __init__(self):
        self.opened_resource = None
        self.closed = False
        self.instrument = FakeVISAInstrument()

    def open_resource(self, resource_name):

        self.opened_resource = resource_name

        return self.instrument

    def close(self):
        self.closed = True

def test_read_voltage():

    instrument = PyVISAInstrument(
        resource_name="GPIB0::1::INSTR"
    )

    fake_resource_manager = FakeResourceManager()

    instrument.resource_manager = fake_resource_manager

    instrument.instrument = (
        fake_resource_manager.instrument
    )

    voltage = instrument.read_voltage()

    assert voltage == 24.0

    assert fake_resource_manager.instrument.queries == [
        "MEAS:VOLT?"
    ]

def test_read_current():

    instrument = PyVISAInstrument(
        resource_name="GPIB0::1::INSTR"
    )

    fake_resource_manager = FakeResourceManager()

    instrument.resource_manager = fake_resource_manager

    instrument.instrument = (
        fake_resource_manager.instrument
    )

    current = instrument.read_current()

    assert current == 0.150

    assert fake_resource_manager.instrument.queries == [
        "MEAS:CURR?"
    ]

def test_read_voltage_without_connection():

    instrument = PyVISAInstrument(
        resource_name="GPIB0::1::INSTR"
    )

    try:
        instrument.read_voltage()
        assert False
    except RuntimeError as error:
        assert str(error) == \
            "Instrument belum terhubung."

def test_read_current_without_connection():

    instrument = PyVISAInstrument(
        resource_name="GPIB0::1::INSTR"
    )

    try:
        instrument.read_current()
        assert False
    except RuntimeError as error:
        assert str(error) == \
            "Instrument belum terhubung."

def test_connect():

    fake_resource_manager = FakeResourceManager()

    instrument = PyVISAInstrument(
        resource_name="GPIB0::1::INSTR",
        resource_manager_factory=lambda: fake_resource_manager
    )

    result = instrument.connect()

    assert result is True

    assert instrument.instrument is fake_resource_manager.instrument

    assert (
        fake_resource_manager.opened_resource
        == "GPIB0::1::INSTR"
    )

def test_disconnect():

    fake_resource_manager = FakeResourceManager()

    instrument = PyVISAInstrument(
        resource_name="GPIB0::1::INSTR",
        resource_manager_factory=lambda: fake_resource_manager
    )

    instrument.connect()
    instrument.disconnect()

    assert fake_resource_manager.instrument.closed is True
    assert fake_resource_manager.closed is True

    assert instrument.instrument is None
    assert instrument.resource_manager is None