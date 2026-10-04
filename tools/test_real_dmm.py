import argparse

import pyvisa


DEFAULT_TIMEOUT = 5000


def create_resource_manager(backend=None):

    if backend:
        return pyvisa.ResourceManager(
            backend
        )

    return pyvisa.ResourceManager()


def list_resources(resource_manager):

    return resource_manager.list_resources()


def print_resources(resources):

    print()
    print("Available VISA resources:")

    if not resources:

        print("  No VISA resources detected.")

        return

    for index, resource in enumerate(
        resources,
        start=1
    ):

        print(
            "  {}. {}".format(
                index,
                resource
            )
        )


def select_resource(resources):

    while True:

        try:

            choice = int(
                input(
                    "\nSelect resource [1-{}]: ".format(
                        len(resources)
                    )
                )
            )

            if 1 <= choice <= len(resources):

                return resources[
                    choice - 1
                ]

            print("Pilihan tidak valid.")

        except ValueError:

            print(
                "Masukkan nomor resource."
            )


def test_dmm(
    resource_name,
    backend=None,
    timeout=DEFAULT_TIMEOUT
):

    resource_manager = None
    instrument = None

    try:

        print()
        print("=" * 50)
        print("DMM Communication Test")
        print("=" * 50)

        print()
        print("Backend:")
        print(
            "  {}".format(
                backend or "default"
            )
        )

        print()
        print("Resource:")
        print(
            "  {}".format(
                resource_name
            )
        )

        print()
        print("Opening VISA Resource Manager...")

        resource_manager = (
            create_resource_manager(
                backend
            )
        )

        print("Opening instrument...")

        instrument = (
            resource_manager.open_resource(
                resource_name
            )
        )

        instrument.timeout = timeout

        print("Connected.")

        # -------------------------------------------------
        # Identification
        # -------------------------------------------------

        print()
        print("Testing identification...")

        identification = (
            instrument.query(
                "*IDN?"
            ).strip()
        )

        if not identification:

            raise RuntimeError(
                "DMM tidak memberikan response dari *IDN?."
            )

        print()
        print("DMM Identification:")
        print(
            "  {}".format(
                identification
            )
        )

        print()
        print("Identification test PASSED.")

        # -------------------------------------------------
        # Voltage
        # -------------------------------------------------

        print()
        print("Testing voltage measurement...")

        voltage_response = (
            instrument.query(
                "MEAS:VOLT?"
            ).strip()
        )

        voltage = float(
            voltage_response
        )

        print(
            "  Voltage: {:.6f} V".format(
                voltage
            )
        )

        print(
            "Voltage measurement PASSED."
        )

        # -------------------------------------------------
        # Current
        # -------------------------------------------------

        print()
        print("Testing current measurement...")

        current_response = (
            instrument.query(
                "MEAS:CURR?"
            ).strip()
        )

        current = float(
            current_response
        )

        print(
            "  Current: {:.6f} A".format(
                current
            )
        )

        print(
            "Current measurement PASSED."
        )

        # -------------------------------------------------
        # Result
        # -------------------------------------------------

        print()
        print("=" * 50)
        print("DMM COMMUNICATION TEST PASSED")
        print("=" * 50)

        return True

    except Exception as error:

        print()
        print("=" * 50)
        print("DMM COMMUNICATION TEST FAILED")
        print("=" * 50)

        print()
        print("Error:")
        print(
            "  {}".format(
                error
            )
        )

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


def parse_arguments():

    parser = argparse.ArgumentParser(
        description=(
            "Diagnostic tool for testing "
            "a real DMM through PyVISA."
        )
    )

    parser.add_argument(
        "--resource",
        help=(
            "VISA resource name, "
            "for example GPIB0::22::INSTR"
        )
    )

    parser.add_argument(
        "--backend",
        help=(
            "VISA backend, "
            "for example @py"
        )
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=(
            "VISA timeout in milliseconds."
        )
    )

    return parser.parse_args()


def main():

    args = parse_arguments()

    print("=" * 50)
    print("Real DMM Diagnostic Tool")
    print("=" * 50)

    resource_manager = None

    try:

        resource_manager = (
            create_resource_manager(
                args.backend
            )
        )

        # -------------------------------------------------
        # Direct resource mode
        # -------------------------------------------------

        if args.resource:

            test_dmm(
                resource_name=args.resource,
                backend=args.backend,
                timeout=args.timeout
            )

            return

        # -------------------------------------------------
        # Discovery mode
        # -------------------------------------------------

        print()
        print("Backend:")
        print(
            "  {}".format(
                args.backend or "default"
            )
        )

        print()
        print("Scanning VISA resources...")

        resources = list_resources(
            resource_manager
        )

        print_resources(
            resources
        )

    except Exception as error:

        print()
        print("VISA initialization failed.")

        print()
        print("Error:")
        print(
            "  {}".format(
                error
            )
        )

        return

    finally:

        if resource_manager is not None:

            try:
                resource_manager.close()

            except Exception:
                pass

    if not resources:

        print()
        print(
            "Tidak ada VISA resource."
        )

        print(
            "Gunakan --resource jika "
            "ingin mengetes resource secara langsung."
        )

        return

    resource_name = select_resource(
        resources
    )

    test_dmm(
        resource_name=resource_name,
        backend=args.backend,
        timeout=args.timeout
    )


if __name__ == "__main__":
    main()