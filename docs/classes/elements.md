# Документация к классу `ElementsPlacer`

## Описание

Класс `ElementsPlacer` предназначен для размещения электрических элементов в заданной топологии цепи с учетом специфических правил и ограничений, зависящих от типа схемы.

## Конструктор

```python
ElementsPlacer(
    circuit_topology,
    voltage_sources_num,
    current_sources_num,
    resistors_num,
    inductors_num,
    capacitors_num,
    scheme_type
)
```

### Параметры

- `circuit_topology`: объект, содержащий информацию о соединениях в электрической цепи (`nodes_connections`).
- `voltage_sources_num` (`int`): количество источников напряжения.
- `current_sources_num` (`int`): количество источников тока.
- `resistors_num` (`int`): количество резисторов.
- `inductors_num` (`int`): количество индуктивностей.
- `capacitors_num` (`int`): количество конденсаторов.
- `scheme_type` (`str`): тип схемы. Возможные значения:
  - `"active_dipole"`
  - `"transient_processes"`

## Методы

### `place_elements()`

Размещает элементы в топологии с учетом правил схемы.

#### Возвращает

- `self`, если схема успешно сгенерирована.
- `{"code": "error", "message": "..."}` — если не удалось сгенерировать корректную схему после 50000 попыток.

### `distribute_elements()`

Вспомогательный метод, который выполняет фактическое распределение элементов по соединениям.

## Логика валидации схемы

Метод `place_elements` использует вложенную функцию `is_layout_valid`, чтобы убедиться, что схема соответствует следующим условиям:

- В каждом соединении не более 8 элементов.
- При наличии источника напряжения должен быть как минимум один резистор в других соединениях.
- В схеме типа `"active_dipole"` не допускается наличие активного диполя в соединении с источником напряжения.
- Для схем типа `"transient_processes"`:
  - Конденсатор, подключённый к источнику напряжения, должен быть с резистором.
  - Связка "источник тока + индуктивность" требует наличия резистора рядом.

## Пример использования

```python
placer = ElementsPlacer(
    circuit_topology=my_topology,
    voltage_sources_num=2,
    current_sources_num=1,
    resistors_num=4,
    inductors_num=2,
    capacitors_num=3,
    scheme_type="transient_processes"
)

result = placer.place_elements()
if isinstance(result, dict) and result["code"] == "error":
    print("Ошибка генерации схемы:", result["message"])
else:
    print("Схема успешно создана")
```
