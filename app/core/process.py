from datetime import datetime

from app.core.judgment import Judgment
from app.logger.production_logger import ProductionLogger
from app.core.state import (
    ProcessState,
    StateManager
)


class ProcessController:

    def __init__(
        self,
        serial_manager,
        batch_repository,
        model_repository,
        instrument,
        operator_id,
        logger=None
    ):

        self.serial_manager = serial_manager
        self.batch_repository = batch_repository
        self.model_repository = model_repository
        self.instrument = instrument
        self.operator_id = operator_id

        self.judgment = Judgment()
        self.logger = logger or ProductionLogger()
        self.state_manager = StateManager()


        self.batch_id = None
        self.model_name = None

        self.attempt_number = 0


    def get_state(self):

        return self.state_manager.get_state()

    def start_test(self):

        self.state_manager.set_state(
            ProcessState.TESTING
        )

        self.attempt_number += 1

        return self.attempt_number


    def retest(self):
        if self.get_state() != ProcessState.RESULT_NG:
            raise ValueError(
                "RETEST hanya dapat dilakukan setelah hasil NG"
            )

        self.state_manager.set_state(
            ProcessState.RETEST
        )


    def accept_ng(self):
        if self.get_state() != ProcessState.RESULT_NG:
            raise ValueError(
                "Accept NG hanya dapat dilakukan setelah hasil NG"
            )
        self.complete_test()


    def handle_error(self):
        current_state = self.get_state()

        if current_state != ProcessState.TESTING:
            raise ValueError(
                "ERROR hanya dapat ditangani saat proses testing"
            )

        self.state_manager.set_state(
            ProcessState.ERROR
        )

    def recover_from_error(self):

        if self.get_state() != ProcessState.ERROR:
            raise ValueError(
                "Recovery hanya dapat dilakukan dari state ERROR"
            )

        self.state_manager.set_state(
            ProcessState.IDLE
        )

        self.state_manager.set_state(
            ProcessState.OPERATOR_VALID
        )

        self.state_manager.set_state(
            ProcessState.BATCH_READY
        )

        self.state_manager.set_state(
            ProcessState.WAIT_SERIAL
        )


    def get_attempt_number(self):

        return self.attempt_number


    def load_active_batch(self):

        batch = (
            self.batch_repository
            .get_active_batch()
        )

        if batch is None:

            self.state_manager.set_state(
                ProcessState.ERROR
            )

            return False

        self.batch_id = batch[0]

        batch_code = batch[1]
        self.model_name = batch[2]
        sequence_number = batch[4]

        self.serial_manager.load_batch(
            batch_code,
            sequence_number
        )

        self.state_manager.set_state(
            ProcessState.BATCH_READY
        )

        return True

    def get_expected_serial(self):

        return (
            self.serial_manager
            .get_expected_serial()
        )

    def validate_operator(self):

        operator = (
            self.operator_id
        )

        if not operator:

            self.state_manager.set_state(
                ProcessState.ERROR
            )

            return False

        self.state_manager.set_state(
            ProcessState.OPERATOR_VALID
        )

        return True

    def wait_for_serial(self):

        self.state_manager.set_state(
            ProcessState.WAIT_SERIAL
        )

    def validate_serial(self, serial_number):

        valid = (
            self.serial_manager
            .validate_serial(serial_number)
        )

        if valid:

            self.state_manager.set_state(
                ProcessState.SERIAL_VALID
            )

            return True

        return False

    def judge_measurement(
        self,
        voltage,
        current
    ):

        model = self.model_repository.get_model(
            self.model_name
        )

        if model is None:

            raise ValueError(
                "Model tidak ditemukan."
            )


        return self.judgment.check(

            voltage=voltage,

            current=current,

            voltage_lower=model[
                "voltage_lower"
            ],

            voltage_upper=model[
                "voltage_upper"
            ],

            current_lower=model[
                "current_lower"
            ],

            current_upper=model[
                "current_upper"
            ]
        )

    def run_test(self):

        if not self.instrument.connect():

            self.state_manager.set_state(
                ProcessState.ERROR
            )

            raise RuntimeError(
                "Instrument gagal terhubung."
            )

        try:

            voltage = self.instrument.read_voltage()
            current = self.instrument.read_current()

            judgment = self.judge_measurement(
                voltage,
                current
            )

            return {
                "voltage": voltage,
                "current": current,
                "judgment": judgment
            }

        except Exception:

            self.state_manager.set_state(
                ProcessState.ERROR
            )

            raise

        finally:

            self.instrument.disconnect()

    def log_test_result(
        self,
        serial_number,
        voltage,
        current,
        judgment
    ):

        model = self.model_repository.get_model(
            self.model_name
        )

        if model is None:

            raise ValueError(
                "Model tidak ditemukan."
            )

        now = datetime.now()

        self.logger.log_test(

            model_name=self.model_name,

            serial_number=serial_number,

            attempt=self.attempt_number,

            operator_id=self.operator_id,

            voltage=voltage,

            current=current,

            judgment=judgment,

            voltage_lower=model[
                "voltage_lower"
            ],

            voltage_upper=model[
                "voltage_upper"
            ],

            current_lower=model[
                "current_lower"
            ],

            current_upper=model[
                "current_upper"
            ],

            date=now,

            time=now
        )


    def process_result(self, judgment):

        if judgment == "OK":

            self.state_manager.set_state(
                ProcessState.RESULT_OK
            )

        elif judgment == "NG":

            self.state_manager.set_state(
                ProcessState.RESULT_NG
            )

        else:

            self.state_manager.set_state(
                ProcessState.ERROR
            )
    

    def complete_test(self):

        self.state_manager.set_state(
            ProcessState.COMPLETED
        )

        self.serial_manager.next_serial()

        self.batch_repository.update_sequence(
            self.batch_id,
            self.serial_manager.sequence_number
        )

        self.attempt_number = 0

        self.state_manager.set_state(
            ProcessState.WAIT_SERIAL
        )


