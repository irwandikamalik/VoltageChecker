from app.core.serial_manager import SerialManager


def test_create_batch():

    serial_manager = SerialManager()

    serial_manager.create_batch()

    assert serial_manager.batch_code is not None
    assert serial_manager.sequence_number == 1


def test_expected_serial():

    serial_manager = SerialManager()

    serial_manager.load_batch(
        "MDF260930212249",
        1
    )

    assert (
        serial_manager.get_expected_serial()
        == "MDF2609302122490001"
    )


def test_validate_serial_correct():

    serial_manager = SerialManager()

    serial_manager.load_batch(
        "MDF260930212249",
        1
    )

    result = serial_manager.validate_serial(
        "MDF2609302122490001"
    )

    assert result is True


def test_validate_serial_wrong():

    serial_manager = SerialManager()

    serial_manager.load_batch(
        "MDF260930212249",
        1
    )

    result = serial_manager.validate_serial(
        "MDF2609302122490002"
    )

    assert result is False


def test_next_serial():

    serial_manager = SerialManager()

    serial_manager.load_batch(
        "MDF260930212249",
        1
    )

    serial_manager.next_serial()

    assert serial_manager.sequence_number == 2

    assert (
        serial_manager.get_expected_serial()
        == "MDF2609302122490002"
    )


def test_wrong_serial_does_not_change_sequence():

    serial_manager = SerialManager()

    serial_manager.load_batch(
        "MDF260930212249",
        5
    )

    serial_manager.validate_serial(
        "MDF2609302122490004"
    )

    assert serial_manager.sequence_number == 5

    assert (
        serial_manager.get_expected_serial()
        == "MDF2609302122490005"
    )