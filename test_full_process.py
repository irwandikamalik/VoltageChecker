from app.database.database import Database
from app.database.batch_repository import BatchRepository
from app.database.model_repository import ModelRepository

from app.core.serial_manager import SerialManager
from app.core.test_process import TestProcess

from app.instrument.instrument_simulator import (
    InstrumentSimulator
)


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


# =====================================
# Serial Manager
# =====================================

serial_manager = SerialManager()


# =====================================
# Instrument
# =====================================

instrument = InstrumentSimulator(
    voltage=22.50,
    current=0.150
)


# =====================================
# Test Process
# =====================================

test_process = TestProcess(
    serial_manager,
    batch_repository,
    model_repository,
    instrument
)


# =====================================
# Load batch
# =====================================

loaded = test_process.load_active_batch()


if not loaded:

    print("Tidak ada batch aktif.")

else:

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

    if not test_process.validate_serial(
        serial_number
    ):

        print("\n=== RESULT ===")

        print("Judgment: NG")

        print(
            "Serial Number tidak sesuai."
        )


    else:

        print(
            "\nSerial Number sesuai."
        )


        # =============================
        # Run Test
        # =============================

        result = (
            test_process
            .run_test()
        )


        print("\n=== MEASUREMENT ===")

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


        print("\n=== RESULT ===")

        print(
            "Judgment:",
            result["judgment"]
        )


        # =============================
        # Complete Test
        # =============================

        test_process.complete_test()


        print("\nTest selesai.")

        print(
            "Expected Serial berikutnya:"
        )

        print(
            test_process.get_expected_serial()
        )