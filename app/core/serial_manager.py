from datetime import datetime


class SerialManager:


    def __init__(self):
        self.batch_code = None
        self.sequence_number = 0


    def create_batch(self):

        now = datetime.now()

        self.batch_code = "MDF{}".format(
            now.strftime("%y%m%d%H%M%S")
        )

        self.sequence_number = 1


    def load_batch(self, batch_code, sequence_number):
        
        self.batch_code = batch_code
        self.sequence_number = sequence_number


    def get_batch_code(self):
        return self.batch_code


    def get_expected_serial(self):
        if self.batch_code is None:
            return None
        
        return "{}{:04d}".format(
            self.batch_code,
            self.sequence_number
        )  



    def validate_serial(self, serial_number):

        expected_serial = self.get_expected_serial()

        if serial_number == expected_serial:
            return True

        return False


    def next_serial(self):

        self.sequence_number += 1