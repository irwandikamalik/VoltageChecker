from app.database.database import Database
from app.database.batch_repository import BatchRepository
from app.core.serial_manager import SerialManager


database = Database()
database.create_tables()

batch_repository = BatchRepository(database)
serial_manager = SerialManager()


# =====================================
# 1. Load batch aktif
# =====================================

batch = batch_repository.get_active_batch()

if batch is None:

    print("Tidak ada batch aktif.")

else:

    batch_id = batch[0]
    batch_code = batch[1]
    model_name = batch[2]
    created_at = batch[3]
    sequence_number = batch[4]
    status = batch[5]

    print("Batch aktif:")
    print("Batch ID:", batch_id)
    print("Batch Code:", batch_code)
    print("Model:", model_name)
    print("Sequence:", sequence_number)


    # =====================================
    # 2. Load batch ke SerialManager
    # =====================================

    serial_manager.load_batch(
        batch_code,
        sequence_number
    )

    expected_serial = (
        serial_manager.get_expected_serial()
    )

    print("\nExpected Serial:")
    print(expected_serial)


    # =====================================
    # 3. Simulasi operator scan serial
    # =====================================

    scanned_serial = input(
        "\nMasukkan Serial Number: "
    ).strip()


    # =====================================
    # 4. Validasi serial
    # =====================================

    if not serial_manager.validate_serial(
        scanned_serial
    ):

        print("\nNG")
        print("Serial Number tidak sesuai.")

        print("\nSequence tetap:")
        print(
            serial_manager.sequence_number
        )

    else:

        print("\nSerial Number sesuai.")

        # =====================================
        # 5. Simulasi test selesai
        # =====================================

        print("Test selesai.")

        serial_manager.next_serial()


        # =====================================
        # 6. Simpan sequence ke database
        # =====================================

        batch_repository.update_sequence(
            batch_id,
            serial_manager.sequence_number
        )


        print("\nSequence berikutnya:")
        print(
            serial_manager.sequence_number
        )

        print("\nExpected Serial berikutnya:")
        print(
            serial_manager.get_expected_serial()
        )