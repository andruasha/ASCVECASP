import sys
import os
import subprocess
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QSpinBox
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QFormLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QMessageBox
from src.active_dipole.main import generate_active_dipole_schemes_set
from src.coupling_coefficient.main import generate_coupling_coefficient_schemes_set
from src.direct_current.main import generate_direct_current_schemes_set
from src.alternating_current.main import generate_alternating_current_schemes_set
from src.transient_processes.main import generate_transient_processes_schemes_set
from src.active_quadripole.main import generate_active_quadripole_schemes_set
from src.filter.main import generate_filter_schemes_set


def open_folder(path):
    if sys.platform == "win32":
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])


def at_least_one_reactive(widgets):
    cond = widgets["capacitors"].value() + widgets["inductors"].value() > 0
    return cond, "Добавьте хотя бы один конденсатор или индуктивность"


def current_sources_no_more_than_nodes_minus_one(widgets):
    cond = widgets["current_sources"].value() <= int(widgets["nodes"].currentText()) - 1
    return cond, "Число источников тока не должно превышать (узлы - 1)"


def total_elements_at_least_branches(widgets):
    try:
        branches = int(widgets["branches"].currentText())
    except Exception:
        return True, ""

    total = sum([
        widgets.get(key).value() for key in [
            "voltage_sources", "current_sources", "resistors", "capacitors", "inductors"
        ] if key in widgets
    ])
    cond = total >= branches
    return cond, f"Сумма всех элементов должна быть не меньше числа ветвей ({branches})"


def total_elements_not_exceed_branches_times_8(widgets):
    try:
        branches = int(widgets["branches"].currentText())
    except Exception:
        return True, ""

    total = sum([
        widgets.get(key).value() for key in [
            "voltage_sources", "current_sources", "resistors", "capacitors", "inductors"
        ] if key in widgets
    ])
    cond = total <= branches * 8
    return cond, f"Сумма всех элементов не должна превышать {branches * 8}"


validators = {
    "active_dipole": [
        total_elements_at_least_branches,
        total_elements_not_exceed_branches_times_8,
        current_sources_no_more_than_nodes_minus_one
    ],
    "coupling_coefficient": [
        total_elements_at_least_branches,
        total_elements_not_exceed_branches_times_8,
        current_sources_no_more_than_nodes_minus_one
    ],
    "direct_current": [
        total_elements_at_least_branches,
        total_elements_not_exceed_branches_times_8,
        current_sources_no_more_than_nodes_minus_one
    ],
    "alternating_current": [
        total_elements_at_least_branches,
        total_elements_not_exceed_branches_times_8,
        current_sources_no_more_than_nodes_minus_one
    ],
    "transient_processes": [
        total_elements_at_least_branches,
        total_elements_not_exceed_branches_times_8,
        current_sources_no_more_than_nodes_minus_one,
        at_least_one_reactive
    ]
}

element_mappings = {
    "active_dipole": ["nodes", "branches", "voltage_sources", "current_sources", "resistors"],
    "coupling_coefficient": ["nodes", "branches", "voltage_sources", "current_sources", "resistors"],
    "direct_current": ["nodes", "branches", "voltage_sources", "current_sources", "resistors"],
    "alternating_current": ["nodes", "branches", "voltage_sources", "current_sources", "resistors", "capacitors", "inductors"],
    "transient_processes": ["nodes", "branches", "voltage_sources", "current_sources", "resistors", "capacitors", "inductors"],
    "active_quadripole": ["scheme_type", "resistors", "capacitors", "inductors"],
    "filter": ["filter_type", "scheme_type"]
}

theme_display_mapping = {
    "Нахождение параметров схемы замещения активного двухполюсника": "active_dipole",
    "Нахождение коэффициентов связи": "coupling_coefficient",
    "Нахождение токов и напряжений в схемах постоянного тока": "direct_current",
    "Нахождение токов и напряжений в схемах переменного тока": "alternating_current",
    "Нахождение формы тока или напряжения при переходном процессе": "transient_processes",
    "Нахождение параметров четырёхполюсника": "active_quadripole",
    "Расчёт параметров пассивных электрических фильтров": "filter"
}

theme_reverse_mapping = {v: k for k, v in theme_display_mapping.items()}

active_quadripole_schemes = ["G", "P", "T", "T_bridge", "T_back_coupling"]

filter_to_schemes = {
    "LPF": ["G", "P", "T"],
    "HPF": ["G", "P", "T"],
    "BPF": ["G", "P", "T"],
    "BSF": ["G", "T_back_coupling"]
}


class SchemeGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_folder = None
        self.submit_btn = None
        self.folder_btn = None
        self.folder_label = None
        self.scheme_type_combo = None
        self.filter_type_combo = None
        self.widgets = None
        self.form = None
        self.theme_combo = None
        self.setWindowTitle("ASCVECASP")
        self.setMinimumSize(400, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.form = QFormLayout()
        layout.addLayout(self.form)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(theme_display_mapping.keys())
        self.theme_combo.currentTextChanged.connect(self.update_visible_elements)
        self.form.addRow("Тема:", self.theme_combo)
        self.widgets = {}

        nodes_combo = QComboBox()
        nodes_combo.addItems([str(i) for i in range(2, 5)])
        nodes_combo.currentTextChanged.connect(self.validate_inputs)
        nodes_combo.currentTextChanged.connect(self.update_branches_range)
        self.form.addRow("Узлы:", nodes_combo)
        self.widgets["nodes"] = nodes_combo

        branches_combo = QComboBox()
        self.form.addRow("Ветви:", branches_combo)
        self.widgets["branches"] = branches_combo

        def add_spin(label, key):
            widget = QSpinBox()
            widget.setRange(0, 100)
            widget.valueChanged.connect(self.validate_inputs)
            self.form.addRow(label, widget)
            self.widgets[key] = widget

        add_spin("Источники напряжения:", "voltage_sources")
        add_spin("Источники тока:", "current_sources")
        add_spin("Резисторы:", "resistors")
        add_spin("Конденсаторы:", "capacitors")
        add_spin("Индуктивности:", "inductors")

        self.filter_type_combo = QComboBox()
        self.filter_type_combo.addItems(filter_to_schemes.keys())
        self.filter_type_combo.currentTextChanged.connect(self.update_scheme_options)
        self.filter_type_combo.currentTextChanged.connect(self.validate_inputs)
        self.widgets["filter_type"] = self.filter_type_combo
        self.form.addRow("Тип фильтра:", self.filter_type_combo)

        self.scheme_type_combo = QComboBox()
        self.scheme_type_combo.currentTextChanged.connect(self.validate_inputs)
        self.widgets["scheme_type"] = self.scheme_type_combo
        self.form.addRow("Тип схемы:", self.scheme_type_combo)

        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("Папка не выбрана")
        self.folder_btn = QPushButton("Выбрать папку")
        self.folder_btn.clicked.connect(self.choose_folder)
        folder_layout.addWidget(self.folder_btn)
        folder_layout.addWidget(self.folder_label)
        layout.addLayout(folder_layout)

        self.submit_btn = QPushButton("Создать")
        self.submit_btn.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)
        self.selected_folder = ""
        self.update_visible_elements()

    def update_branches_range(self):
        nodes = int(self.widgets["nodes"].currentText())
        branches_combo = self.widgets["branches"]
        branches_combo.clear()
        if nodes == 2:
            options = [3]
        elif nodes == 3:
            options = list(range(5, 10))
        elif nodes == 4:
            options = list(range(6, 13))
        branches_combo.addItems([str(x) for x in options])
        self.validate_inputs()

    def update_visible_elements(self):
        theme_display = self.theme_combo.currentText()
        theme = theme_display_mapping[theme_display]
        visible = set(element_mappings.get(theme, []))
        for key, widget in self.widgets.items():
            row = self.form.labelForField(widget)
            should_show = key in visible
            widget.setVisible(should_show)
            row.setVisible(should_show)
        if "scheme_type" in visible and "filter_type" in visible:
            self.update_scheme_options()
        elif theme == "active_quadripole" and "scheme_type" in visible:
            self.scheme_type_combo.clear()
            self.scheme_type_combo.addItems(active_quadripole_schemes)
        self.update_branches_range()
        self.validate_inputs()

    def update_scheme_options(self):
        filter_type = self.filter_type_combo.currentText()
        schemes = filter_to_schemes.get(filter_type, [])
        self.scheme_type_combo.clear()
        self.scheme_type_combo.addItems(schemes)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        if folder:
            self.selected_folder = folder
            self.folder_label.setText(folder)
            self.validate_inputs()

    def validate_inputs(self):
        theme_display = self.theme_combo.currentText()
        theme = theme_display_mapping.get(theme_display)
        validators_list = validators.get(theme, [])

        for validator in validators_list:
            is_valid, message = validator(self.widgets)
            if not is_valid:
                self.submit_btn.setEnabled(False)
                self.submit_btn.setToolTip(message)
                return

        if not self.selected_folder:
            self.submit_btn.setEnabled(False)
            self.submit_btn.setToolTip("Выберите папку для сохранения")
            return

        self.submit_btn.setEnabled(True)
        self.submit_btn.setToolTip("")

    def submit_data(self):
        self.setEnabled(False)
        self.submit_btn.setText("Генерация...")
        QApplication.processEvents()

        try:
            status = {}
            theme_display = self.theme_combo.currentText()
            theme = theme_display_mapping[theme_display]

            def get_value(key):
                if key in self.widgets:
                    widget = self.widgets[key]
                    if isinstance(widget, QSpinBox):
                        return widget.value()
                    elif isinstance(widget, QComboBox):
                        text = widget.currentText()
                        return int(text) if text.isdigit() else text
                return None

            if theme == "active_dipole":
                status = generate_active_dipole_schemes_set(
                    nodes_num=get_value("nodes"),
                    branches_num=get_value("branches"),
                    voltage_sources_num=get_value("voltage_sources"),
                    current_sources_num=get_value("current_sources"),
                    resistors_num=get_value("resistors"),
                    save_path=self.selected_folder
                )

            elif theme == "coupling_coefficient":
                status = generate_coupling_coefficient_schemes_set(
                    nodes_num=get_value("nodes"),
                    branches_num=get_value("branches"),
                    voltage_sources_num=get_value("voltage_sources"),
                    current_sources_num=get_value("current_sources"),
                    resistors_num=get_value("resistors"),
                    save_path=self.selected_folder
                )

            elif theme == "direct_current":
                status = generate_direct_current_schemes_set(
                    nodes_num=get_value("nodes"),
                    branches_num=get_value("branches"),
                    voltage_sources_num=get_value("voltage_sources"),
                    current_sources_num=get_value("current_sources"),
                    resistors_num=get_value("resistors"),
                    save_path=self.selected_folder
                )

            elif theme == "alternating_current":
                status = generate_alternating_current_schemes_set(
                    nodes_num=get_value("nodes"),
                    branches_num=get_value("branches"),
                    voltage_sources_num=get_value("voltage_sources"),
                    current_sources_num=get_value("current_sources"),
                    resistors_num=get_value("resistors"),
                    capacitors_num=get_value("capacitors"),
                    inductors_num=get_value("inductors"),
                    save_path=self.selected_folder
                )

            elif theme == "transient_processes":
                status = generate_transient_processes_schemes_set(
                    nodes_num=get_value("nodes"),
                    branches_num=get_value("branches"),
                    voltage_sources_num=get_value("voltage_sources"),
                    current_sources_num=get_value("current_sources"),
                    resistors_num=get_value("resistors"),
                    capacitors_num=get_value("capacitors"),
                    inductors_num=get_value("inductors"),
                    save_path=self.selected_folder
                )

            elif theme == "active_quadripole":
                status = generate_active_quadripole_schemes_set(
                    scheme_type=get_value("scheme_type"),
                    resistors_num=get_value("resistors"),
                    capacitors_num=get_value("capacitors"),
                    inductors_num=get_value("inductors"),
                    save_path=self.selected_folder
                )

            elif theme == "filter":
                status = generate_filter_schemes_set(
                    scheme_type=get_value("scheme_type"),
                    filter_type=get_value("filter_type"),
                    save_path=self.selected_folder
                )

            if status['code'] in ["success", "warning"]:
                msg_box = QMessageBox(self)
                msg_box.setIcon(QMessageBox.Information if status['code'] == "success" else QMessageBox.Warning)
                msg_box.setWindowTitle("Успешно" if status['code'] == "success" else "Предупреждение")
                msg_box.setText(status['message'])
                open_btn = msg_box.addButton("Открыть папку", QMessageBox.ActionRole)
                ok_btn = msg_box.addButton(QMessageBox.Ok)
                msg_box.exec()
                if msg_box.clickedButton() == open_btn:
                    open_folder(self.selected_folder)
            elif status['code'] == "error":
                QMessageBox.critical(self, "Ошибка", status['message'])

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f'Возникла непредвиденная ошибка: {str(e)}')
            print(f'Ошибка: {str(e)}')

        finally:
            self.setEnabled(True)
            self.submit_btn.setText("Создать")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchemeGenerator()
    window.show()
    sys.exit(app.exec())
