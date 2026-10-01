from app.database.database import Database
from app.database.batch_repository import BatchRepository
from app.database.model_repository import ModelRepository

from app.core.serial_manager import SerialManager
from app.core.process import ProcessController


database = Database()
database.create_tables()


batch_repository = BatchRepository(
    database
)

model_repository = ModelRepository(
    database
)

serial_manager = SerialManager()


test_process = ProcessController(
    serial_manager,
    batch_repository,
    model_repository
)


# =====================================
# Load batch
# =====================================

loaded = test_process.load_active_batch()

if not loaded:

    print("Tidak ada batch aktif.")

else:

    print("Batch berhasil di-load.")

    print(
        "Model:",
        test_process.model_name
    )

    print(
        "Expected Serial:",
        test_process.get_expected_serial()
    )


    # =================================
    # Test measurement
    # =================================

    print("\nTest Measurement 1")

    voltage = 24.00
    current = 0.150

    result = test_process.judge_measurement(
        voltage,
        current
    )

    print("Voltage:", voltage)
    print("Current:", current)
    print("Judgment:", result)


    # =================================
    # Test measurement 2
    # =================================

    print("\nTest Measurement 2")

    voltage = 22.50
    current = 0.150

    result = test_process.judge_measurement(
        voltage,
        current
    )

    print("Voltage:", voltage)
    print("Current:", current)
    print("Judgment:", result)