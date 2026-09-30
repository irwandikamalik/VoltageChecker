import csv
import os


class ProductionLogger:

    def __init__(self, base_path="log"):

        self.base_path = base_path

    def get_log_path(
        self,
        model_name,
        date
    ):

        date_folder = date.strftime(
            "%Y-%m-%d"
        )

        folder_path = os.path.join(
            self.base_path,
            model_name,
            date_folder
        )

        os.makedirs(
            folder_path,
            exist_ok=True
        )

        return os.path.join(
            folder_path,
            "test_result.csv"
        )

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

        log_path = self.get_log_path(
            model_name,
            date
        )

        file_exists = os.path.exists(
            log_path
        )

        with open(
            log_path,
            mode="a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            if not file_exists:

                writer.writerow([
                    "Serial_Number",
                    "Attempt",
                    "Date",
                    "Time",
                    "Operator_ID",
                    "Model",
                    "Voltage",
                    "Current",
                    "Voltage_Lower",
                    "Voltage_Upper",
                    "Current_Lower",
                    "Current_Upper",
                    "Judgment"
                ])

            writer.writerow([
                serial_number,
                attempt,
                date.strftime("%d/%m/%Y"),
                time.strftime("%H:%M:%S"),
                operator_id,
                model_name,
                voltage,
                current,
                voltage_lower,
                voltage_upper,
                current_lower,
                current_upper,
                judgment
            ])