from datetime import datetime

from app.database.database import Database
from app.database.batch_repository import BatchRepository
from app.core.serial_manager import SerialManager


database = Database()

database.create_tables()

batch_repository = BatchRepository(database)

serial_manager = SerialManager()


# Membuat batch
serial_manager.create_batch()

batch_code = serial_manager.get_batch_code()

created_at = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)


print("Batch Code:")
print(batch_code)


# Simpan batch ke database
batch_repository.create_batch(
    batch_code,
    "MODEL-A",
    created_at
)


# Ambil batch aktif
batch = batch_repository.get_active_batch()


print("\nActive Batch:")

print(batch)