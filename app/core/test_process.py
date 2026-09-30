class TestProcess:

    def __init__(
        self,
        serial_manager,
        batch_repository
    ):

        self.serial_manager = serial_manager
        self.batch_repository = batch_repository

        self.batch_id = None


    def load_active_batch(self):

        batch = (
            self.batch_repository
            .get_active_batch()
        )

        if batch is None:
            return False

        self.batch_id = batch[0]

        batch_code = batch[1]
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


    def complete_test(self):

        self.serial_manager.next_serial()

        self.batch_repository.update_sequence(
            self.batch_id,
            self.serial_manager.sequence_number
        )