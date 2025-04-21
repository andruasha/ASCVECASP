from src.common.word_functions import add_schemes_to_word
from src.common.generate_schemes import generate_schemes_set


# TODO: в ворде не отображается состояние ключа (открывается или закрывается)
def generate_transient_processes_schemes_set(nodes_num, branches_num, voltage_sources_num, current_sources_num, resistors_num, inductors_num, capacitors_num, save_path):
    status = generate_schemes_set(
        nodes_num=nodes_num,
        branches_num=branches_num,
        voltage_sources_num=voltage_sources_num,
        current_sources_num=current_sources_num,
        resistors_num=resistors_num,
        capacitors_num=capacitors_num,
        inductors_num=inductors_num,
        scheme_type="transient_processes",
        save_path=save_path
    )

    if status['code'] == "error":
        return status

    add_schemes_to_word(
        scheme_type="transient_processes",
        save_path=save_path
    )

    return status
