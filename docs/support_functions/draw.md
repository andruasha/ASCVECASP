# Документация модуля для рисования электронных компонентов

Этот модуль предоставляет функции для отрисовки различных электронных компонентов с использованием matplotlib. Все компоненты рисуются в масштабе, заданном константой `SCALE` из конфигурации.

## Общие параметры

Все функции рисования используют общие параметры:

- `center`: Словарь с ключами 'x' и 'y' для указания координат центра
- `name`: Текстовая метка компонента
- `orientation`: Один из вариантов:
  - 'horizontal' (горизонтальный)
  - 'vertical' (вертикальный)
  - 'diagonal' (диагональный 45°)
  - '-diagonal' (диагональный -45°)

Компоненты рисуются с:
- Черными контурами
- Белой заливкой
- Текстовыми метками размером 6pt
- Правильным порядком отрисовки (z-order)

## Функции рисования компонентов

### `draw_resistor`

Рисует символ резистора (прямоугольник).

```python
def draw_resistor(center, name, orientation):
    """
    Рисует резистор.
    
    Аргументы:
        center: Словарь с координатами 'x' и 'y'
        name: Текст метки резистора
        orientation: 'horizontal', 'vertical', 'diagonal' или '-diagonal'
    """
```

### `draw_capacitor`

Рисует символ конденсатора (параллельные пластины).

```python
def draw_capacitor(center, name, orientation):
    """
    Рисует конденсатор.
    
    Аргументы:
        center: Словарь с координатами 'x' и 'y'
        name: Текст метки конденсатора
        orientation: 'horizontal', 'vertical', 'diagonal' или '-diagonal'
    """
```

### `draw_inductor`

Рисует символ катушки индуктивности (3 витка).

```python
def draw_inductor(center, name, orientation):
    """
    Рисует катушку индуктивности.
    
    Аргументы:
        center: Словарь с координатами 'x' и 'y'
        name: Текст метки катушки
        orientation: 'horizontal', 'vertical', 'diagonal' или '-diagonal'
    """
```

### `draw_active_dipole`

Рисует активный диполь с метками подключения.

```python
def draw_active_dipole(center, orientation):
    """
    Рисует активный диполь с метками 'a' и 'b'.
    
    Аргументы:
        center: Словарь с координатами 'x' и 'y'
        orientation: 'horizontal' или 'vertical'
    """
```

### `draw_voltage_source`

Рисует символ источника напряжения с направленной стрелкой.

```python
def draw_voltage_source(center, name, orientation):
    """
    Рисует источник напряжения.
    
    Аргументы:
        center: Словарь с координатами 'x' и 'y'
        name: Текст метки источника
        orientation: 'horizontal' или 'vertical'
    """
```

### `draw_current_source`

Рисует символ источника тока со стрелками.

```python
def draw_current_source(center, name, orientation):
    """
    Рисует источник тока.
    
    Аргументы:
        center: Словарь с координатами 'x' и 'y'
        name: Текст метки источника
        orientation: 'horizontal' или 'vertical'
    """
```

### `draw_switch`

Рисует символ выключателя.

```python
def draw_switch(center, orientation):
    """
    Рисует выключатель.
    
    Аргументы:
        center: Словарь с координатами 'x' и 'y'
        orientation: 'horizontal' или 'vertical'
    """
```

### `draw_circle`

Рисует круговой маркер для контрольных точек.

```python
def draw_circle(center, name, color='red'):
    """
    Рисует круговой маркер.
    
    Аргументы:
        center: Словарь с координатами 'x' и 'y'
        name: Текст метки круга
        color: Цвет контура (по умолчанию 'red')
    """
```