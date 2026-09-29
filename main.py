import sys

from PySide2.QtWidgets import QApplication

from app.gui.main_window import MainWindow
from app.database.database import Database
from app.database.operator_repository import OperatorRepository


def main():
    # DATABASES
    database = Database()

    database.create_tables()

    print("Database berhasil dibuat.")
    print("Database path: ", database.db_path)

    # OPERATOR REPOSITORY
    operator_repository = OperatorRepository(database)

    operator_repository.add_operator(
        "OP001",
        "Budi"
    )

    operator_repository.add_operator(
        "OP002",
        "Andi"
    )

    # TEST VALIDATION
    print(
        "OP001: ",
        operator_repository.is_valid_operator("OP001")
    )

    print(
        "OP999:",
        operator_repository.is_valid_operator("OP999")
    )

    # GET  OPERATOR
    operator = operator_repository.get_operator("OP001")

    print("Operator:", operator)

    # GET ALL OPERATORS
    operators = operator_repository.get_all_operators()
    print("Semua operator:")

    for operator in operators:
        print(operator)
    

    # GUI
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()