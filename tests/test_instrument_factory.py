from app.instrument.instrument_factory import (
    InstrumentFactory
)

from app.instrument.config.connection_config import (
    DMMConnectionConfig
)

from app.instrument.dmm.generic_dmm import (
    GenericDMM
)

from app.instrument.config.dmm_command_config import (
    DMMCommandConfig
)

def test_create_dmm():

    config = DMMConnectionConfig(
        communication_type="GPIB",
        resource_name="GPIB0::22::INSTR"
    )

    command_config = DMMCommandConfig()

    dmm = InstrumentFactory.create_dmm(
        connection_config=config,
        command_config=command_config
    )

    assert isinstance(
        dmm,
        GenericDMM
    )

    assert dmm.connection.resource_name == (
        "GPIB0::22::INSTR"
    )


def test_create_serial_dmm():

    config = DMMConnectionConfig(
        communication_type="SERIAL",
        resource_name="ASRL3::INSTR"
    )

    command_config = DMMCommandConfig()

    dmm = InstrumentFactory.create_dmm(
        connection_config=config,
        command_config=command_config
    )

    assert isinstance(
        dmm,
        GenericDMM
    )

    assert dmm.connection.resource_name == (
        "ASRL3::INSTR"
    )


def test_create_tcpip_dmm():

    config = DMMConnectionConfig(
        communication_type="TCPIP",
        resource_name=(
            "TCPIP0::192.168.1.100::inst0::INSTR"
        )
    )

    command_config = DMMCommandConfig()

    dmm = InstrumentFactory.create_dmm(
        connection_config=config,
        command_config=command_config
    )

    assert isinstance(
        dmm,
        GenericDMM
    )

    assert dmm.connection.resource_name == (
        "TCPIP0::192.168.1.100::inst0::INSTR"
    )


def test_invalid_config():

    config = DMMConnectionConfig(
        communication_type="UNKNOWN",
        resource_name="TEST"
    )

    command_config = DMMCommandConfig()

    try:

        InstrumentFactory.create_dmm(
            connection_config=config,
            command_config=command_config
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Konfigurasi koneksi DMM tidak valid."
        )

def test_custom_command_config():

    connection_config = DMMConnectionConfig(
        communication_type="GPIB",
        resource_name="GPIB0::22::INSTR"
    )

    command_config = DMMCommandConfig(
        identify_command="CUSTOM:IDN?",
        voltage_command="CUSTOM:VOLT?",
        current_command="CUSTOM:CURR?"
    )

    dmm = InstrumentFactory.create_dmm(
        connection_config=connection_config,
        command_config=command_config
    )

    assert (
        dmm.command_config
        is command_config
    )

def test_invalid_command_config():

    connection_config = DMMConnectionConfig(
        communication_type="GPIB",
        resource_name="GPIB0::22::INSTR"
    )

    command_config = DMMCommandConfig(
        voltage_command=""
    )

    try:

        InstrumentFactory.create_dmm(
            connection_config=connection_config,
            command_config=command_config
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Konfigurasi command DMM tidak valid."
        )