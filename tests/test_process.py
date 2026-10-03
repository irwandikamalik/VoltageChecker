from app.core.process import ProcessController
from app.core.state import ProcessState


class FakeSerialManager:

    def __init__(self):
        self.loaded_batch = None
        self.sequence_number = None

    def load_batch(
        self,
        batch_code,
        sequence_number
    ):
        self.loaded_batch = (
            batch_code,
            sequence_number
        )

        self.batch_code = batch_code
        self.sequence_number = sequence_number

    def validate_serial(self, serial_number):

        if self.loaded_batch is None:
            return False

        batch_code, sequence_number = self.loaded_batch

        expected_serial = "{}{:04d}".format(
            batch_code,
            sequence_number
        )

        return serial_number == expected_serial

    def get_expected_serial(self):

        return "{}{:04d}".format(
            self.batch_code,
            self.sequence_number
        )

    def next_serial(self):

        self.sequence_number += 1

        self.loaded_batch = (
            self.batch_code,
            self.sequence_number
        )

class FakeBatchRepository:

    def __init__(self, batch=None):
        self.batch = batch
        self.updated_sequence = None

    def get_active_batch(self):
        return self.batch

    def update_sequence(
        self,
        batch_id,
        sequence_number
    ):
        self.updated_sequence = (
            batch_id,
            sequence_number
        )

class FakeModelRepository:

    def get_model(self, model_name):

        return {
            "model_name": model_name,
            "voltage_lower": 23.0,
            "voltage_upper": 25.0,
            "current_lower": 0.100,
            "current_upper": 0.200
        }


class FakeInstrument:

    def __init__(
        self,
        voltage=24.0,
        current=0.150,
        connect_result=True,
        fail_on_read=False
    ):
        self.voltage = voltage
        self.current = current
        self.connect_result = connect_result
        self.fail_on_read = fail_on_read
        self.connected = False
        self.disconnected = False

    def connect(self):
        self.connected = self.connect_result
        return self.connect_result

    def disconnect(self):
        self.disconnected = True

    def read_voltage(self):

        if self.fail_on_read:
            raise RuntimeError(
                "Simulasi instrument error."
            )

        return self.voltage

    def read_current(self):
        return self.current

class FakeLogger:

    def __init__(self):
        self.logged_data = []

    def log_test(
        self,
        model_name,
        serial_number,
        attempt,
        operator_id,
        voltage,
        current,
        judgment,
        voltage_lower,
        voltage_upper,
        current_lower,
        current_upper,
        date,
        time
    ):
        self.logged_data.append({
            "model_name": model_name,
            "serial_number": serial_number,
            "attempt": attempt,
            "operator_id": operator_id,
            "voltage": voltage,
            "current": current,
            "judgment": judgment,
            "voltage_lower": voltage_lower,
            "voltage_upper": voltage_upper,
            "current_lower": current_lower,
            "current_upper": current_upper,
            "date": date,
            "time": time
        })


    

def create_process(
    batch=None,
    instrument=None,
    logger=None
):

    if instrument is None:
        instrument = FakeInstrument()

    return ProcessController(
        serial_manager=FakeSerialManager(),
        batch_repository=FakeBatchRepository(batch),
        model_repository=FakeModelRepository(),
        instrument=instrument,
        operator_id="OP001",
        logger=logger
    )

def test_process_initial_state():

    process = create_process()

    assert process.get_state().value == "IDLE"


def test_validate_operator_valid():

    process = create_process()

    result = process.validate_operator()

    assert result is True

    assert (
        process.get_state().value
        == "OPERATOR_VALID"
    )


def test_validate_operator_empty():

    process = ProcessController(
        serial_manager=FakeSerialManager(),
        batch_repository=FakeBatchRepository(),
        model_repository=FakeModelRepository(),
        instrument=FakeInstrument(),
        operator_id=""
    )

    result = process.validate_operator()

    assert result is False

    assert (
        process.get_state().value
        == "ERROR"
    )

def test_load_active_batch():

    batch = (
        1,
        "MDF260930212249",
        "MODEL-A",
        "2026-09-30 21:22:49",
        25,
        "ACTIVE"
    )

    process = create_process(batch)

    process.validate_operator()

    result = process.load_active_batch()

    assert result is True
    assert process.get_state().value == "BATCH_READY"
    assert process.batch_id == 1
    assert process.model_name == "MODEL-A"
    assert process.serial_manager.loaded_batch == (
        "MDF260930212249",
        25
    )

def test_load_active_batch_not_found():

    process = create_process(batch=None)

    result = process.load_active_batch()

    assert result is False
    assert process.get_state().value == "ERROR"

