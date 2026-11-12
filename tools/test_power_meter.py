import pyvisa
import time

rm = pyvisa.ResourceManager()

print ("List: ", rm.list_resources())

wt310e = "USB0::0x0B21::0x0025::43335348303130303145::INSTR"
instrument = rm.open_resource(wt310e)

instrument.timeout = 5000

try:
    idn = instrument.query("*IDN?")
    print(f"Instrument: {idn}")

    instrument.write(":NUMERIC:NORMAL:ITEM1 U,1")

    voltage = float(
        instrument.query(":NUMERIC:NORMAL:VALUE? 1")
    )

    print(f"Voltage: {voltage:.3f} V")


    instrument.write(":NUMERIC:NORMAL:ITEM2 I,1")

    current = float(
        instrument.query(":NUMERIC:NORMAL:VALUE? 2")
    )

    print(f"Current: {current:.3f} A")

finally:
    instrument.close()
    rm.close()
    print("Instrument close!")