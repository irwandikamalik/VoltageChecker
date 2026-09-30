from app.database.database import Database
from app.database.batch_repository import BatchRepository
from app.core.serial_manager import SerialManager
from app.core.test_process import TestProcess


database = Database()
database.create_tables()

batch_repository = BatchRepository(database)

serial_manager = SerialManager()

test_process = TestProcess(
    serial_manager,
    batch_repository
)


# =====================================
# Load batch
# =====================================

loaded = test_process.load_active_batch()

if not loaded:

    print("Tidak ada batch aktif.")

else:

    print("Batch berhasil di-load.")

    print("\nExpected Serial:")

    print(
        test_process.get_expected_serial()
    )


    # =================================
    # Test serial
    # =================================

    serial_number = input(
        "\nMasukkan Serial Number: "
    ).strip()


    if not test_process.validate_serial(
        serial_number
    ):

        print("\nNG")
        print("Serial Number tidak sesuai.")

    else:

        print("\nSerial Number sesuai.")

        print("Test selesai.")

        test_process.complete_test()

        print("\nSequence berikutnya:")

        print(
            serial_manager.sequence_number
        )

        print("\nExpected Serial berikutnya:")

        print(
            test_process.get_expected_serial()
        )