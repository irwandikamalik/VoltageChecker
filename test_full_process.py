from app.database.database import Database
from app.database.batch_repository import BatchRepository
from app.database.model_repository import ModelRepository
from app.database.operator_repository import OperatorRepository


from app.core.serial_manager import SerialManager
from app.core.test_process import TestProcess

from app.instrument.instrument_simulator import (
    InstrumentSimulator
)

from app.core.test_state import TestState
import app.core.test_state
import app.core.test_process

print("test_state.py:", app.core.test_state.__file__)
print("test_process.py:", app.core.test_process.__file__)

# =====================================
# Database
# =====================================

database = Database()

database.create_tables()


# =====================================
# Repository
# =====================================

batch_repository = BatchRepository(
    database
)

model_repository = ModelRepository(
    database
)

operator_repository = OperatorRepository(
    database
)

# =====================================
# Serial Manager
# =====================================

serial_manager = SerialManager()


# =====================================
# Instrument
# =====================================

instrument = InstrumentSimulator(
    measurements=[
        {
            "voltage": 22.00,
            "current": 0.150
        },
        {
            "voltage": 24.00,
            "current": 0.150
        }
    ],
    fail_on_read=True
)

# =====================================
# Operator
# =====================================

operator_id = input(
    "\nOperator ID: "
).strip()

operator = operator_repository.get_operator(
    operator_id
)

if operator is None:

    print(
        "\nOperator ID tidak terdaftar."
    )

    exit()

else:

    print(
        "\nOperator:",
        operator["name"]
    )


# =====================================
# Test Process
# =====================================

test_process = TestProcess(
    serial_manager,
    batch_repository,
    model_repository,
    instrument,
    operator_id
)

if not test_process.validate_operator():

    print("\nOperator validation error.")
    exit()


print(
    "State after operator validation:",
    test_process.get_state()
)


# =====================================
# Load batch
# =====================================

loaded = test_process.load_active_batch()

if not loaded:

    print("Tidak ada batch aktif.")
    exit()


test_process.wait_for_serial()

print(
    "State after batch:",
    test_process.get_state()
)


print("=== BATCH ===")

print(
    "Model:",
    test_process.model_name
)

print(
    "Expected Serial:",
    test_process.get_expected_serial()
)

# =================================
# Serial Number
# =================================

serial_number = input(
    "\nScan Serial Number: "
).strip()


# =================================
# Validate Serial
# =================================

if not test_process.validate_serial(serial_number):

    print("\n=== RESULT ===")
    print("Judgment: NG")
    print("Serial Number tidak sesuai.")

else:

    print("\nSerial Number sesuai.")

    print(
        "State after serial validation:",
        test_process.get_state()
    )

    attempt = test_process.start_test()

    print(
        "State after start test:",
        test_process.get_state()
    )

    print(
        "\n=== TEST ==="
    )

    print(
        "Attempt:",
        attempt
    )

    try:
        result = (
            test_process
            .run_test()
        )

    except RuntimeError as error:

        test_process.state_manager.set_state(
            TestState.ERROR
        )

        print(
            "\n=== INSTRUMENT ERROR ==="
        )

        print(error)

        print(
            "State:",
            test_process.get_state()
        )

        exit()

    test_process.process_result(
        result["judgment"]
    )

    print(
        "State after result:",
        test_process.get_state()
    )

    test_process.log_test_result(
        serial_number=serial_number,
        voltage=result["voltage"],
        current=result["current"],
        judgment=result["judgment"]
    )

    print(
        "\n=== MEASUREMENT ==="
    )

    print(
        "Voltage:",
        result["voltage"],
        "V"
    )

    print(
        "Current:",
        result["current"],
        "A"
    )

    print(
        "\n=== RESULT ==="
    )

    print(
        "Judgment:",
        result["judgment"]
    )

    if result["judgment"] == "OK":

        test_process.complete_test()

    else:

        while True:

            choice = input(
                "\nRETEST atau ACCEPT NG? "
            ).strip().upper()

            if choice == "RETEST":

                test_process.state_manager.set_state(
                    TestState.RETEST
                )

                print(
                    "State after retest:",
                    test_process.get_state()
                )

                attempt = (
                    test_process
                    .start_test()
                )

                print(
                    "\n=== RETEST ==="
                )

                print(
                    "Attempt:",
                    attempt
                )

                result = (
                    test_process
                    .run_test()
                )

                test_process.process_result(
                    result["judgment"]
                )

                test_process.log_test_result(
                    serial_number=serial_number,
                    voltage=result["voltage"],
                    current=result["current"],
                    judgment=result["judgment"]
                )

                print(
                    "Voltage:",
                    result["voltage"],
                    "V"
                )

                print(
                    "Current:",
                    result["current"],
                    "A"
                )

                print(
                    "Judgment:",
                    result["judgment"]
                )

                if result["judgment"] == "OK":

                    test_process.complete_test()

                    break

            elif choice == "ACCEPT NG":

                print(
                    "\nNG diterima."
                )

                test_process.complete_test()

                break

            else:

                print(
                    "Pilihan tidak valid."
                )

    print(
        "\nTest selesai."
    )

    print(
        "Expected Serial berikutnya:"
    )

    print(
        test_process.get_expected_serial()
    )