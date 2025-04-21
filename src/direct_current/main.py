from src.common.word_functions import add_schemes_to_word
from src.common.generate_schemes import generate_schemes_set


def generate_direct_current_schemes_set(nodes_num, branches_num, voltage_sources_num, current_sources_num, resistors_num, save_path):
    status = generate_schemes_set(
        nodes_num=nodes_num,
        branches_num=branches_num,
        voltage_sources_num=voltage_sources_num,
        current_sources_num=current_sources_num,
        resistors_num=resistors_num,
        capacitors_num=0,
        inductors_num=0,
        scheme_type="direct_current",
        save_path=save_path
    )

    if status['code'] == "error":
        return status

    add_schemes_to_word(
        scheme_type="direct_current",
        save_path=save_path
    )

    return status
