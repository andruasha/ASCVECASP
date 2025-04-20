from src.common.word_functions import add_schemes_to_word
from src.common.generate_schemes import generate_schemes_set


def generate_coupling_coefficient_schemes_set(nodes_num, branches_num, voltage_sources_num, current_sources_num, resistors_num):
    status = generate_schemes_set(
        nodes_num=nodes_num,
        branches_num=branches_num,
        voltage_sources_num=voltage_sources_num,
        current_sources_num=current_sources_num,
        capacitors_num=0,
        inductors_num=0,
        resistors_num=resistors_num,
        scheme_type="coupling_coefficient"
    )

    if status['code'] == "error":
        return status

    add_schemes_to_word(
        scheme_type="coupling_coefficient"
    )

    return status
