from datetime import datetime

from app.logger.production_logger import (
    ProductionLogger
)


logger = ProductionLogger()


now = datetime.now()


logger.log_test(
    model_name="MODEL-A",
    serial_number="MDF2609302122490010",
    attempt=1,
    operator_id="OP001",
    voltage=22.50,
    current=0.150,
    judgment="NG",
    voltage_lower=23.00,
    voltage_upper=25.00,
    current_lower=0.100,
    current_upper=0.200,
    date=now,
    time=now
)


logger.log_test(
    model_name="MODEL-A",
    serial_number="MDF2609302122490010",
    attempt=2,
    operator_id="OP001",
    voltage=24.00,
    current=0.150,
    judgment="OK",
    voltage_lower=23.00,
    voltage_upper=25.00,
    current_lower=0.100,
    current_upper=0.200,
    date=now,
    time=now
)


print("Log berhasil dibuat.")