def test_validate_serial_correct():

    batch = (
        1,
        "MDF260930212249",
        "MODEL-A",
        "2026-09-30 21:22:49",
        25,
        "ACTIVE"
    )

    process = create_process(batch)

    process.validate_operator()
    process.load_active_batch()
    process.wait_for_serial()

    result = process.validate_serial(
        "MDF2609302122490025"
    )

    assert result is True
    assert process.get_state().value == "SERIAL_VALID"

def test_validate_serial_wrong():

    batch = (
        1,
        "MDF260930212249",
        "MODEL-A",
        "2026-09-30 21:22:49",
        25,
        "ACTIVE"
    )

    process = create_process(batch)

    process.validate_operator()
    process.load_active_batch()
    process.wait_for_serial()

    result = process.validate_serial(
        "MDF2609302122490024"
    )

    assert result is False
    assert process.get_state().value == "WAIT_SERIAL"

def test_start_test():

    batch = (
        1,
        "MDF260930212249",
        "MODEL-A",
        "2026-09-30 21:22:49",
        25,
        "ACTIVE"
    )

    process = create_process(batch)

    process.validate_operator()
    process.load_active_batch()
    process.wait_for_serial()

    process.validate_serial(
        "MDF2609302122490025"
    )

    attempt = process.start_test()

    assert attempt == 1
    assert process.get_state().value == "TESTING"

def test_start_test_attempt_number():

    batch = (
        1,
        "MDF260930212249",
        "MODEL-A",
        "2026-09-30 21:22:49",
        25,
        "ACTIVE"
    )

    process = create_process(batch)

    process.validate_operator()
    process.load_active_batch()
    process.wait_for_serial()

    process.validate_serial(
        "MDF2609302122490025"
    )

    attempt_1 = process.start_test()

    assert attempt_1 == 1

    process.process_result("NG")
    process.retest()

    attempt_2 = process.start_test()

    assert attempt_2 == 2
    assert process.get_attempt_number() == 2

def test_run_test_ok():

    instrument = FakeInstrument(
        voltage=24.0,
        current=0.150
    )

    process = create_process(
        instrument=instrument
    )

    process.model_name = "MODEL-A"

    result = process.run_test()

    assert result["voltage"] == 24.0
    assert result["current"] == 0.150
    assert result["judgment"] == "OK"

    assert instrument.connected is True
    assert instrument.disconnected is True

def test_run_test_ng():

    instrument = FakeInstrument(
        voltage=22.0,
        current=0.150
    )

    process = create_process(
        instrument=instrument
    )

    process.model_name = "MODEL-A"

    result = process.run_test()

    assert result["voltage"] == 22.0
    assert result["current"] == 0.150
    assert result["judgment"] == "NG"

    assert instrument.connected is True
    assert instrument.disconnected is True

def prepare_testing_process():

    batch = (
        1,
        "MDF260930212249",
        "MODEL-A",
        "2026-09-30 21:22:49",
        25,
        "ACTIVE"
    )

    process = create_process(batch)

    process.validate_operator()
    process.load_active_batch()
    process.wait_for_serial()

    process.validate_serial(
        "MDF2609302122490025"
    )

    process.start_test()

    return process

def test_process_result_ok():

    process = prepare_testing_process()

    process.process_result("OK")

    assert process.get_state().value == "RESULT_OK"

def test_process_result_ng():

    process = prepare_testing_process()

    process.process_result("NG")

    assert process.get_state().value == "RESULT_NG"

def test_retest():

    process = prepare_testing_process()

    process.process_result("NG")

    process.retest()

    assert process.get_state().value == "RETEST"

def test_retest_start_test():

    process = prepare_testing_process()

    process.process_result("NG")

    process.retest()

    process.start_test()

    assert process.get_state().value == "TESTING"
    assert process.get_attempt_number() == 2

def test_retest_invalid_state():

    process = prepare_testing_process()

    process.process_result("OK")

    try:
        process.retest()
        assert False
    except ValueError:
        assert True

def test_accept_ng():

    process = prepare_testing_process()

    process.process_result("NG")

    process.accept_ng()

    assert process.get_state().value == "WAIT_SERIAL"

def test_accept_ng_increments_sequence_and_resets_attempt():

    process = prepare_testing_process()

    process.process_result("NG")

    assert process.get_state().value == "RESULT_NG"
    assert process.get_attempt_number() == 1

    process.accept_ng()

    assert process.get_state().value == "WAIT_SERIAL"

    assert (
        process.serial_manager.sequence_number
        == 26
    )

    assert process.batch_repository.updated_sequence == (
        1,
        26
    )

    assert process.get_attempt_number() == 0

