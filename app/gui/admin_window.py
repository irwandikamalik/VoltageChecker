from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QMessageBox
)

from app.database.operator_repository import OperatorRepository
from app.database.model_repository import ModelRepository
from app.database.admin_repository import AdminRepository


class AdminWindow(QMainWindow):

    def __init__(
        self,
        database
    ):

        super().__init__()

        self.database = database

        self.admin_repository = AdminRepository(database)
        self.operator_repository = OperatorRepository(database)
        self.model_repository = ModelRepository(database)

        self.setWindowTitle(
            "Voltage Checker - Admin Setting"
        )

        self.setMinimumSize(
            900,
            650
        )

        self.setup_login_ui()

    def setup_login_ui(self):

        self.setFixedSize(
            450,
            350
        )

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            50,
            35,
            50,
            35
        )

        main_layout.setSpacing(
            15
        )

        central_widget.setLayout(
            main_layout
        )

        # =========================
        # TITLE
        # =========================

        title = QLabel(
            "VOLTAGE CHECKER"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet("""
            QLabel {
                font-size: 26px;
                font-weight: bold;
            }
        """)

        main_layout.addWidget(
            title
        )

        subtitle = QLabel(
            "Administrator Login"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        subtitle.setStyleSheet("""
            QLabel {
                font-size: 15px;
            }
        """)

        main_layout.addWidget(
            subtitle
        )

        main_layout.addSpacing(
            15
        )

        # =========================
        # USERNAME
        # =========================

        username_label = QLabel(
            "Username"
        )

        username_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: bold;
            }
        """)

        main_layout.addWidget(
            username_label
        )

        username_input = QLineEdit()

        username_input.setPlaceholderText(
            "Masukkan username"
        )

        username_input.setMinimumHeight(
            40
        )

        username_input.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                border: 1px solid #999999;
                border-radius: 5px;
            }

            QLineEdit:focus {
                border: 2px solid #1976D2;
            }
        """)

        main_layout.addWidget(
            username_input
        )

        # =========================
        # PASSWORD
        # =========================

        password_label = QLabel(
            "Password"
        )

        password_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: bold;
            }
        """)

        main_layout.addWidget(
            password_label
        )

        password_input = QLineEdit()

        password_input.setPlaceholderText(
            "Masukkan password"
        )

        password_input.setEchoMode(
            QLineEdit.Password
        )

        password_input.setMinimumHeight(
            40
        )

        password_input.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                border: 1px solid #999999;
                border-radius: 5px;
            }

            QLineEdit:focus {
                border: 2px solid #1976D2;
            }
        """)

        main_layout.addWidget(
            password_input
        )

        # =========================
        # LOGIN BUTTON
        # =========================

        login_button = QPushButton(
            "LOGIN"
        )

        login_button.setMinimumHeight(
            45
        )

        login_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: #eeeeee;
            }

            QPushButton:pressed {
                background-color: #dddddd;
            }
        """)

        main_layout.addWidget(
            login_button
        )

        # =========================
        # LOGIN FUNCTION
        # =========================

        def login():

            username = (
                username_input
                .text()
                .strip()
            )

            password = (
                password_input
                .text()
            )

            if not username or not password:

                QMessageBox.warning(
                    self,
                    "Login",
                    "Username dan password harus diisi."
                )

                return

            if self.admin_repository.validate_admin(
                username,
                password
            ):

                self.setFixedSize(
                    900,
                    650
                )

                self.setup_ui()

                self.load_operators()
                self.load_models()

                self.operator_id_input.setFocus()

            else:

                QMessageBox.warning(
                    self,
                    "Login Gagal",
                    "Username atau password salah."
                )

                password_input.clear()

                password_input.setFocus()

        # =========================
        # KEYBOARD WORKFLOW
        # =========================

        login_button.clicked.connect(
            login
        )

        username_input.returnPressed.connect(
            password_input.setFocus
        )

        password_input.returnPressed.connect(
            login
        )

        username_input.setFocus()

        # =========================
        # CENTER WINDOW
        # =========================

        screen = self.screen()

        if screen:

            screen_geometry = (
                screen.availableGeometry()
            )

            window_geometry = (
                self.frameGeometry()
            )

            window_geometry.moveCenter(
                screen_geometry.center()
            )

            self.move(
                window_geometry.topLeft()
            )

        username_input.setFocus()

    def setup_ui(self):

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QVBoxLayout()

        central_widget.setLayout(
            main_layout
        )

        # TITLE

        title = QLabel(
            "ADMIN SETTING"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                padding: 15px;
            }
        """)

        main_layout.addWidget(
            title
        )

        # =========================
        # OPERATOR SECTION
        # =========================

        operator_group = QGroupBox(
            "Operator Management"
        )

        operator_layout = QVBoxLayout()

        form_layout = QGridLayout()

        operator_id_label = QLabel(
            "Operator ID"
        )

        self.operator_id_input = QLineEdit()

        self.operator_id_input.setPlaceholderText(
            "Contoh: OP003"
        )

        name_label = QLabel(
            "Name"
        )

        self.operator_name_input = QLineEdit()

        self.operator_name_input.setPlaceholderText(
            "Nama Operator"
        )

        self.operator_id_input.returnPressed.connect(
            self.operator_name_input.setFocus
        )   

        self.operator_name_input.returnPressed.connect(
            self.add_operator
        )

        form_layout.addWidget(
            operator_id_label,
            0,
            0
        )

        form_layout.addWidget(
            self.operator_id_input,
            0,
            1
        )

        form_layout.addWidget(
            name_label,
            1,
            0
        )

        form_layout.addWidget(
            self.operator_name_input,
            1,
            1
        )

        operator_layout.addLayout(
            form_layout
        )

        button_layout = QHBoxLayout()

        self.add_operator_button = QPushButton("ADD OPERATOR")

        self.delete_operator_button = QPushButton("DELETE SELECTED")

        self.add_operator_button.clicked.connect(
            self.add_operator
        )

        self.delete_operator_button.clicked.connect(
            self.delete_operator
        )

        button_layout.addWidget(
            self.add_operator_button
        )

        button_layout.addWidget(
            self.delete_operator_button
        )

        operator_layout.addLayout(
            button_layout
        )

        self.operator_table = QTableWidget()

        self.operator_table.setColumnCount(
            2
        )

        self.operator_table.setHorizontalHeaderLabels([
            "Operator ID",
            "Name"
        ])

        self.operator_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        operator_layout.addWidget(
            self.operator_table
        )

        operator_group.setLayout(
            operator_layout
        )

        main_layout.addWidget(
            operator_group
        )

        self.operator_table.itemSelectionChanged.connect(
            self.load_selected_operator
        )


        # =========================
        # MODEL SECTION
        # =========================

        model_group = QGroupBox(
            "Model Management"
        )

        model_layout = QVBoxLayout()

        model_form = QGridLayout()

        model_form.addWidget(
            QLabel("Model Name"),
            0,
            0
        )

        self.model_name_input = QLineEdit()

        self.model_name_input.setPlaceholderText(
            "Contoh: MODEL-A"
        )

        model_form.addWidget(
            self.model_name_input,
            0,
            1
        )

        model_form.addWidget(
            QLabel("Voltage Lower"),
            1,
            0
        )

        self.voltage_lower_input = QLineEdit()

        self.voltage_lower_input.setPlaceholderText(
            "Contoh: 21.50"
        )

        model_form.addWidget(
            self.voltage_lower_input,
            1,
            1
        )

        model_form.addWidget(
            QLabel("Voltage Upper"),
            2,
            0
        )

        self.voltage_upper_input = QLineEdit()

        self.voltage_upper_input.setPlaceholderText(
            "Contoh: 22.50"
        )

        model_form.addWidget(
            self.voltage_upper_input,
            2,
            1
        )
        
        model_form.addWidget(
            QLabel("Current Lower"),
            3,
            0
        )

        self.current_lower_input = QLineEdit()

        self.current_lower_input.setPlaceholderText(
            "Contoh: 0.100"
        )

        model_form.addWidget(
            self.current_lower_input,
            3,
            1
        )

        model_form.addWidget(
            QLabel("Current Upper"),
            4,
            0
        )

        self.current_upper_input = QLineEdit()

        self.current_upper_input.setPlaceholderText(
            "Contoh: 0.200"
        )

        model_form.addWidget(
            self.current_upper_input,
            4,
            1
        )

        self.model_name_input.returnPressed.connect(
            self.voltage_lower_input.setFocus
        )

        self.voltage_lower_input.returnPressed.connect(
            self.voltage_upper_input.setFocus
        )

        self.voltage_upper_input.returnPressed.connect(
            self.current_lower_input.setFocus
        )

        self.current_lower_input.returnPressed.connect(
            self.current_upper_input.setFocus
        )

        self.current_upper_input.returnPressed.connect(
            self.add_model
        )

        model_layout.addLayout(
            model_form
        )

        model_button_layout = QHBoxLayout()

        self.add_model_button = QPushButton(
            "ADD MODEL"
        )

        self.edit_model_button = QPushButton(
            "EDIT"
        )

        self.delete_model_button = QPushButton(
            "DELETE SELECTED"
        )

        self.add_model_button.clicked.connect(
            self.add_model
        )

        self.edit_model_button.clicked.connect(
            self.edit_model
        )

        self.delete_model_button.clicked.connect(
            self.delete_model
        )

        model_button_layout.addWidget(
            self.add_model_button
        )
        
        model_button_layout.addWidget(
            self.edit_model_button
        )

        model_button_layout.addWidget(
            self.delete_model_button
        )

        model_layout.addLayout(
            model_button_layout
        )

        self.model_table = QTableWidget()

        self.model_table.setColumnCount(
            5
        )

        self.model_table.setHorizontalHeaderLabels([
            "Model",
            "Voltage Lower",
            "Voltage Upper",
            "Current Lower",
            "Current Upper"
        ])

        self.model_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        model_layout.addWidget(
            self.model_table
        )

        model_group.setLayout(
            model_layout
        )

        main_layout.addWidget(
            model_group
        )

        self.model_table.itemSelectionChanged.connect(
            self.load_selected_model
        )

    # =========================
    # OPERATOR
    # =========================

    def load_operators(self):
        operators = self.operator_repository.get_all_operators()

        self.operator_table.setRowCount(0)

        for operator in operators:
            row = self.operator_table.rowCount()
            self.operator_table.insertRow(row)

            self.operator_table.setItem(
                row, 0, QTableWidgetItem(str(operator[1]))
            )
            self.operator_table.setItem(
                row, 1, QTableWidgetItem(str(operator[2]))
            )
                        
    def add_operator(self):
        operator_id = self.operator_id_input.text().strip()
        name = self.operator_name_input.text().strip()

        # =========================
        # VALIDASI OPERATOR ID
        # =========================

        if not operator_id:
            QMessageBox.warning(
                self,
                "Invalid Operator",
                "Operator ID tidak boleh kosong."
            )
            self.operator_id_input.setFocus()
            return

        if " " in operator_id:
            QMessageBox.warning(
                self,
                "Invalid Operator",
                "Operator ID tidak boleh mengandung spasi."
            )
            self.operator_id_input.setFocus()
            return

        if len(operator_id) < 3:
            QMessageBox.warning(
                self,
                "Invalid Operator",
                "Operator ID minimal 3 karakter."
            )
            self.operator_id_input.setFocus()
            return

        # =========================
        # VALIDASI NAME
        # =========================

        if not name:
            QMessageBox.warning(
                self,
                "Invalid Operator",
                "Name tidak boleh kosong."
            )
            self.operator_name_input.setFocus()
            return

        if len(name) < 2:
            QMessageBox.warning(
                self,
                "Invalid Operator",
                "Name minimal 2 karakter."
            )
            self.operator_name_input.setFocus()
            return

        # =========================
        # CEK DUPLIKAT
        # =========================

        if self.operator_repository.is_valid_operator(operator_id):
            QMessageBox.warning(
                self,
                "Duplicate Operator",
                f"Operator ID '{operator_id}' sudah terdaftar."
            )
            self.operator_id_input.setFocus()
            return

        # =========================
        # SIMPAN
        # =========================

        self.operator_repository.add_operator(
            operator_id,
            name
        )

        QMessageBox.information(
            self,
            "Success",
            f"Operator '{operator_id}' berhasil ditambahkan."
        )

        self.load_operators()

        self.operator_id_input.clear()
        self.operator_name_input.clear()

        self.operator_id_input.setFocus()

    def load_selected_operator(self):
        row = self.operator_table.currentRow()

        if row < 0:
            return

        operator_id = self.operator_table.item(row, 0).text()
        name = self.operator_table.item(row, 1).text()

        self.operator_id_input.setText(operator_id)
        self.operator_name_input.setText(name)
        
    def delete_operator(self):
        row = self.operator_table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Delete Operator",
                "Pilih operator yang ingin dihapus."
            )
            return

        operator_id = self.operator_table.item(row, 0).text()

        confirm = QMessageBox.question(
            self,
            "Delete Operator",
            f"Apakah Anda yakin ingin menghapus operator '{operator_id}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.operator_repository.delete_operator(operator_id)
            self.load_operators()
            self.operator_id_input.clear()
            self.operator_name_input.clear()
            self.operator_id_input.setFocus()
            
    # =========================
    # MODEL
    # =========================

    def load_models(self):
        models = self.model_repository.get_all_models()

        self.model_table.setRowCount(0)

        for model in models:
            row = self.model_table.rowCount()
            self.model_table.insertRow(row)

            self.model_table.setItem(
                row, 0, QTableWidgetItem(str(model[1]))
            )
            self.model_table.setItem(
                row, 1, QTableWidgetItem(str(model[2]))
            )
            self.model_table.setItem(
                row, 2, QTableWidgetItem(str(model[3]))
            )
            self.model_table.setItem(
                row, 3, QTableWidgetItem(str(model[4]))
            )
            self.model_table.setItem(
                row, 4, QTableWidgetItem(str(model[5]))
            )
            
    def add_model(self):
        model_name = self.model_name_input.text().strip()

        voltage_lower_text = self.voltage_lower_input.text().strip()
        voltage_upper_text = self.voltage_upper_input.text().strip()
        current_lower_text = self.current_lower_input.text().strip()
        current_upper_text = self.current_upper_input.text().strip()

        # =========================
        # MODEL NAME
        # =========================

        if not model_name:
            QMessageBox.warning(
                self,
                "Invalid Model",
                "Model Name tidak boleh kosong."
            )
            self.model_name_input.setFocus()
            return

        # =========================
        # CEK INPUT KOSONG
        # =========================

        if not voltage_lower_text:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Voltage Lower tidak boleh kosong."
            )
            self.voltage_lower_input.setFocus()
            return

        if not voltage_upper_text:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Voltage Upper tidak boleh kosong."
            )
            self.voltage_upper_input.setFocus()
            return

        if not current_lower_text:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Current Lower tidak boleh kosong."
            )
            self.current_lower_input.setFocus()
            return

        if not current_upper_text:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Current Upper tidak boleh kosong."
            )
            self.current_upper_input.setFocus()
            return

        # =========================
        # KONVERSI KE FLOAT
        # =========================

        try:
            voltage_lower = float(voltage_lower_text)
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Voltage Lower harus berupa angka."
            )
            self.voltage_lower_input.setFocus()
            return

        try:
            voltage_upper = float(voltage_upper_text)
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Voltage Upper harus berupa angka."
            )
            self.voltage_upper_input.setFocus()
            return

        try:
            current_lower = float(current_lower_text)
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Current Lower harus berupa angka."
            )
            self.current_lower_input.setFocus()
            return

        try:
            current_upper = float(current_upper_text)
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Current Upper harus berupa angka."
            )
            self.current_upper_input.setFocus()
            return

        # =========================
        # VALIDASI RANGE
        # =========================

        if voltage_lower >= voltage_upper:
            QMessageBox.warning(
                self,
                "Invalid Voltage Range",
                "Voltage Lower harus lebih kecil dari Voltage Upper."
            )
            self.voltage_lower_input.setFocus()
            return

        if current_lower >= current_upper:
            QMessageBox.warning(
                self,
                "Invalid Current Range",
                "Current Lower harus lebih kecil dari Current Upper."
            )
            self.current_lower_input.setFocus()
            return

        # =========================
        # CEK DUPLIKAT MODEL
        # =========================

        if self.model_repository.get_model(model_name):
            QMessageBox.warning(
                self,
                "Duplicate Model",
                f"Model '{model_name}' sudah terdaftar."
            )
            self.model_name_input.setFocus()
            return

        # =========================
        # SIMPAN
        # =========================

        self.model_repository.add_model(
            model_name,
            voltage_lower,
            voltage_upper,
            current_lower,
            current_upper
        )

        QMessageBox.information(
            self,
            "Success",
            f"Model '{model_name}' berhasil ditambahkan."
        )

        self.load_models()

        self.model_name_input.clear()
        self.voltage_lower_input.clear()
        self.voltage_upper_input.clear()
        self.current_lower_input.clear()
        self.current_upper_input.clear()

        self.model_name_input.setFocus()

    def edit_model(self):

        row = self.model_table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Edit Model",
                "Pilih model yang ingin diedit."
            )
            return

        model_name = self.model_name_input.text().strip()

        voltage_lower_text = (
            self.voltage_lower_input.text().strip()
        )

        voltage_upper_text = (
            self.voltage_upper_input.text().strip()
        )

        current_lower_text = (
            self.current_lower_input.text().strip()
        )

        current_upper_text = (
            self.current_upper_input.text().strip()
        )

        if not model_name:
            QMessageBox.warning(
                self,
                "Invalid Model",
                "Model Name tidak boleh kosong."
            )
            self.model_name_input.setFocus()
            return

        if not voltage_lower_text:
            QMessageBox.warning(
                self,
                "Invalid Model",
                "Voltage Lower tidak boleh kosong."
            )
            self.voltage_lower_input.setFocus()
            return

        if not voltage_upper_text:
            QMessageBox.warning(
                self,
                "Invalid Model",
                "Voltage Upper tidak boleh kosong."
            )
            self.voltage_upper_input.setFocus()
            return

        if not current_lower_text:
            QMessageBox.warning(
                self,
                "Invalid Model",
                "Current Lower tidak boleh kosong."
            )
            self.current_lower_input.setFocus()
            return

        if not current_upper_text:
            QMessageBox.warning(
                self,
                "Invalid Model",
                "Current Upper tidak boleh kosong."
            )
            self.current_upper_input.setFocus()
            return

        try:
            voltage_lower = float(
                voltage_lower_text
            )

            voltage_upper = float(
                voltage_upper_text
            )

            current_lower = float(
                current_lower_text
            )

            current_upper = float(
                current_upper_text
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "Invalid Model",
                "Nilai voltage dan current harus berupa angka."
            )
            return

        if voltage_lower >= voltage_upper:

            QMessageBox.warning(
                self,
                "Invalid Voltage",
                "Voltage Lower harus lebih kecil dari Voltage Upper."
            )
            self.voltage_lower_input.setFocus()
            return

        if current_lower >= current_upper:

            QMessageBox.warning(
                self,
                "Invalid Current",
                "Current Lower harus lebih kecil dari Current Upper."
            )
            self.current_lower_input.setFocus()
            return

        confirm = QMessageBox.question(
            self,
            "Edit Model",
            f"Update model '{model_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        updated = self.model_repository.update_model(
            model_name,
            voltage_lower,
            voltage_upper,
            current_lower,
            current_upper
        )

        if not updated:

            QMessageBox.warning(
                self,
                "Edit Model",
                f"Model '{model_name}' tidak ditemukan."
            )
            return

        QMessageBox.information(
            self,
            "Success",
            f"Model '{model_name}' berhasil diperbarui."
        )

        self.load_models()

        self.model_table.clearSelection()

        self.model_name_input.clear()
        self.voltage_lower_input.clear()
        self.voltage_upper_input.clear()
        self.current_lower_input.clear()
        self.current_upper_input.clear()

        self.model_name_input.setFocus()

    def load_selected_model(self):

        row = self.model_table.currentRow()

        if row < 0:
            return

        model_name = self.model_table.item(row, 0).text()
        voltage_lower = self.model_table.item(row, 1).text()
        voltage_upper = self.model_table.item(row, 2).text()
        current_lower = self.model_table.item(row, 3).text()
        current_upper = self.model_table.item(row, 4).text()

        self.model_name_input.setText(model_name)
        self.voltage_lower_input.setText(voltage_lower)
        self.voltage_upper_input.setText(voltage_upper)
        self.current_lower_input.setText(current_lower)
        self.current_upper_input.setText(current_upper)

    def delete_model(self):
        row = self.model_table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Delete Model",
                "Pilih model yang ingin dihapus."
            )
            return

        model_name = self.model_table.item(row, 0).text()

        confirm = QMessageBox.question(
            self,
            "Delete Model",
            f"Apakah Anda yakin ingin menghapus model '{model_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.model_repository.delete_model(model_name)
            self.load_models()
            self.model_name_input.clear()
            self.voltage_lower_input.clear()
            self.voltage_upper_input.clear()
            self.current_lower_input.clear()
            self.current_upper_input.clear()

            self.model_name_input.setFocus()