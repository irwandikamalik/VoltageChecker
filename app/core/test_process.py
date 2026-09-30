from app.core.judgment import Judgment


class TestProcess:

    def __init__(
        self,
        serial_manager,
        batch_repository,
        model_repository,
        instrument
    ):

        self.serial_manager = serial_manager
        self.batch_repository = batch_repository
        self.model_repository = model_repository
        self.instrument = instrument

        self.judgment = Judgment()

        self.batch_id = None
        self.model_name = None

        self.attempt_number = 0


    def start_test(self):

        self.attempt_number += 1

        return self.attempt_number
    

    def get_attempt_number(self):

        return self.attempt_number


    def load_active_batch(self):

        batch = (
            self.batch_repository
            .get_active_batch()
        )

        if batch is None:
            return False

        self.batch_id = batch[0]

        batch_code = batch[1]
        self.model_name = batch[2]
        sequence_number = batch[4]

        self.serial_manager.load_batch(
            batch_code,
            sequence_number
        )

        return True


    def get_expected_serial(self):

        return (
            self.serial_manager
            .get_expected_serial()
        )


    def validate_serial(self, serial_number):

        return (
            self.serial_manager
            .validate_serial(serial_number)
        )


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

        connected = self.instrument.connect()

        if not connected:

            raise RuntimeError(
                "Instrument gagal terhubung."
            )


        voltage = (
            self.instrument
            .read_voltage()
        )

        current = (
            self.instrument
            .read_current()
        )


        result = self.judge_measurement(
            voltage,
            current
        )


        self.instrument.disconnect()


        return {
            "voltage": voltage,
            "current": current,
            "judgment": result
        }

    def complete_test(self):

        self.serial_manager.next_serial()

        self.batch_repository.update_sequence(
            self.batch_id,
            self.serial_manager.sequence_number
        )

        self.attempt_number = 0