def test_accept_ng_invalid_state():

    process = prepare_testing_process()

    process.process_result("OK")

    try:
        process.accept_ng()
        assert False
    except ValueError:
        assert True

def test_complete_test():

    process = prepare_testing_process()

    process.process_result("OK")

    process.complete_test()

    assert process.get_state().value == "WAIT_SERIAL"
    assert process.serial_manager.sequence_number == 26

def test_complete_test_increments_sequence():

    process = prepare_testing_process()

    process.process_result("OK")
    process.complete_test()

    assert (
        process.serial_manager.sequence_number
        == 26
    )

    assert process.batch_repository.updated_sequence == (
        1,
        26
    )

def test_complete_test_resets_attempt():

    process = prepare_testing_process()

    process.process_result("OK")
    process.complete_test()

    assert process.get_attempt_number() == 0

def test_run_test_connection_failed():

    instrument = FakeInstrument(
        connect_result=False
    )

    process = create_process(
        instrument=instrument
    )

    process.model_name = "MODEL-A"

    try:
        process.run_test()
        assert False
    except RuntimeError as error:
        assert str(error) == "Instrument gagal terhubung."

def test_run_test_read_error_disconnects():

    instrument = FakeInstrument(
        fail_on_read=True
    )

    process = create_process(
        instrument=instrument
    )

    process.model_name = "MODEL-A"

    try:
        process.run_test()
        assert False
    except RuntimeError as error:
        assert str(error) == "Simulasi instrument error."

    assert instrument.connected is True
    assert instrument.disconnected is True

def test_log_test_result():

    logger = FakeLogger()

    process = create_process(
        logger=logger
    )

    process.model_name = "MODEL-A"
    process.attempt_number = 2

    process.log_test_result(
        serial_number="MDF2609302122490025",
        voltage=24.0,
        current=0.150,
        judgment="OK"
    )

    assert len(logger.logged_data) == 1

    result = logger.logged_data[0]

    assert result["serial_number"] == \
        "MDF2609302122490025"

    assert result["attempt"] == 2

    assert result["operator_id"] == \
        "OP001"

    assert result["model_name"] == \
        "MODEL-A"

    assert result["voltage"] == 24.0

    assert result["current"] == 0.150

    assert result["voltage_lower"] == 23.0
    assert result["voltage_upper"] == 25.0

    assert result["current_lower"] == 0.100
    assert result["current_upper"] == 0.200

    assert result["judgment"] == "OK"

def test_retest_logging():

    logger = FakeLogger()

    process = prepare_testing_process()

    process.logger = logger

    # =========================
    # ATTEMPT 1
    # =========================

    process.log_test_result(
        serial_number="MDF2609302122490025",
        voltage=22.0,
        current=0.150,
        judgment="NG"
    )

    # NG
    process.process_result("NG")

    # =========================
    # RETEST
    # =========================

    process.retest()

    process.start_test()

    # =========================
    # ATTEMPT 2
    # =========================

    process.log_test_result(
        serial_number="MDF2609302122490025",
        voltage=24.0,
        current=0.150,
        judgment="OK"
    )

    # =========================
    # ASSERT
    # =========================

    assert len(logger.logged_data) == 2

    first_result = logger.logged_data[0]
    second_result = logger.logged_data[1]

    assert first_result["serial_number"] == \
        "MDF2609302122490025"

    assert first_result["attempt"] == 1
    assert first_result["judgment"] == "NG"

    assert second_result["serial_number"] == \
        "MDF2609302122490025"

    assert second_result["attempt"] == 2
    assert second_result["judgment"] == "OK"

def test_wrong_serial_does_not_start_test():

    instrument = FakeInstrument()

    batch = (
        1,
        "MDF260930212249",
        "MODEL-A",
        "2026-09-30 21:22:49",
        25,
        "ACTIVE"
    )

    process = create_process(
        batch=batch,
        instrument=instrument
    )

    process.validate_operator()
    process.load_active_batch()
    process.wait_for_serial()

    result = process.validate_serial(
        "MDF2609302122490024"
    )

    assert result is False

    assert process.get_state().value == \
        "WAIT_SERIAL"

    assert instrument.connected is False
    assert instrument.disconnected is False

    assert process.get_attempt_number() == 0

def test_wrong_serial_does_not_change_sequence():

    batch = (
        1,
        "MDF260930212249",
        "MODEL-A",
        "2026-09-30 21:22:49",
        25,
        "ACTIVE"
    )

    process = create_process(
        batch=batch
    )

    process.validate_operator()
    process.load_active_batch()
    process.wait_for_serial()

    result = process.validate_serial(
        "MDF2609302122490024"
    )

    assert result is False

    assert (
        process.serial_manager.sequence_number
        == 25
    )

    assert (
        process.get_expected_serial()
        == "MDF2609302122490025"
    )

