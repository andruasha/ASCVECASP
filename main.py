from src.active_dipole.main import generate_active_dipole_schemes_set
from src.coupling_coefficient.main import generate_coupling_coefficient_schemes_set


# generate_active_dipole_schemes_set(
#     nodes_num=4,
#     branches_num=6,
#     voltage_sources_num=1,
#     current_sources_num=1,
#     resistors_num=6
# )

generate_coupling_coefficient_schemes_set(
    nodes_num=4,
    branches_num=6,
    voltage_sources_num=1,
    current_sources_num=1,
    resistors_num=6
)
