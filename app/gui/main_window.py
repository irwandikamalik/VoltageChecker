from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QFrame,
)

from app.database.database import Database
from app.database.operator_repository import OperatorRepository
from app.database.model_repository import ModelRepository


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.database = Database()
        self.database.create_tables()

        self.operator_repository = OperatorRepository(
            self.database
        )

        self.model_repository = ModelRepository(
            self.database
        )

        self.operator_valid  = False

        self.setWindowTitle("Voltage Checker System")
        self.setMinimumSize(1100, 750)

        self.setup_ui()
        self.load_models()

    def load_models(self):

        models = self.model_repository.get_all_models()

        self.model_combo.clear()

        for model in models:
            model_name = model[1]
            self.model_combo.addItem(model_name)

    def validateOperator(self):

        operator_id = self.operator_input.text().strip()

        if not operator_id:
         
            self.operator_valid = False

            self.start_button.setEnabled(False)

            self.statusBar().showMessage(
                "Operator ID belum diisi"
            )

            return
        operator = self.operator_repository.get_operator(
            operator_id
        )

        if operator is None:

            self.operator_valid = False

            self.start_button.setEnabled(False)

            self.statusBar().showMessage(
                "Operator ID tidak terdaftar"
            )

            return

        self.operator_valid = True

        self.start_button.setEnabled(True)

        self.statusBar().showMessage(
            "Operator valid: {}".format(
                operator["name"]
            )
        )

    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        title_label = QLabel("Voltage Checker System")
        title_label.setAlignment(Qt.AlignCenter)

        # TITLE
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                padding: 15px;
                }
        """)

        main_layout.addWidget(title_label)

        # INPUT SECTION
        input_group = QGroupBox("Test Information")
        input_layout = QGridLayout()



        operator_label = QLabel("Operator ID")

        self.operator_input = QLineEdit()
        self.operator_input.setPlaceholderText("Enter Operator ID")

        self.validate_button = QPushButton("VALIDATE")

        self.validate_button.clicked.connect(
            self.validateOperator
        )

        input_layout.addWidget(operator_label, 0, 0)
        input_layout.addWidget(self.operator_input, 0, 1)
        input_layout.addWidget(self.validate_button, 0, 2)




        serial_label = QLabel("Serial Number")
        
        self.serial_input = QLineEdit()
        self.serial_input.setPlaceholderText("Enter Serial Number")

        input_layout.addWidget(serial_label, 1, 0)
        input_layout.addWidget(self.serial_input, 1, 1, 1, 2)



        model_label = QLabel("Model")

        self.model_combo = QComboBox()
        self.model_combo.addItem("MODEL-A")
        self.model_combo.addItem("MODEL-B")

        input_layout.addWidget(model_label, 2, 0)
        input_layout.addWidget(self.model_combo, 2, 1, 1, 2)

        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)



        # Measurement Section
        measurement_layout = QHBoxLayout()

        voltage_group = QGroupBox("VOLTAGE")

        voltage_layout = QVBoxLayout()

        self.voltage_value = QLabel("--.-- V")
        self.voltage_value.setAlignment(Qt.AlignCenter)

        self.voltage_value.setStyleSheet(""" 
            QLabel {
                font-size: 40px;
                font-weight: bold;
                padding: 20px;
            }
        """)

        voltage_layout.addWidget(self.voltage_value)

        voltage_group.setLayout(voltage_layout)


        current_group = QGroupBox("CURRENT")

        current_layout = QVBoxLayout()

        self.current_value = QLabel("--.-- A")
        self.current_value.setAlignment(Qt.AlignCenter)

        self.current_value.setStyleSheet(""" 
            QLabel {
                font-size: 40px;
                font-weight: bold;
                padding: 20px;
            }
        """)

        current_layout.addWidget(self.current_value)

        current_group.setLayout(current_layout)

        measurement_layout.addWidget(voltage_group)
        measurement_layout.addWidget(current_group)

        main_layout.addLayout(measurement_layout)


        # LIMIT SECTION
        limit_group = QGroupBox("Test Limits")

        limit_layout = QGridLayout()

        voltage_limit_label = QLabel("Voltage")

        self.voltage_lower = QLabel("23.00 V")
        self.voltage_upper = QLabel("25.00 V")

        limit_layout.addWidget(
            voltage_limit_label,
            0,
            0
        )

        limit_layout.addWidget(
            QLabel("Lower:"),
            0,
            1
        )

        limit_layout.addWidget(
            self.voltage_lower,
            0,
            2
        )

        limit_layout.addWidget(
            QLabel("Upper:"),
            0,
            3
        )

        limit_layout.addWidget(
            self.voltage_upper,
            0,4
        )


        current_limit_label = QLabel("Current")

        self.current_lower = QLabel("0.100 A")
        self.current_upper = QLabel("0.200 A")

        limit_layout.addWidget(
            current_limit_label,
            1,
            0
        )

        limit_layout.addWidget(
            QLabel("Lower:"),
            1,
            1
        )

        limit_layout.addWidget(
            self.current_lower,
            1,
            2
        )

        limit_layout.addWidget(
            QLabel("Upper:"),
            1,
            3
        )

        limit_layout.addWidget(
            self.current_upper,
            1,
            4
        )

        limit_group.setLayout(limit_layout)

        main_layout.addWidget(limit_group)



        # TEST SECTION

        test_layout = QVBoxLayout()

        self.start_button = QPushButton("START TEST")
        self.start_button.setEnabled(False)
        self.start_button.setMinimumHeight(50)

        self.judgment_label = QLabel("READY")
        self.judgment_label.setAlignment(Qt.AlignCenter)

        self.judgment_label.setStyleSheet(""" 
            QLabel {
                font-size: 30px;
                font-weight: bold;
                padding: 15px;
            }
        """)

        test_layout.addWidget(self.start_button)
        test_layout.addWidget(self.judgment_label)

        main_layout.addLayout(test_layout)




        # RESULT TABLE

        result_group = QGroupBox("Last 10 Test Results")

        result_layout = QVBoxLayout()

        self.result_table = QTableWidget()

        self.result_table.setColumnCount(7)

        self.result_table.setHorizontalHeaderLabels([
            "NO",
            "Judgment",
            "Date",
            "Time",
            "Operator ID",
            "Model",
            "Serial Number",
        ])

        self.result_table.setRowCount(0)

        self.result_table.horizontalHeader().setStretchLastSection(True)

        result_layout.addWidget(self.result_table)

        result_group.setLayout(result_layout)

        main_layout.addWidget(result_group)


        # STATUS BAR

        self.statusBar().showMessage(
            "Instrument: DISCONNECTED | Status: READY"
        )