from app.instrument.instrument_factory import (
    InstrumentFactory
)

from app.instrument.config.connection_config import (
    DMMConnectionConfig
)

from app.instrument.dmm.generic_dmm import (
    GenericDMM
)


def test_create_dmm():

    config = DMMConnectionConfig(
        communication_type="GPIB",
        resource_name="GPIB0::22::INSTR"
    )

    dmm = InstrumentFactory.create_dmm(
        config
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

    dmm = InstrumentFactory.create_dmm(
        config
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

    dmm = InstrumentFactory.create_dmm(
        config
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

    try:
        InstrumentFactory.create_dmm(config)
        assert False
    except ValueError as error:
        assert str(error) == (
            "Konfigurasi DMM tidak valid."
        )