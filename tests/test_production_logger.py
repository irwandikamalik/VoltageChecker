import csv

from app.logger.production_logger import ProductionLogger


def test_get_log_path_creates_folder(tmp_path):

    logger = ProductionLogger(
        base_path=str(tmp_path)
    )

    from datetime import datetime

    date = datetime(2026, 10, 1)

    log_path = logger.get_log_path(
        "MODEL-A",
        date
    )

    assert log_path.endswith(
        "MODEL-A\\2026-10-01\\test_result.csv"
    )


def test_log_test_creates_csv(tmp_path):

    logger = ProductionLogger(
        base_path=str(tmp_path)
    )

    from datetime import datetime

    now = datetime(
        2026,
        10,
        1,
        10,
        30,
        15
    )

    logger.log_test(
        model_name="MODEL-A",
        serial_number="MDF2610011030150001",
        attempt=1,
        operator_id="OP001",
        voltage=24.0,
        current=0.150,
        judgment="OK",
        voltage_lower=23.0,
        voltage_upper=25.0,
        current_lower=0.100,
        current_upper=0.200,
        date=now,
        time=now
    )

    log_path = (
        tmp_path
        / "MODEL-A"
        / "2026-10-01"
        / "test_result.csv"
    )

    assert log_path.exists()


def test_log_test_writes_header_and_data(tmp_path):

    logger = ProductionLogger(
        base_path=str(tmp_path)
    )

    from datetime import datetime

    now = datetime(
        2026,
        10,
        1,
        10,
        30,
        15
    )

    logger.log_test(
        model_name="MODEL-A",
        serial_number="MDF2610011030150001",
        attempt=1,
        operator_id="OP001",
        voltage=24.0,
        current=0.150,
        judgment="OK",
        voltage_lower=23.0,
        voltage_upper=25.0,
        current_lower=0.100,
        current_upper=0.200,
        date=now,
        time=now
    )

    log_path = (
        tmp_path
        / "MODEL-A"
        / "2026-10-01"
        / "test_result.csv"
    )

    with open(
        log_path,
        mode="r",
        encoding="utf-8"
    ) as file:

        rows = list(
            csv.reader(file)
        )

    assert len(rows) == 2

    assert rows[0] == [
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
    ]

    assert rows[1] == [
        "MDF2610011030150001",
        "1",
        "01/10/2026",
        "10:30:15",
        "OP001",
        "MODEL-A",
        "24.0",
        "0.15",
        "23.0",
        "25.0",
        "0.1",
        "0.2",
        "OK"
    ]


def test_log_test_appends_without_duplicate_header(tmp_path):

    logger = ProductionLogger(
        base_path=str(tmp_path)
    )

    from datetime import datetime

    now = datetime(
        2026,
        10,
        1,
        10,
        30,
        15
    )

    logger.log_test(
        model_name="MODEL-A",
        serial_number="MDF2610011030150001",
        attempt=1,
        operator_id="OP001",
        voltage=22.0,
        current=0.150,
        judgment="NG",
        voltage_lower=23.0,
        voltage_upper=25.0,
        current_lower=0.100,
        current_upper=0.200,
        date=now,
        time=now
    )

    logger.log_test(
        model_name="MODEL-A",
        serial_number="MDF2610011030150001",
        attempt=2,
        operator_id="OP001",
        voltage=24.0,
        current=0.150,
        judgment="OK",
        voltage_lower=23.0,
        voltage_upper=25.0,
        current_lower=0.100,
        current_upper=0.200,
        date=now,
        time=now
    )

    log_path = (
        tmp_path
        / "MODEL-A"
        / "2026-10-01"
        / "test_result.csv"
    )

    with open(
        log_path,
        mode="r",
        encoding="utf-8"
    ) as file:

        rows = list(
            csv.reader(file)
        )

    assert len(rows) == 3

    # Header hanya satu
    assert rows[0][0] == "Serial_Number"

    # Attempt 1
    assert rows[1][1] == "1"
    assert rows[1][-1] == "NG"

    # Attempt 2
    assert rows[2][1] == "2"
    assert rows[2][-1] == "OK"