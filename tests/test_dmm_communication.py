from app.instrument.config.connection_config import (
    DMMConnectionConfig
)

from app.instrument.instrument_factory import (
    InstrumentFactory
)

from app.instrument.config.dmm_command_config import (
    DMMCommandConfig
)

class FakeInstrument:

    def __init__(self):
        self.timeout = None
        self.closed = False

    def write(self, command):
        return len(command)

    def read(self):
        return "SIMULATED RESPONSE"

    def query(self, command):

        responses = {
            "*IDN?": (
                "SIMULATED,DMM,MODEL-001,1.0"
            ),
            "MEAS:VOLT?": "24.000",
            "MEAS:CURR?": "0.150"
        }

        return responses[command]

    def close(self):
        self.closed = True


class FakeResourceManager:

    def __init__(self):
        self.instrument = FakeInstrument()
        self.closed = False

    def open_resource(self, resource_name):

        self.resource_name = resource_name

        return self.instrument

    def close(self):
        self.closed = True


def create_simulated_dmm(
    communication_type,
    resource_name
):

    config = DMMConnectionConfig(
        communication_type=communication_type,
        resource_name=resource_name
    )

    command_config = DMMCommandConfig()

    dmm = InstrumentFactory.create_dmm(
        connection_config=config,
        command_config=command_config
    )

    fake_resource_manager = (
        FakeResourceManager()
    )

    dmm.connection.resource_manager_factory = (
        lambda: fake_resource_manager
    )

    return dmm, fake_resource_manager

def test_serial_dmm_end_to_end():

    dmm, resource_manager = create_simulated_dmm(
        communication_type="SERIAL",
        resource_name="COM1"
    )

    dmm.connect()

    assert (
        dmm.identify()
        == "SIMULATED,DMM,MODEL-001,1.0"
    )

    assert dmm.read_voltage() == 24.0
    assert dmm.read_current() == 0.150

    dmm.disconnect()

    assert resource_manager.closed is True


def test_gpib_dmm_end_to_end():

    dmm, resource_manager = create_simulated_dmm(
        communication_type="GPIB",
        resource_name="GPIB0::22::INSTR"
    )

    dmm.connect()

    assert (
        dmm.identify()
        == "SIMULATED,DMM,MODEL-001,1.0"
    )

    assert dmm.read_voltage() == 24.0
    assert dmm.read_current() == 0.150

    dmm.disconnect()

    assert resource_manager.closed is True


def test_tcpip_dmm_end_to_end():

    dmm, resource_manager = create_simulated_dmm(
        communication_type="TCPIP",
        resource_name="TCPIP0::192.168.1.100::INSTR"
    )

    dmm.connect()

    assert (
        dmm.identify()
        == "SIMULATED,DMM,MODEL-001,1.0"
    )

    assert dmm.read_voltage() == 24.0
    assert dmm.read_current() == 0.150

    dmm.disconnect()

    assert resource_manager.closed is True