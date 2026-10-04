import pyvisa


def main():

    print("=" * 50)
    print("VISA Resource Discovery")
    print("=" * 50)

    resource_manager = None

    try:
        resource_manager = pyvisa.ResourceManager()

        print()
        print("Backend:")
        print("  {}".format(
            resource_manager.visalib
        ))

        print()
        print("Scanning VISA resources...")

        resources = resource_manager.list_resources()

        print()

        if not resources:

            print("No VISA resources detected.")

        else:

            print("Detected resources:")

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

        print()
        print("Discovery completed.")

    except Exception as error:

        print()
        print("Discovery FAILED.")

        print()
        print("Error:")
        print("  {}".format(error))

    finally:

        if resource_manager is not None:

            try:
                resource_manager.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()