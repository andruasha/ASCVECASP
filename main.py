from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QSpinBox,
    QPushButton, QFileDialog, QVBoxLayout, QFormLayout, QHBoxLayout, QMessageBox
)
import sys

from src.active_dipole.main import generate_active_dipole_schemes_set
from src.coupling_coefficient.main import generate_coupling_coefficient_schemes_set
from src.direct_current.main import generate_direct_current_schemes_set
from src.alternating_current.main import generate_alternating_current_schemes_set
from src.transient_processes.main import generate_transient_processes_schemes_set
from src.active_quadripole.main import generate_active_quadripole_schemes_set
from src.filter.main import generate_filter_schemes_set


element_mappings = {
    "active_dipole": ["nodes", "branches", "voltage_sources", "current_sources", "resistors"],
    "coupling_coefficient": ["nodes", "branches", "voltage_sources", "current_sources", "resistors"],
    "direct_current": ["nodes", "branches", "voltage_sources", "current_sources", "resistors"],
    "alternating_current": ["nodes", "branches", "voltage_sources", "current_sources", "resistors", "capacitors", "inductors"],
    "transient_processes": ["nodes", "branches", "voltage_sources", "current_sources", "resistors", "capacitors", "inductors"],
    "active_quadripole": ["scheme_type", "resistors", "capacitors", "inductors"],
    "filter": ["filter_type", "scheme_type"]
}

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
        self.theme_combo.addItems(element_mappings.keys())
        self.theme_combo.currentTextChanged.connect(self.update_visible_elements)
        self.form.addRow("Тема:", self.theme_combo)

        self.widgets = {}

        def add_spin(label, key):
            widget = QSpinBox()
            widget.setRange(0, 100)
            self.form.addRow(label, widget)
            self.widgets[key] = widget

        add_spin("Узлы:", "nodes")
        add_spin("Ветви:", "branches")
        add_spin("Источники напряжения:", "voltage_sources")
        add_spin("Источники тока:", "current_sources")
        add_spin("Резисторы:", "resistors")
        add_spin("Конденсаторы:", "capacitors")
        add_spin("Индуктивности:", "inductors")

        self.filter_type_combo = QComboBox()
        self.filter_type_combo.addItems(filter_to_schemes.keys())
        self.filter_type_combo.currentTextChanged.connect(self.update_scheme_options)
        self.widgets["filter_type"] = self.filter_type_combo
        self.form.addRow("Тип фильтра:", self.filter_type_combo)

        self.scheme_type_combo = QComboBox()
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

    def update_visible_elements(self):
        theme = self.theme_combo.currentText()
        visible = set(element_mappings.get(theme, []))

        for key, widget in self.widgets.items():
            row = self.form.labelForField(widget)
            should_show = key in visible
            widget.setVisible(should_show)
            row.setVisible(should_show)

        if "scheme_type" in visible and "filter_type" in visible:
            self.update_scheme_options()

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

    def submit_data(self):
        theme = self.theme_combo.currentText()

        def get_value(key):
            if key in self.widgets:
                widget = self.widgets[key]
                if isinstance(widget, QSpinBox):
                    return widget.value()
                elif isinstance(widget, QComboBox):
                    return widget.currentText()
            return None

        print(self.selected_folder)

        if theme == "active_dipole":
            generate_active_dipole_schemes_set(
                nodes_num=get_value("nodes"),
                branches_num=get_value("branches"),
                voltage_sources_num=get_value("voltage_sources"),
                current_sources_num=get_value("current_sources"),
                resistors_num=get_value("resistors")
            )

        elif theme == "coupling_coefficient":
            generate_coupling_coefficient_schemes_set(
                nodes_num=get_value("nodes"),
                branches_num=get_value("branches"),
                voltage_sources_num=get_value("voltage_sources"),
                current_sources_num=get_value("current_sources"),
                resistors_num=get_value("resistors")
            )

        elif theme == "direct_current":
            generate_direct_current_schemes_set(
                nodes_num=get_value("nodes"),
                branches_num=get_value("branches"),
                voltage_sources_num=get_value("voltage_sources"),
                current_sources_num=get_value("current_sources"),
                resistors_num=get_value("resistors")
            )

        elif theme == "alternating_current":
            generate_alternating_current_schemes_set(
                nodes_num=get_value("nodes"),
                branches_num=get_value("branches"),
                voltage_sources_num=get_value("voltage_sources"),
                current_sources_num=get_value("current_sources"),
                resistors_num=get_value("resistors"),
                capacitors_num=get_value("capacitors"),
                inductors_num=get_value("inductors")
            )

        elif theme == "transient_processes":
            generate_transient_processes_schemes_set(
                nodes_num=get_value("nodes"),
                branches_num=get_value("branches"),
                voltage_sources_num=get_value("voltage_sources"),
                current_sources_num=get_value("current_sources"),
                resistors_num=get_value("resistors"),
                capacitors_num=get_value("capacitors"),
                inductors_num=get_value("inductors")
            )

        elif theme == "active_quadripole":
            generate_active_quadripole_schemes_set(
                scheme_type=get_value("scheme_type"),
                resistors_num=get_value("resistors"),
                capacitors_num=get_value("capacitors"),
                inductors_num=get_value("inductors")
            )

        elif theme == "filter":
            generate_filter_schemes_set(
                scheme_type=get_value("scheme_type"),
                filter_type=get_value("filter_type")
            )

        QMessageBox.information(self, "Готово", "Схемы успешно сгенерированы (заглушка).")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchemeGenerator()
    window.show()
    sys.exit(app.exec())
