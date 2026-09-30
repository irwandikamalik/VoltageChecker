from app.core.serial_manager import SerialManager

serial_manager = SerialManager()

print("Batch sebelum dibuat:")
print(
    serial_manager.get_batch_code()
)


print("\nMembuat batch baru...")

serial_manager.create_batch()

print("\nBatch code:")
print(
    serial_manager.get_batch_code()
)

print("\nExpected Serial:")
print(
    serial_manager.get_expected_serial()
)

print("\nValidasi serial:")

expected_serial = serial_manager.get_expected_serial()

print(
    "Serial Benar:",
    serial_manager.validate_serial(
        expected_serial
    )
)

print(
    "Serial salah:",
    serial_manager.validate_serial(
        "MDF0000000000000000"
    )
)


print("\nSerial Berikutnya:")

serial_manager.next_serial()

print(
    serial_manager.get_expected_serial()
)


print("\nSerial berikutnya:")

serial_manager.next_serial()

print(
    serial_manager.get_expected_serial()
)