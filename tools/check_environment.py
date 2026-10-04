import sys
import importlib


REQUIRED_PYTHON = (3, 8)


REQUIRED_PACKAGES = [
    ("PySide2", "PySide2"),
    ("PyVISA", "pyvisa"),
    ("PyVISA-Py", "pyvisa_py"),
    ("PySerial", "serial"),
    ("psutil", "psutil"),
    ("zeroconf", "zeroconf"),
    ("pytest", "pytest")
]


def print_header(title):

    print()
    print("=" * 50)
    print(title)
    print("=" * 50)


def check_python():

    print()
    print("Python")

    version = sys.version_info

    version_string = (
        "{}.{}.{}".format(
            version.major,
            version.minor,
            version.micro
        )
    )

    print(
        "  Version: {}".format(
            version_string
        )
    )

    if (version.major, version.minor) >= REQUIRED_PYTHON:

        print("  Status: PASS")

        return True

    print(
        "  Status: FAIL"
    )

    print(
        "  Required: Python {}.{}".format(
            REQUIRED_PYTHON[0],
            REQUIRED_PYTHON[1]
        )
    )

    return False


def check_package(display_name, import_name):

    print()
    print(display_name)

    try:

        module = importlib.import_module(
            import_name
        )

        version = getattr(
            module,
            "__version__",
            "unknown"
        )

        print(
            "  Version: {}".format(
                version
            )
        )

        print("  Status: PASS")

        return True

    except ImportError:

        print("  Status: FAIL")

        print(
            "  Package tidak ditemukan."
        )

        return False

    except Exception as error:

        print("  Status: FAIL")

        print(
            "  Error: {}".format(
                error
            )
        )

        return False


def check_packages():

    results = []

    for display_name, import_name in (
        REQUIRED_PACKAGES
    ):

        result = check_package(
            display_name,
            import_name
        )

        results.append(result)

    return results


def main():

    print_header(
        "VoltageChecker Environment Check"
    )

    python_result = check_python()

    package_results = check_packages()

    all_passed = (
        python_result
        and all(package_results)
    )

    print_header(
        "Environment Check Result"
    )

    if all_passed:

        print()
        print(
            "ENVIRONMENT CHECK PASSED"
        )

    else:

        print()
        print(
            "ENVIRONMENT CHECK FAILED"
        )

    print()

    return all_passed


if __name__ == "__main__":

    success = main()

    if not success:
        sys.exit(1)