def test_correct_serial_allows_test():

    instrument = FakeInstrument()

    batch = (
        1,
        "MDF260930212249",
        "MODEL-A",
        "2026-09-30 21:22:49",
        25,
        "ACTIVE"
    )

    process = create_process(
        batch=batch,
        instrument=instrument
    )

    process.validate_operator()
    process.load_active_batch()
    process.wait_for_serial()

    result = process.validate_serial(
        "MDF2609302122490025"
    )

    assert result is True

    assert process.get_state().value == \
        "SERIAL_VALID"

    process.start_test()

    assert process.get_state().value == \
        "TESTING"

    assert process.get_attempt_number() == 1

def test_full_production_flow_ng_retest_ok():

    logger = FakeLogger()

    instrument = FakeInstrument(
        voltage=22.0,
        current=0.150
    )

    batch = (
        1,
        "MDF260930212249",
        "MODEL-A",
        "2026-09-30 21:22:49",
        25,
        "ACTIVE"
    )

    process = create_process(
        batch=batch,
        instrument=instrument,
        logger=logger
    )

    # =========================
    # OPERATOR
    # =========================

    assert process.validate_operator() is True

    # =========================
    # BATCH
    # =========================

    assert process.load_active_batch() is True

    process.wait_for_serial()

    # =========================
    # SERIAL
    # =========================

    assert process.validate_serial(
        "MDF2609302122490025"
    ) is True

    # =========================
    # ATTEMPT 1
    # =========================

    attempt = process.start_test()

    assert attempt == 1

    result = process.run_test()

    assert result["voltage"] == 22.0
    assert result["current"] == 0.150
    assert result["judgment"] == "NG"

    process.log_test_result(
        serial_number="MDF2609302122490025",
        voltage=result["voltage"],
        current=result["current"],
        judgment=result["judgment"]
    )

    process.process_result(
        result["judgment"]
    )

    assert process.get_state().value == "RESULT_NG"

    # =========================
    # RETEST
    # =========================

    process.retest()

    assert process.get_state().value == "RETEST"

    # Measurement kedua sekarang OK
    instrument.voltage = 24.0

    attempt = process.start_test()

    assert attempt == 2

    result = process.run_test()

    assert result["voltage"] == 24.0
    assert result["current"] == 0.150
    assert result["judgment"] == "OK"

    process.log_test_result(
        serial_number="MDF2609302122490025",
        voltage=result["voltage"],
        current=result["current"],
        judgment=result["judgment"]
    )

    process.process_result(
        result["judgment"]
    )

    assert process.get_state().value == "RESULT_OK"

    # =========================
    # COMPLETE
    # =========================

    process.complete_test()

    assert process.get_state().value == "WAIT_SERIAL"

    # =========================
    # VERIFY LOG
    # =========================

    assert len(logger.logged_data) == 2

    first_result = logger.logged_data[0]
    second_result = logger.logged_data[1]

    assert first_result["serial_number"] == \
        "MDF2609302122490025"

    assert first_result["attempt"] == 1
    assert first_result["voltage"] == 22.0
    assert first_result["judgment"] == "NG"

    assert second_result["serial_number"] == \
        "MDF2609302122490025"

    assert second_result["attempt"] == 2
    assert second_result["voltage"] == 24.0
    assert second_result["judgment"] == "OK"

    # =========================
    # VERIFY SEQUENCE
    # =========================

    assert process.serial_manager.sequence_number == 26

    assert process.batch_repository.updated_sequence == (
        1,
        26
    )

    # =========================
    # VERIFY ATTEMPT RESET
    # =========================

    assert process.get_attempt_number() == 0

def test_run_test_connection_failed_does_not_change_sequence():

    instrument = FakeInstrument(
        connect_result=False
    )

    process = create_process(
        batch=(
            1,
            "MDF260930212249",
            "MODEL-A",
            "2026-09-30 21:22:49",
            25,
            "ACTIVE"
        ),
        instrument=instrument
    )

    process.validate_operator()
    process.load_active_batch()
    process.wait_for_serial()

    process.validate_serial(
        "MDF2609302122490025"
    )

    process.start_test()

    try:
        process.run_test()
        assert False
    except RuntimeError as error:
        assert str(error) == "Instrument gagal terhubung."

    assert (
        process.serial_manager.sequence_number
        == 25
    )

    assert (
        process.get_attempt_number()
        == 1
    )

