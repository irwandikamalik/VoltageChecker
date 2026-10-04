import pyvisa


def main():

    print("=" * 50)
    print("VISA Environment Check")
    print("=" * 50)

    try:
        resource_manager = pyvisa.ResourceManager()

        print()
        print("PyVISA version:")
        print("  {}".format(pyvisa.__version__))

        print()
        print("VISA backend:")
        print("  {}".format(
            resource_manager.visalib
        ))

        print()
        print("Resource Manager:")
        print("  {}".format(
            resource_manager
        ))

        print()
        print("VISA resources:")

        resources = resource_manager.list_resources()

        if resources:
            for resource in resources:
                print("  {}".format(resource))
        else:
            print("  Tidak ada resource.")

        print()
        print("VISA environment check PASSED.")

        resource_manager.close()

    except Exception as error:

        print()
        print("VISA environment check FAILED.")

        print()
        print("Error:")
        print("  {}".format(error))


if __name__ == "__main__":
    main()