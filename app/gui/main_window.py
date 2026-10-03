from datetime import datetime

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
    QMessageBox
)

from app.database.database import Database
from app.database.operator_repository import OperatorRepository
from app.database.model_repository import ModelRepository
from app.database.batch_repository import BatchRepository
from app.core.serial_manager import SerialManager
from app.core.process import ProcessController
from app.instrument.instrument_simulator import InstrumentSimulator
from app.gui.admin_window import AdminWindow

class NGMessageBox(QMessageBox):

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            return

        super().keyPressEvent(event)

    def closeEvent(self, event):

        # Jangan izinkan popup ditutup dengan tombol X
        event.ignore()


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

        self.batch_repository = BatchRepository(
            self.database
        )

        self.operator_valid  = False

        self.setWindowTitle("Voltage Checker System")
        self.setMinimumSize(1100, 750)

        self.serial_manager = SerialManager()
        self.process_controller = None

        self.setup_ui()
        self.load_models()

    def load_models(self):

        models = self.model_repository.get_all_models()

        self.model_combo.clear()

        for model in models:
            model_name = model[1]
            self.model_combo.addItem(model_name)

    def load_process(self):

        operator_id = self.operator_input.text().strip()

        instrument = InstrumentSimulator()

        self.process_controller = ProcessController(
            serial_manager=self.serial_manager,
            batch_repository=self.batch_repository,
            model_repository=self.model_repository,
            instrument=instrument,
            operator_id=operator_id
        )

        if not self.process_controller.validate_operator():
            self.statusBar().showMessage(
                "Gagal memvalidasi operator"
            )
            return

        if not self.process_controller.load_active_batch():
            self.statusBar().showMessage(
                "Tidak ada batch aktif"
            )
            return

        self.process_controller.wait_for_serial()

        self.update_expected_serial()

        self.statusBar().showMessage(
            "Batch siap | Silakan masukkan Serial Number"
        )

    def on_model_changed(self):

        model_name = self.model_combo.currentText()

        if not model_name:
            return

        model = self.model_repository.get_model(
            model_name
        )

        if model is None:
            return

        self.voltage_lower.setText(
            "{:.2f} V".format(
                model["voltage_lower"]
            )
        )

        self.voltage_upper.setText(
            "{:.2f} V".format(
                model["voltage_upper"]
            )
        )

        self.current_lower.setText(
            "{:.3f} A".format(
                model["current_lower"]
            )
        )

        self.current_upper.setText(
            "{:.3f} A".format(
                model["current_upper"]
            )
        )

    def reset_serial_input(self):
        self.serial_input.clear()
        self.serial_input.setFocus()
        self.start_button.setEnabled(False)
        self.judgment_label.setText("READY")

    def add_result_to_table(
        self,
        judgment,
        operator_id,
        model,
        serial_number
    ):

        now = datetime.now()

        # Cek apakah Serial Number sudah ada di tabel
        existing_row = -1

        for row in range(self.result_table.rowCount()):

            item = self.result_table.item(row, 6)

            if item is not None:
                if item.text() == serial_number:
                    existing_row = row
                    break

        if existing_row != -1:

            row = existing_row

        else:

            self.result_table.insertRow(0)
            row = 0

        values = [
            "",
            judgment,
            now.strftime("%d/%m/%Y"),
            now.strftime("%H:%M:%S"),
            operator_id,
            model,
            serial_number
        ]

        for column, value in enumerate(values):

            item = QTableWidgetItem(str(value))

            self.result_table.setItem(
                row,
                column,
                item
            )

        if row != 0:

            self.result_table.removeRow(row)
            self.result_table.insertRow(0)

            for column, value in enumerate(values):

                item = QTableWidgetItem(str(value))

                self.result_table.setItem(
                    0,
                    column,
                    item
                )

        while self.result_table.rowCount() > 10:

            self.result_table.removeRow(
                self.result_table.rowCount() - 1
            )

        for row in range(self.result_table.rowCount()):

            self.result_table.setItem(
                row,
                0,
                QTableWidgetItem(str(row + 1))
            )


    def validate_operator(self):

        operator_id = self.operator_input.text().strip()

        if not operator_id:
         
            self.operator_valid = False

            self.start_button.setEnabled(False)

            self.operator_input.setReadOnly(False)
            self.operator_input.setStyleSheet("")

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

            self.operator_input.setReadOnly(False)
            self.operator_input.setStyleSheet("")

            self.statusBar().showMessage(
                "Operator ID tidak terdaftar"
            )

            return

        self.operator_valid = True

        self.statusBar().showMessage(
            "Operator valid: {}".format(
                operator["name"]
            )
        )

        self.load_process()
        self.operator_input.setReadOnly(True)
        self.operator_input.setStyleSheet("""
            QLineEdit {
                background-color: #e0e0e0;
                color: #555555;
            }
        """)
        self.serial_input.setFocus()


    def update_expected_serial(self):

        if self.process_controller is None:
            return

        expected_serial = (
            self.process_controller.get_expected_serial()
        )

        if expected_serial is None:
            return

        self.serial_input.setPlaceholderText(
            "Expected: {}".format(
                expected_serial
            )
        )

    def validate_serial(self):
        serial_number = self.serial_input.text().strip()

        if self.process_controller is None:
            self.statusBar().showMessage(
                "Process belum siap"
            )
            return

        if not serial_number:
            self.statusBar().showMessage(
                "Serial Number belum diisi"
            )
            return

        valid = self.process_controller.validate_serial(
            serial_number
        )

        if not valid:
            self.start_button.setEnabled(False)
            self.judgment_label.setText("SERIAL NG")
            self.statusBar().showMessage(
                "Serial Number tidak sesuai"
            )
            return

        self.start_button.setEnabled(True)
        self.judgment_label.setText("READY")
        self.statusBar().showMessage(
            "Serial Number valid | Siap melakukan test"
        )

        self.start_button.setFocus()


    def start_test(self):

        if self.process_controller is None:
            self.statusBar().showMessage(
                "Process belum siap"
            )
            return

        serial_number = self.serial_input.text().strip()

        if not serial_number:
            self.statusBar().showMessage(
                "Serial Number belum diisi"
            )
            return

        try:
            self.process_controller.start_test()

            self.judgment_label.setText("TESTING")

            self.start_button.setEnabled(False)

            result = self.process_controller.run_test()

            voltage = result["voltage"]
            current = result["current"]
            judgment = result["judgment"]

            self.voltage_value.setText(
                "{:.2f} V".format(voltage)
            )

            self.current_value.setText(
                "{:.3f} A".format(current)
            )

            self.process_controller.process_result(
                judgment
            )

            self.process_controller.log_test_result(
                serial_number=serial_number,
                voltage=voltage,
                current=current,
                judgment=judgment
            )

            self.add_result_to_table(
                judgment=judgment,
                operator_id=self.operator_input.text().strip(),
                model=self.model_combo.currentText(),
                serial_number=serial_number
            )

            self.judgment_label.setText(judgment)

            self.statusBar().showMessage(
                "Test selesai | Hasil: {}".format(judgment)
            )

            if judgment == "OK":

                self.process_controller.complete_test()

                self.reset_serial_input()

            elif judgment == "NG":

                self.show_ng_popup(serial_number)

        except Exception as error:

            self.judgment_label.setText(
                "ERROR"
            )

            self.statusBar().showMessage(
                "Test error: {}".format(error)
            )

            print(
                "Test error:",
                error
            )

            try:

                self.process_controller.recover_from_error()

                self.start_button.setEnabled(
                    False
                )

                self.reset_serial_input()

                self.statusBar().showMessage(
                    "Test error | Silakan scan Serial Number kembali"
                )

            except Exception as recovery_error:

                self.statusBar().showMessage(
                    "Recovery error: {}".format(
                        recovery_error
                    )
                )

                print(
                    "Recovery error:",
                    recovery_error
                )

    def show_ng_popup(self, serial_number):

        message_box = QMessageBox(self)

        message_box.setWindowTitle("Hasil Test NG")

        message_box.setText(
            "Hasil test adalah NG.\n\n"
            "Serial Number: {}".format(serial_number)
        )

        message_box.setInformativeText(
            "Silakan pilih RETEST atau ACCEPT NG."
        )

        retest_button = message_box.addButton(
            "RETEST",
            QMessageBox.AcceptRole
        )

        accept_ng_button = message_box.addButton(
            "ACCEPT NG",
            QMessageBox.AcceptRole
        )

        message_box.exec_()

        clicked_button = message_box.clickedButton()

        if clicked_button == retest_button:

            self.handle_retest()

        elif clicked_button == accept_ng_button:

            self.handle_accept_ng()

        else:
            self.judgment_label.setText("NG")

            self.start_button.setEnabled(False)

            self.statusBar().showMessage(
                "Hasil NG | Silakan pilih RETEST atau ACCEPT NG"
            )


    def handle_retest(self):

        try:
            self.process_controller.retest()
            self.judgment_label.setText("RETEST")

            self.statusBar().showMessage(
                "Retest dipilih | Silakan lakukan test kembali"
            )

            self.start_button.setEnabled(True)

        except Exception as error:

            self.judgment_label.setText("ERROR")

            self.statusBar().showMessage(
                "Retest error: {}".format(error)
            )

            print("Retest error:", error)

    def handle_accept_ng(self):

        try:
            self.process_controller.accept_ng()

            self.judgment_label.setText("NG")

            self.update_expected_serial()

            self.statusBar().showMessage(
                "NG diterima | Serial berikutnya siap"
            )

            self.start_button.setEnabled(False)
            self.reset_serial_input()

        except Exception as error:

            self.judgment_label.setText("ERROR")

            self.statusBar().showMessage(
                "Accept NG error: {}".format(error)
            )

            print("Accept NG error:", error)


    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        title_label = QLabel("Voltage Checker System")
        title_label.setAlignment(Qt.AlignCenter)

        admin_button = QPushButton(
            "ADMIN SETTING"
        )

        admin_button.clicked.connect(
            self.open_admin_setting
        )

        admin_layout = QHBoxLayout()

        admin_layout.addStretch()

        admin_layout.addWidget(
            admin_button
        )

        main_layout.addLayout(
            admin_layout
        )

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
        self.operator_input.returnPressed.connect(self.validate_operator)

        self.validate_button = QPushButton("VALIDATE")

        self.validate_button.clicked.connect(
            self.validate_operator
        )

        input_layout.addWidget(operator_label, 0, 0)
        input_layout.addWidget(self.operator_input, 0, 1)
        input_layout.addWidget(self.validate_button, 0, 2)




        serial_label = QLabel("Serial Number")
        
        self.serial_input = QLineEdit()
        self.serial_input.setPlaceholderText("Enter Serial Number")

        self.serial_input.returnPressed.connect(
            self.validate_serial
        )

        input_layout.addWidget(serial_label, 1, 0)
        input_layout.addWidget(self.serial_input, 1, 1, 1, 2)



        model_label = QLabel("Model")

        self.model_combo = QComboBox()

        self.model_combo.currentIndexChanged.connect(
            self.on_model_changed
        )

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
        self.start_button.clicked.connect(
            self.start_test
        )

        self.start_button.setShortcut("Return")

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

    def open_admin_setting(self):

        self.admin_window = AdminWindow(
            self.database
        )

        self.admin_window.setWindowModality(
            Qt.ApplicationModal
        )

        self.admin_window.show()
        
