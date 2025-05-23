import sys
import os
import subprocess
import traceback
from PySide6.QtCore import Qt
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
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QGroupBox
from PySide6.QtWidgets import QGridLayout
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

filter_type_display_mapping = {
    "Фильтр нижних частот": "LPF",
    "Фильтр верхних частот": "HPF",
    "Полосовой фильтр": "BPF",
    "Режекторный фильтр": "BSF"
}
filter_type_reverse_mapping = {v: k for k, v in filter_type_display_mapping.items()}

active_quadripole_scheme_display_mapping = {
    "G": "Г-образная",
    "P": "П-образная",
    "T": "Т-образная",
    "T_bridge": "Т-образная мостовая",
    "T_back_coupling": "Т-образная с обратной связью"
}
active_quadripole_scheme_reverse_mapping = {v: k for k, v in active_quadripole_scheme_display_mapping.items()}

scheme_type_display_mapping = {
    "G": "Г-образная",
    "P": "П-образная",
    "T": "Т-образная",
    "T_bridge": "Т-образная мостовая",
    "T_back_coupling": "Т-образная с обратной связью"
}
scheme_type_reverse_mapping = {v: k for k, v in scheme_type_display_mapping.items()}

generation_mode_mapping = {
    "Генерировать номиналы элементов": "generate_values",
    "Генерировать граничные частоты": "generate_frequencies"
}


class SchemeGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_folder = None
        self.submit_btn = None
        self.folder_btn = None
        self.folder_label = None
        self.widgets = {}
        self.form = None
        self.theme_combo = None
        self.folder_name_input = None
        self.filter_generation_mode = None
        self.error_label = None
        self.filter_type_checkboxes = {}
        self.scheme_type_checkboxes = {}
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

        self.filter_group = QGroupBox("Тип фильтра:")
        filter_layout = QGridLayout()
        for i, (name, code) in enumerate(filter_type_display_mapping.items()):
            cb = QCheckBox(name)
            cb.stateChanged.connect(self.update_scheme_checkboxes)
            cb.stateChanged.connect(self.validate_inputs)
            filter_layout.addWidget(cb, i, 0)
            self.filter_type_checkboxes[code] = cb
        self.filter_group.setLayout(filter_layout)
        self.widgets["filter_type"] = self.filter_group
        self.form.addRow(self.filter_group)

        self.scheme_group = QGroupBox("Тип схемы:")
        scheme_layout = QGridLayout()
        for i, (code, name) in enumerate(scheme_type_display_mapping.items()):
            cb = QCheckBox(name)
            cb.stateChanged.connect(self.validate_inputs)
            cb.stateChanged.connect(self.handle_scheme_checkbox_change)
            scheme_layout.addWidget(cb, i, 0)
            self.scheme_type_checkboxes[code] = cb
        self.scheme_group.setLayout(scheme_layout)
        self.widgets["scheme_type"] = self.scheme_group
        self.form.addRow(self.scheme_group)

        self.filter_generation_mode = QComboBox()
        self.filter_generation_mode.addItems([
            "Генерировать номиналы элементов",
            "Генерировать граничные частоты"
        ])
        self.filter_generation_mode.currentTextChanged.connect(self.validate_inputs)
        self.form.addRow("Тип генерации:", self.filter_generation_mode)
        self.widgets["filter_generation_mode"] = self.filter_generation_mode

        self.folder_label = QLabel("Папка не выбрана")
        self.folder_btn = QPushButton("Выбрать папку")
        self.folder_btn.clicked.connect(self.choose_folder)
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_btn)
        folder_layout.addWidget(self.folder_label)
        folder_container = QWidget()
        folder_container.setLayout(folder_layout)
        self.form.addRow("Папка:", folder_container)

        self.folder_name_input = QLineEdit()
        self.folder_name_input.textChanged.connect(self.validate_inputs)
        self.form.addRow("Название папки:", self.folder_name_input)

        self.submit_btn = QPushButton("Создать")
        self.submit_btn.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_btn)

        self.error_label = QLabel()
        self.error_label.setStyleSheet(
            '''
            color: red;
            background - color: transparent;
            padding: 4
            px;
            font - size: 12
            px;
            '''
        )
        self.error_label.setWordWrap(True)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setMaximumHeight(30)
        self.error_label.setVisible(False)
        layout.addWidget(self.error_label)

        self.setLayout(layout)
        self.selected_folder = ""
        self.update_visible_elements()

    def handle_scheme_checkbox_change(self):
        theme_display = self.theme_combo.currentText()
        theme = theme_display_mapping.get(theme_display)

        if theme == "active_quadripole":
            sender = self.sender()
            if sender.isChecked():
                for cb in self.scheme_type_checkboxes.values():
                    if cb != sender:
                        cb.setChecked(False)

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
            row = self.form.labelForField(widget) or widget
            should_show = key in visible
            widget.setVisible(should_show)
            if hasattr(row, 'setVisible'):
                row.setVisible(should_show)

        if theme == "filter":
            self.update_scheme_checkboxes()
        elif theme == "active_quadripole":
            for code, cb in self.scheme_type_checkboxes.items():
                cb.setEnabled(code in active_quadripole_schemes)
                cb.setChecked(False)

        self.widgets["filter_generation_mode"].setVisible(theme == "filter")
        row = self.form.labelForField(self.widgets["filter_generation_mode"])
        if row:
            row.setVisible(theme == "filter")

        self.update_branches_range()
        self.validate_inputs()

    def update_scheme_checkboxes(self):
        selected_filters = [ftype for ftype, cb in self.filter_type_checkboxes.items() if cb.isChecked()]
        allowed_schemes = set()
        for f in selected_filters:
            allowed_schemes.update(filter_to_schemes.get(f, []))

        for scheme_code, cb in self.scheme_type_checkboxes.items():
            cb.setEnabled(scheme_code in allowed_schemes)
            cb.setChecked(cb.isChecked() and scheme_code in allowed_schemes)

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
                self.show_error(message)
                self.submit_btn.setEnabled(False)
                return

        if not self.selected_folder:
            self.show_error("Выберите путь для сохранения")
            self.submit_btn.setEnabled(False)
            return

        if not self.folder_name_input.text().strip():
            self.show_error("Введите название папки")
            self.submit_btn.setEnabled(False)
            return

        if theme == "filter":
            selected_filters = [ftype for ftype, cb in self.filter_type_checkboxes.items() if cb.isChecked()]
            if not selected_filters:
                self.show_error("Выберите хотя бы один тип фильтра")
                self.submit_btn.setEnabled(False)
                return

            allowed_schemes = set()
            for f in selected_filters:
                allowed_schemes.update(filter_to_schemes.get(f, []))

            schemes_selected = any(
                cb.isChecked() for code, cb in self.scheme_type_checkboxes.items() if code in allowed_schemes
            )

            if not schemes_selected:
                self.show_error("Выберите хотя бы один доступный тип схемы")
                self.submit_btn.setEnabled(False)
                return

        self.submit_btn.setEnabled(True)
        self.submit_btn.setToolTip("")
        self.error_label.setVisible(False)

    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.setVisible(True)

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

            save_path = os.path.join(self.selected_folder, self.folder_name_input.text().strip())

            if theme == "filter":
                selected_filters = [ftype for ftype, cb in self.filter_type_checkboxes.items() if cb.isChecked()]
                selected_schemes = [stype for stype, cb in self.scheme_type_checkboxes.items() if cb.isChecked()]
                generation_mode_text = self.filter_generation_mode.currentText()
                generation_mode_code = generation_mode_mapping.get(generation_mode_text)
                status = generate_filter_schemes_set(
                    scheme_types=selected_schemes,
                    filter_types=selected_filters,
                    save_path=save_path,
                    generation_mode=generation_mode_code
                )

            elif theme == "active_quadripole":
                selected_scheme = next((k for k, cb in self.scheme_type_checkboxes.items() if cb.isChecked()), None)
                status = generate_active_quadripole_schemes_set(
                    scheme_type=selected_scheme,
                    resistors_num=get_value("resistors"),
                    capacitors_num=get_value("capacitors"),
                    inductors_num=get_value("inductors"),
                    save_path=save_path
                )

            else:
                params = {
                    "nodes_num": get_value("nodes"),
                    "branches_num": get_value("branches"),
                    "voltage_sources_num": get_value("voltage_sources"),
                    "current_sources_num": get_value("current_sources"),
                    "resistors_num": get_value("resistors"),
                    "save_path": save_path
                }

                if theme in ["alternating_current", "transient_processes"]:
                    params["capacitors_num"] = get_value("capacitors")
                    params["inductors_num"] = get_value("inductors")

                generators = {
                    "active_dipole": generate_active_dipole_schemes_set,
                    "coupling_coefficient": generate_coupling_coefficient_schemes_set,
                    "direct_current": generate_direct_current_schemes_set,
                    "alternating_current": generate_alternating_current_schemes_set,
                    "transient_processes": generate_transient_processes_schemes_set
                }

                status = generators[theme](**params)

            if status['code'] in ["success", "warning"]:
                msg_box = QMessageBox(self)
                msg_box.setIcon(QMessageBox.Information if status['code'] == "success" else QMessageBox.Warning)
                msg_box.setWindowTitle("Успешно" if status['code'] == "success" else "Предупреждение")
                msg_box.setText(status['message'])
                open_btn = msg_box.addButton("Открыть папку", QMessageBox.ActionRole)
                msg_box.addButton(QMessageBox.Ok)
                msg_box.exec()
                if msg_box.clickedButton() == open_btn:
                    open_folder(save_path)
            elif status['code'] == "error":
                QMessageBox.critical(self, "Ошибка", status['message'])

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f'Возникла непредвиденная ошибка: {str(e)}')
            traceback.print_exc()
        finally:
            self.setEnabled(True)
            self.submit_btn.setText("Создать")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchemeGenerator()
    window.show()
    sys.exit(app.exec())
