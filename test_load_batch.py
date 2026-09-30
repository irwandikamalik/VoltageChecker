from app.database.database import Database
from app.database.batch_repository import BatchRepository
from app.core.serial_manager import SerialManager


database = Database()

database.create_tables()

batch_repository = BatchRepository(database)

serial_manager = SerialManager()


# Ambil batch aktif dari database
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

    print("Batch ditemukan:")
    print("ID:", batch_id)
    print("Batch Code:", batch_code)
    print("Model:", model_name)
    print("Created:", created_at)
    print("Sequence:", sequence_number)
    print("Status:", status)

    # Load batch ke SerialManager
    serial_manager.load_batch(
        batch_code,
        sequence_number
    )

    print("\nExpected Serial:")

    print(
        serial_manager.get_expected_serial()
    )

    serial_manager.next_serial()

    print("\nExpected Serial setelah next:")

    print(
        serial_manager.get_expected_serial()
    )