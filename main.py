import eel

from src.active_dipole.main import generate_active_dipole_schemes_set
from src.coupling_coefficient.main import generate_coupling_coefficient_schemes_set
from src.direct_current.main import generate_direct_current_schemes_set
from src.alternating_current.main import generate_alternating_current_schemes_set
from src.transient_processes.main import generate_transient_processes_schemes_set
from src.active_quadripole.main import generate_active_quadripole_schemes_set
from src.filter.main import generate_filter_schemes_set


eel.init('gui')


@eel.expose
def generate_schemes_set(
    lab_theme,
    nodes_num,
    branches_num,
    voltage_sources,
    current_sources,
    resistors,
    capacitors,
    inductors,
    filter_type,
    scheme_type
):
    print("Тема:", lab_theme)
    print("Узлы:", nodes_num)
    print("Ветви:", branches_num)
    print("Источники напряжения:", voltage_sources)
    print("Источники тока:", current_sources)
    print("Резисторы:", resistors)
    print("Конденсаторы:", capacitors)
    print("Индуктивности:", inductors)
    print("Тип фильтра:", filter_type)
    print("Тип схемы:", scheme_type)


eel.start('index.html', size=(600, 500))


# generate_active_dipole_schemes_set(
#     nodes_num=4,
#     branches_num=6,
#     voltage_sources_num=1,
#     current_sources_num=1,
#     resistors_num=6
# )

# generate_coupling_coefficient_schemes_set(
#     nodes_num=4,
#     branches_num=6,
#     voltage_sources_num=1,
#     current_sources_num=1,
#     resistors_num=6
# )

# generate_direct_current_schemes_set(
#     nodes_num=4,
#     branches_num=6,
#     voltage_sources_num=1,
#     current_sources_num=1,
#     resistors_num=6
# )

# generate_alternating_current_schemes_set(
#     nodes_num=4,
#     branches_num=10,
#     voltage_sources_num=2,
#     current_sources_num=2,
#     resistors_num=6,
#     capacitors_num=2,
#     inductors_num=2
# )

# generate_transient_processes_schemes_set(
#     nodes_num=4,
#     branches_num=10,
#     voltage_sources_num=2,
#     current_sources_num=2,
#     resistors_num=6,
#     capacitors_num=2,
#     inductors_num=2
# )

# generate_active_quadripole_schemes_set(
#     scheme_type="G",
#     resistors_num=1,
#     capacitors_num=1,
#     inductors_num=2
# )

# generate_filter_schemes_set(
#     scheme_type='G',
#     filter_type='LPF'
# )