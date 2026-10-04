import pyvisa


def print_resources(resources):
    print()
    print("Available VISA resources:")

    if not resources:
        print("  Tidak ada VISA resource yang terdeteksi.")
        return

    for index, resource in enumerate(resources, start=1):
        print("  {}. {}".format(index, resource))


def select_resource(resources):
    while True:
        try:
            choice = int(
                input("\nSelect resource [1-{}]: ".format(
                    len(resources)
                ))
            )

            if 1 <= choice <= len(resources):
                return resources[choice - 1]

            print("Pilihan tidak valid.")

        except ValueError:
            print("Masukkan nomor resource.")


def test_dmm(resource_name):
    resource_manager = None
    instrument = None

    try:
        print()
        print("=" * 50)
        print("DMM Communication Test")
        print("=" * 50)

        print()
        print("Resource:")
        print("  {}".format(resource_name))

        print()
        print("Opening VISA Resource Manager...")

        resource_manager = pyvisa.ResourceManager()

        print("Opening instrument...")

        instrument = resource_manager.open_resource(
            resource_name
        )

        instrument.timeout = 5000

        print("Connected.")

        print()
        print("Querying DMM identification...")

        identification = instrument.query(
            "*IDN?"
        ).strip()

        print()
        print("DMM Identification:")
        print("  {}".format(identification))

        print()
        print("Testing voltage measurement...")

        voltage_response = instrument.query(
            "MEAS:VOLT?"
        ).strip()

        voltage = float(voltage_response)

        print("  Voltage: {:.6f} V".format(voltage))

        print()
        print("Testing current measurement...")

        current_response = instrument.query(
            "MEAS:CURR?"
        ).strip()

        current = float(current_response)

        print("  Current: {:.6f} A".format(current))

        print()
        print("=" * 50)
        print("Communication test PASSED")
        print("=" * 50)

        return True

    except Exception as error:

        print()
        print("=" * 50)
        print("Communication test FAILED")
        print("=" * 50)

        print()
        print("Error:")
        print("  {}".format(error))

        return False

    finally:

        if instrument is not None:
            try:
                instrument.close()
            except Exception:
                pass

        if resource_manager is not None:
            try:
                resource_manager.close()
            except Exception:
                pass


def main():

    print("=" * 50)
    print("Real DMM VISA Test Tool")
    print("=" * 50)

    try:
        resource_manager = pyvisa.ResourceManager()

    except Exception as error:

        print()
        print("Failed to open VISA Resource Manager.")
        print("Error:")
        print("  {}".format(error))

        return

    try:
        resources = resource_manager.list_resources()

    except Exception as error:

        print()
        print("Failed to list VISA resources.")
        print("Error:")
        print("  {}".format(error))

        resource_manager.close()
        return

    print_resources(resources)

    resource_manager.close()

    if not resources:
        print()
        print("Tidak ada resource yang bisa dites.")
        print("Pastikan DMM sudah terhubung.")
        return

    resource_name = select_resource(resources)

    test_dmm(resource_name)


if __name__ == "__main__":
    main()