def test_run_test_read_error_does_not_change_sequence():

    instrument = FakeInstrument(
        fail_on_read=True
    )

    process = create_process(
        batch=(
            1,
            "MDF260930212249",
            "MODEL-A",
            "2026-09-30 21:22:49",
            25,
            "ACTIVE"
        ),
        instrument=instrument
    )

    process.validate_operator()
    process.load_active_batch()
    process.wait_for_serial()

    process.validate_serial(
        "MDF2609302122490025"
    )

    process.start_test()

    try:
        process.run_test()
        assert False
    except RuntimeError as error:
        assert str(error) == "Simulasi instrument error."

    assert (
        process.serial_manager.sequence_number
        == 25
    )

    assert (
        process.get_attempt_number()
        == 1
    )

    assert instrument.disconnected is True

def test_run_test_connection_failed_state():

    instrument = FakeInstrument(
        connect_result=False
    )

    process = create_process(
        batch=(
            1,
            "MDF260930212249",
            "MODEL-A",
            "2026-09-30 21:22:49",
            25,
            "ACTIVE"
        ),
        instrument=instrument
    )

    process.validate_operator()
    process.load_active_batch()
    process.wait_for_serial()

    process.validate_serial(
        "MDF2609302122490025"
    )

    process.start_test()

    try:
        process.run_test()
        assert False
    except RuntimeError:
        pass

    assert process.get_state().value == "ERROR"

def test_run_test_read_error_state():

    instrument = FakeInstrument(
        fail_on_read=True
    )

    process = create_process(
        batch=(
            1,
            "MDF260930212249",
            "MODEL-A",
            "2026-09-30 21:22:49",
            25,
            "ACTIVE"
        ),
        instrument=instrument
    )

    process.validate_operator()
    process.load_active_batch()
    process.wait_for_serial()

    process.validate_serial(
        "MDF2609302122490025"
    )

    process.start_test()

    try:
        process.run_test()
        assert False
    except RuntimeError:
        pass

    assert process.get_state().value == "ERROR"

def test_instrument_error_changes_state_to_error():

    instrument = FakeInstrument(
        connect_result=False
    )

    process = create_process(
        batch=(
            1,
            "MDF260930212249",
            "MODEL-A",
            "2026-09-30 21:22:49",
            25,
            "ACTIVE"
        ),
        instrument=instrument
    )

    process.validate_operator()
    process.load_active_batch()
    process.wait_for_serial()

    process.validate_serial(
        "MDF2609302122490025"
    )

    process.start_test()

    try:
        process.run_test()
        assert False
    except RuntimeError:
        pass

    # Untuk behavior baru:
    assert process.get_state().value == "ERROR"

def test_handle_error_changes_state_to_error():

    instrument = FakeInstrument(
        connect_result=False
    )

    process = create_process(
        batch=(
            1,
            "MDF260930212249",
            "MODEL-A",
            "2026-09-30 21:22:49",
            25,
            "ACTIVE"
        ),
        instrument=instrument
    )

    process.validate_operator()
    process.load_active_batch()
    process.wait_for_serial()

    process.validate_serial(
        "MDF2609302122490025"
    )

    process.start_test()

    process.handle_error()

    assert process.get_state().value == "ERROR"

def test_error_can_recover_to_wait_serial():

    instrument = FakeInstrument(
        connect_result=False
    )

    process = create_process(
        batch=(
            1,
            "MDF260930212249",
            "MODEL-A",
            "2026-09-30 21:22:49",
            25,
            "ACTIVE"
        ),
        instrument=instrument
    )

    process.validate_operator()
    process.load_active_batch()
    process.wait_for_serial()

    process.validate_serial(
        "MDF2609302122490025"
    )

    process.start_test()

    process.handle_error()

    # Behavior yang kita inginkan:
    process.recover_from_error()

    assert process.get_state().value == "WAIT_SERIAL"

def test_recover_from_error_keeps_sequence_and_attempt():

    instrument = FakeInstrument(
        connect_result=False
    )

    process = create_process(
        batch=(
            1,
            "MDF260930212249",
            "MODEL-A",
            "2026-09-30 21:22:49",
            25,
            "ACTIVE"
        ),
        instrument=instrument
    )

    process.validate_operator()
    process.load_active_batch()
    process.wait_for_serial()

    process.validate_serial(
        "MDF2609302122490025"
    )

    process.start_test()

    assert process.get_attempt_number() == 1
    assert process.serial_manager.sequence_number == 25

    process.handle_error()

    process.recover_from_error()

    assert process.get_state().value == "WAIT_SERIAL"

    assert process.get_attempt_number() == 1

    assert process.serial_manager.sequence_number == 25