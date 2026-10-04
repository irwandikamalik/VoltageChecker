from app.instrument.config.connection_config import (
    DMMConnectionConfig
)


def test_serial_config():

    config = DMMConnectionConfig(
        communication_type="SERIAL",
        resource_name="ASRL3::INSTR"
    )

    assert config.communication_type == "SERIAL"
    assert config.resource_name == "ASRL3::INSTR"
    assert config.is_valid() is True


def test_gpib_config():

    config = DMMConnectionConfig(
        communication_type="GPIB",
        resource_name="GPIB0::22::INSTR"
    )

    assert config.communication_type == "GPIB"
    assert config.resource_name == "GPIB0::22::INSTR"
    assert config.is_valid() is True


def test_tcpip_config():

    config = DMMConnectionConfig(
        communication_type="TCPIP",
        resource_name=(
            "TCPIP0::192.168.1.100::inst0::INSTR"
        )
    )

    assert config.communication_type == "TCPIP"
    assert config.is_valid() is True


def test_invalid_communication_type():

    config = DMMConnectionConfig(
        communication_type="BLUETOOTH",
        resource_name="TEST"
    )

    assert config.is_valid() is False


def test_empty_resource():

    config = DMMConnectionConfig(
        communication_type="GPIB",
        resource_name=""
    )

    assert config.is_valid() is False


def test_invalid_timeout():

    config = DMMConnectionConfig(
        communication_type="GPIB",
        resource_name="GPIB0::22::INSTR",
        timeout=0
    )

    assert config.is_valid() is False