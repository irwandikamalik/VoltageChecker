from app.instrument.config.dmm_command_config import (
    DMMCommandConfig
)


def test_default_commands():

    config = DMMCommandConfig()

    assert config.identify_command == "*IDN?"
    assert config.voltage_command == "MEAS:VOLT?"
    assert config.current_command == "MEAS:CURR?"


def test_custom_commands():

    config = DMMCommandConfig(
        identify_command="*IDN?",
        voltage_command="READ:VOLT?",
        current_command="READ:CURR?"
    )

    assert config.identify_command == "*IDN?"
    assert config.voltage_command == "READ:VOLT?"
    assert config.current_command == "READ:CURR?"


def test_valid_commands():

    config = DMMCommandConfig()

    assert config.is_valid() is True


def test_empty_identify_command_is_invalid():

    config = DMMCommandConfig(
        identify_command=""
    )

    assert config.is_valid() is False


def test_empty_voltage_command_is_invalid():

    config = DMMCommandConfig(
        voltage_command=""
    )

    assert config.is_valid() is False


def test_empty_current_command_is_invalid():

    config = DMMCommandConfig(
        current_command=""
    )

    assert config.is_valid() is False