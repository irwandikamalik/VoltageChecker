from app.instrument.instrument_simulator import (
    InstrumentSimulator
)


instrument = InstrumentSimulator(
    voltage=24.00,
    current=0.150
)


# =====================================
# Connect
# =====================================

connected = instrument.connect()

print(
    "Connected:",
    connected
)


# =====================================
# Read voltage
# =====================================

voltage = instrument.read_voltage()

print(
    "Voltage:",
    voltage,
    "V"
)


# =====================================
# Read current
# =====================================

current = instrument.read_current()

print(
    "Current:",
    current,
    "A"
)


# =====================================
# Disconnect
# =====================================

instrument.disconnect()