import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from conf.config import SCALE


def draw_resistor(center, name, orientation):
    width = SCALE / 10
    height = SCALE / 20

    if orientation == 'horizontal':
        lower_left = (center['x'] - width / 2, center['y'] - height / 2)
        rect = Rectangle(
            lower_left,
            width, height,
            linewidth=1.0,
            edgecolor='black',
            facecolor='white',
            zorder=10
        )
        text_x, text_y = center['x'], center['y'] - height * 1.2
        ha, va = 'center', 'top'

    elif orientation == 'vertical':
        lower_left = (center['x'] - height / 2, center['y'] - width / 2)
        rect = Rectangle(
            lower_left,
            height, width,
            linewidth=1.0,
            edgecolor='black',
            facecolor='white',
            zorder=10
        )
        text_x, text_y = center['x'] + height * 1.2, center['y']
        ha, va = 'left', 'center'

    elif orientation == 'diagonal':
        half_diag = np.sqrt(width ** 2 + height ** 2) / 2
        angle = np.arctan(height / width)
        x_offset = half_diag * np.cos(np.pi / 4 + angle)
        y_offset = half_diag * np.sin(np.pi / 4 + angle)

        points = [
            (center['x'] - x_offset, center['y'] - y_offset),
            (center['x'] - x_offset + width * np.cos(np.pi / 4), center['y'] - y_offset + width * np.sin(np.pi / 4)),
            (center['x'] - x_offset + width * np.cos(np.pi / 4) - height * np.sin(np.pi / 4),
             center['y'] - y_offset + width * np.sin(np.pi / 4) + height * np.cos(np.pi / 4)),
            (center['x'] - x_offset - height * np.sin(np.pi / 4), center['y'] - y_offset + height * np.cos(np.pi / 4))
        ]
        rect = Polygon(
            points,
            closed=True,
            linewidth=1.0,
            edgecolor='black',
            facecolor='white',
            zorder=10
        )
        text_x, text_y = center['x'] - height * 0.85, center['y'] - height * 0.85
        ha, va = 'center', 'top'

    elif orientation == '-diagonal':
        half_diag = np.sqrt(width ** 2 + height ** 2) / 2
        angle = np.arctan(height / width)
        x_offset = half_diag * np.cos(3 * np.pi / 4 + angle)
        y_offset = half_diag * np.sin(3 * np.pi / 4 + angle)

        points = [
            (center['x'] - x_offset, center['y'] - y_offset),
            (center['x'] - x_offset + width * np.cos(3 * np.pi / 4),
             center['y'] - y_offset + width * np.sin(3 * np.pi / 4)),
            (center['x'] - x_offset + width * np.cos(3 * np.pi / 4) - height * np.sin(3 * np.pi / 4),
             center['y'] - y_offset + width * np.sin(3 * np.pi / 4) + height * np.cos(3 * np.pi / 4)),
            (center['x'] - x_offset - height * np.sin(3 * np.pi / 4),
             center['y'] - y_offset + height * np.cos(3 * np.pi / 4))
        ]
        rect = Polygon(
            points,
            closed=True,
            linewidth=1.0,
            edgecolor='black',
            facecolor='white',
            zorder=10
        )
        text_x, text_y = center['x'] + height * 0.85, center['y'] - height * 0.85
        ha, va = 'center', 'top'

    plt.gca().add_patch(rect)
    plt.text(text_x, text_y, name, fontsize=6, ha=ha, va=va, color='black', zorder=11)


def draw_capacitor(center, name, orientation):
    plate_length = SCALE / 20
    gap = SCALE / 40
    cover_thickness = SCALE / 80

    if orientation == 'horizontal':
        x1 = center['x'] - gap / 2
        x2 = center['x'] + gap / 2
        y_top = center['y'] + plate_length / 2
        y_bottom = center['y'] - plate_length / 2

        plt.plot([x1, x1], [y_bottom, y_top], color='black', linewidth=1.0, zorder=10)
        plt.plot([x2, x2], [y_bottom, y_top], color='black', linewidth=1.0, zorder=10)

        rect = Rectangle(
            (x1, y_bottom),
            x2 - x1, y_top - y_bottom,
            facecolor='white',
            edgecolor='none',
            zorder=9.5
        )
        plt.gca().add_patch(rect)

        text_x, text_y = center['x'], center['y'] - plate_length
        ha, va = 'center', 'top'

    elif orientation == 'vertical':
        y1 = center['y'] - gap / 2
        y2 = center['y'] + gap / 2
        x_left = center['x'] - plate_length / 2
        x_right = center['x'] + plate_length / 2

        plt.plot([x_left, x_right], [y1, y1], color='black', linewidth=1.0, zorder=10)
        plt.plot([x_left, x_right], [y2, y2], color='black', linewidth=1.0, zorder=10)

        rect = Rectangle(
            (x_left, y1),
            x_right - x_left, y2 - y1,
            facecolor='white',
            edgecolor='none',
            zorder=9.5
        )
        plt.gca().add_patch(rect)

        text_x, text_y = center['x'] + plate_length, center['y']
        ha, va = 'left', 'center'

    elif orientation == 'diagonal':
        angle = np.pi / 4
        dx = plate_length / 2 * np.cos(angle + np.pi / 2)
        dy = plate_length / 2 * np.sin(angle + np.pi / 2)

        x1 = center['x'] - (gap / 2) * np.cos(angle)
        y1 = center['y'] - (gap / 2) * np.sin(angle)
        plt.plot([x1 - dx, x1 + dx], [y1 - dy, y1 + dy], color='black', linewidth=1.0, zorder=10)

        x2 = center['x'] + (gap / 2) * np.cos(angle)
        y2 = center['y'] + (gap / 2) * np.sin(angle)
        plt.plot([x2 - dx, x2 + dx], [y2 - dy, y2 + dy], color='black', linewidth=1.0, zorder=10)

        points = [
            (x1 - dx, y1 - dy),
            (x1 + dx, y1 + dy),
            (x2 + dx, y2 + dy),
            (x2 - dx, y2 - dy)
        ]
        rect = Polygon(
            points,
            closed=True,
            facecolor='white',
            edgecolor='none',
            zorder=9.5
        )
        plt.gca().add_patch(rect)

        text_x, text_y = center['x'] - plate_length * 0.7, center['y'] - plate_length * 0.7
        ha, va = 'center', 'top'

    elif orientation == '-diagonal':
        angle = 3 * np.pi / 4
        dx = plate_length / 2 * np.cos(angle + np.pi / 2)
        dy = plate_length / 2 * np.sin(angle + np.pi / 2)

        x1 = center['x'] - (gap / 2) * np.cos(angle)
        y1 = center['y'] - (gap / 2) * np.sin(angle)
        plt.plot([x1 - dx, x1 + dx], [y1 - dy, y1 + dy], color='black', linewidth=1.0, zorder=10)

        x2 = center['x'] + (gap / 2) * np.cos(angle)
        y2 = center['y'] + (gap / 2) * np.sin(angle)
        plt.plot([x2 - dx, x2 + dx], [y2 - dy, y2 + dy], color='black', linewidth=1.0, zorder=10)

        points = [
            (x1 - dx, y1 - dy),
            (x1 + dx, y1 + dy),
            (x2 + dx, y2 + dy),
            (x2 - dx, y2 - dy)
        ]
        rect = Polygon(
            points,
            closed=True,
            facecolor='white',
            edgecolor='none',
            zorder=9.5
        )
        plt.gca().add_patch(rect)

        text_x, text_y = center['x'] + plate_length * 0.7, center['y'] - plate_length * 0.7
        ha, va = 'center', 'top'

    plt.text(text_x, text_y, name, fontsize=6, ha=ha, va=va, color='black', zorder=11)


def draw_inductor(center, name, orientation):
    num_loops = 3
    total_length = SCALE / 10
    loop_spacing = total_length / num_loops
    loop_radius = loop_spacing / 2

    if orientation == 'horizontal':
        start_x = center['x'] - total_length / 2
        y_center = center['y']

        rect = Rectangle(
            (start_x, y_center - loop_radius),
            total_length, loop_radius * 2,
            facecolor='white',
            edgecolor='none',
            zorder=9.5
        )
        plt.gca().add_patch(rect)

        for i in range(num_loops):
            theta = np.linspace(0, np.pi, 100)
            x = start_x + i * loop_spacing + loop_radius * (1 - np.cos(theta))
            y = y_center + loop_radius * np.sin(theta)
            plt.plot(x, y, color='black', linewidth=1.0, zorder=10)

        text_x, text_y = center['x'], center['y'] - loop_radius * 1.8
        ha, va = 'center', 'top'

    elif orientation == 'vertical':
        start_y = center['y'] - total_length / 2
        x_center = center['x']

        rect = Rectangle(
            (x_center - loop_radius, start_y),
            loop_radius * 2, total_length,
            facecolor='white',
            edgecolor='none',
            zorder=9.5
        )
        plt.gca().add_patch(rect)

        for i in range(num_loops):
            theta = np.linspace(0, np.pi, 100)
            y = start_y + i * loop_spacing + loop_radius * (1 - np.cos(theta))
            x = x_center + loop_radius * np.sin(theta)
            plt.plot(x, y, color='black', linewidth=1.0, zorder=10)

        text_x, text_y = center['x'] + loop_radius * 1.8, center['y']
        ha, va = 'left', 'center'

    elif orientation == 'diagonal':
        angle = np.pi / 4
        start_x = center['x'] - (total_length / 2) * np.cos(angle)
        start_y = center['y'] - (total_length / 2) * np.sin(angle)

        points = [
            (start_x - loop_radius * np.sin(angle), start_y + loop_radius * np.cos(angle)),
            (start_x + total_length * np.cos(angle) - loop_radius * np.sin(angle),
             start_y + total_length * np.sin(angle) + loop_radius * np.cos(angle)),
            (start_x + total_length * np.cos(angle) + loop_radius * np.sin(angle),
             start_y + total_length * np.sin(angle) - loop_radius * np.cos(angle)),
            (start_x + loop_radius * np.sin(angle), start_y - loop_radius * np.cos(angle))
        ]
        rect = Polygon(
            points,
            closed=True,
            facecolor='white',
            edgecolor='none',
            zorder=9.5
        )
        plt.gca().add_patch(rect)

        for i in range(num_loops):
            theta = np.linspace(0, np.pi, 100)
            loop_x = start_x + i * loop_spacing * np.cos(angle) + loop_radius * (1 - np.cos(theta)) * np.cos(angle)
            loop_y = start_y + i * loop_spacing * np.sin(angle) + loop_radius * (1 - np.cos(theta)) * np.sin(angle)
            loop_x += loop_radius * np.sin(theta) * np.sin(angle)
            loop_y -= loop_radius * np.sin(theta) * np.cos(angle)
            plt.plot(loop_x, loop_y, color='black', linewidth=1.0, zorder=10)

        text_x, text_y = center['x'] - loop_radius * 1.8 * np.cos(angle), center['y'] - loop_radius * 1.8 * np.sin(
            angle)
        ha, va = 'center', 'top'

    elif orientation == '-diagonal':
        angle = 3 * np.pi / 4
        start_x = center['x'] - (total_length / 2) * np.cos(angle)
        start_y = center['y'] - (total_length / 2) * np.sin(angle)

        points = [
            (start_x - loop_radius * np.sin(angle), start_y + loop_radius * np.cos(angle)),
            (start_x + total_length * np.cos(angle) - loop_radius * np.sin(angle),
             start_y + total_length * np.sin(angle) + loop_radius * np.cos(angle)),
            (start_x + total_length * np.cos(angle) + loop_radius * np.sin(angle),
             start_y + total_length * np.sin(angle) - loop_radius * np.cos(angle)),
            (start_x + loop_radius * np.sin(angle), start_y - loop_radius * np.cos(angle))
        ]
        rect = Polygon(
            points,
            closed=True,
            facecolor='white',
            edgecolor='none',
            zorder=9.5
        )
        plt.gca().add_patch(rect)

        for i in range(num_loops):
            theta = np.linspace(0, np.pi, 100)
            loop_x = start_x + i * loop_spacing * np.cos(angle) + loop_radius * (1 - np.cos(theta)) * np.cos(angle)
            loop_y = start_y + i * loop_spacing * np.sin(angle) + loop_radius * (1 - np.cos(theta)) * np.sin(angle)
            loop_x += loop_radius * np.sin(theta) * np.sin(angle)
            loop_y -= loop_radius * np.sin(theta) * np.cos(angle)
            plt.plot(loop_x, loop_y, color='black', linewidth=1.0, zorder=10)

        text_x, text_y = center['x'] - loop_radius * 1.8 * np.cos(angle), center['y'] - loop_radius * 1.8 * np.sin(
            angle)
        ha, va = 'center', 'top'

    plt.text(text_x, text_y, name, fontsize=6, ha=ha, va=va, color='black', zorder=11)


def draw_active_dipole(center, orientation):
    radius = SCALE / 60
    spacing = SCALE / 15 + radius * 2

    width = spacing
    height = radius * 2.5

    if orientation == 'horizontal':
        point_a = (center['x'] - spacing / 2, center['y'])
        point_b = (center['x'] + spacing / 2, center['y'])

        lower_left = (center['x'] - width / 2, center['y'] - height / 2)
        rect_width, rect_height = width, height

        text_a = (point_a[0], point_a[1] - radius * 2)
        text_b = (point_b[0], point_b[1] - radius * 2)
        ha, va = 'center', 'top'

    elif orientation == 'vertical':
        point_a = (center['x'], center['y'] - spacing / 2)
        point_b = (center['x'], center['y'] + spacing / 2)

        lower_left = (center['x'] - height / 2, center['y'] - width / 2)
        rect_width, rect_height = height, width

        text_a = (point_a[0] + radius * 2, point_a[1])
        text_b = (point_b[0] + radius * 2, point_b[1])
        ha, va = 'left', 'center'

    rect = plt.Rectangle(
        lower_left,
        rect_width, rect_height,
        linewidth=0,
        edgecolor=None,
        facecolor='white',
        zorder=5
    )
    plt.gca().add_patch(rect)

    circle_a = plt.Circle(point_a, radius, edgecolor='black', facecolor='white', linewidth=1.0, zorder=10)
    circle_b = plt.Circle(point_b, radius, edgecolor='black', facecolor='white', linewidth=1.0, zorder=10)
    plt.gca().add_patch(circle_a)
    plt.gca().add_patch(circle_b)

    plt.text(text_a[0], text_a[1], 'a', fontsize=6, ha=ha, va=va, color='black', zorder=11)
    plt.text(text_b[0], text_b[1], 'b', fontsize=6, ha=ha, va=va, color='black', zorder=11)


def draw_voltage_source(center, name, orientation):
    radius = SCALE / 20
    arrow_head_length = radius * 0.8
    arrow_head_width = radius / 2

    ax = plt.gca()

    circle = plt.Circle(
        (center['x'], center['y']),
        radius,
        edgecolor='black',
        facecolor='white',
        linewidth=1.0,
        zorder=10
    )
    ax.add_patch(circle)

    rect = plt.Rectangle(
        (center['x'] - radius, center['y'] - radius),
        2 * radius, 2 * radius,
        facecolor='white',
        edgecolor='none',
        zorder=9.5
    )
    ax.add_patch(rect)

    if orientation == 'horizontal':
        x_start = center['x'] - radius
        x_end = center['x'] + radius
        y = center['y']

        plt.plot(
            [x_start, x_end - arrow_head_length],
            [y, y],
            color='black',
            linewidth=1.0,
            zorder=10
        )

        triangle = np.array([
            [x_end - 0.2 * radius, y],
            [x_end - arrow_head_length, y + arrow_head_width / 2],
            [x_end - arrow_head_length, y - arrow_head_width / 2]
        ])

        polygon = plt.Polygon(
            triangle,
            closed=True,
            facecolor='black',
            edgecolor='black',
            zorder=11
        )
        ax.add_patch(polygon)

        text_x, text_y = center['x'], center['y'] - radius * 1.8
        ha, va = 'center', 'top'

    elif orientation == 'vertical':
        y_start = center['y'] + radius
        y_end = center['y'] - radius
        x = center['x']

        plt.plot(
            [x, x],
            [y_start, y_end + arrow_head_length],
            color='black',
            linewidth=1.0,
            zorder=10
        )

        triangle = np.array([
            [x, y_end + 0.2 * radius],
            [x - arrow_head_width / 2, y_end + arrow_head_length],
            [x + arrow_head_width / 2, y_end + arrow_head_length]
        ])

        polygon = plt.Polygon(
            triangle,
            closed=True,
            facecolor='black',
            edgecolor='black',
            zorder=11
        )
        ax.add_patch(polygon)

        text_x, text_y = center['x'] + radius * 1.8, center['y']
        ha, va = 'left', 'center'

    plt.text(
        text_x, text_y, name,
        fontsize=6,
        ha=ha, va=va,
        color='black',
        zorder=12
    )


def draw_current_source(center, name, orientation):
    radius = SCALE / 20

    circle = plt.Circle(
        (center['x'], center['y']),
        radius,
        edgecolor='black',
        facecolor='white',
        linewidth=1.0,
        zorder=10
    )
    plt.gca().add_patch(circle)

    rect = plt.Rectangle(
        (center['x'] - radius, center['y'] - radius),
        2 * radius, 2 * radius,
        facecolor='white',
        edgecolor='none',
        zorder=9.5
    )
    plt.gca().add_patch(rect)

    x = center['x']
    y = center['y']

    if orientation == 'horizontal':

        plt.plot(
            [x - radius, x], [y, y],
            color='black',
            linewidth=1.0,
            zorder=10
        )
        plt.plot(
            [x + radius, x + (radius / 2)], [y, y],
            color='black',
            linewidth=1.0,
            zorder=10
        )

        plt.plot(
            [x - (radius / 3), x], [y + (radius / 3), y],
            color='black',
            linewidth=1.0,
            zorder=10
        )
        plt.plot(
            [x - (radius / 3), x], [y - (radius / 3), y],
            color='black',
            linewidth=1.0,
            zorder=10
        )

        plt.plot(
            [x + (radius / 6), x + (radius / 2)], [y + (radius / 3), y],
            color='black',
            linewidth=1.0,
            zorder=10
        )
        plt.plot(
            [x + (radius / 6), x + (radius / 2)], [y - (radius / 3), y],
            color='black',
            linewidth=1.0,
            zorder=10
        )

        text_x, text_y = x, y - radius * 1.8
        ha, va = 'center', 'top'

    elif orientation == 'vertical':
        plt.plot(
            [x, x], [y - radius, y],
            color='black',
            linewidth=1.0,
            zorder=10
        )
        plt.plot(
            [x, x], [y + radius, y + (radius / 2)],
            color='black',
            linewidth=1.0,
            zorder=10
        )

        plt.plot(
            [x + (radius / 3), x], [y - (radius / 3), y],
            color='black',
            linewidth=1.0,
            zorder=10
        )
        plt.plot(
            [x - (radius / 3), x], [y - (radius / 3), y],
            color='black',
            linewidth=1.0,
            zorder=10
        )

        plt.plot(
            [x + (radius / 3), x], [y + (radius / 6), y + (radius / 2)],
            color='black',
            linewidth=1.0,
            zorder=10
        )
        plt.plot(
            [x - (radius / 3), x], [y + (radius / 6), y + (radius / 2)],
            color='black',
            linewidth=1.0,
            zorder=10
        )

        text_x, text_y = center['x'] + radius * 1.8, y
        ha, va = 'center', 'top'

    plt.text(text_x, text_y, name, fontsize=6, ha=ha, va=va, color='black', zorder=11)


def draw_switch(center, orientation):
    width = SCALE / 10
    gap = SCALE / 10
    wire_length = (width - gap) / 2

    if orientation == 'horizontal':
        x1 = center['x'] - width / 2
        x2 = center['x'] + width / 2
        y = center['y']

        plt.plot([x1, x1 + wire_length], [y, y], color='black', linewidth=1.0, zorder=9)
        plt.plot([x2 - wire_length, x2], [y, y], color='black', linewidth=1.0, zorder=9)

        plt.plot([x1 + wire_length, x2 - wire_length], [y, y], color='white', linewidth=1.5, zorder=10)

        contact_x = [x1 + wire_length, x2 - wire_length]
        contact_y = [y, y + SCALE / 40]
        plt.plot(contact_x, contact_y, color='black', linewidth=1.0, zorder=11)

    elif orientation == 'vertical':
        y1 = center['y'] - width / 2
        y2 = center['y'] + width / 2
        x = center['x']

        plt.plot([x, x], [y1, y1 + wire_length], color='black', linewidth=1.0, zorder=9)
        plt.plot([x, x], [y2 - wire_length, y2], color='black', linewidth=1.0, zorder=9)

        plt.plot([x, x], [y1 + wire_length, y2 - wire_length], color='white', linewidth=1.5, zorder=10)

        contact_y = [y1 + wire_length, y2 - wire_length]
        contact_x = [x, x + SCALE / 40]
        plt.plot(contact_x, contact_y, color='black', linewidth=1.0, zorder=11)


def draw_circle(center, name, color='red'):
    radius = SCALE / 40

    circle = plt.Circle(
        (center['x'], center['y']),
        radius,
        linewidth=1.0,
        edgecolor=color,
        facecolor='white',
        zorder=10
    )

    plt.gca().add_patch(circle)
    plt.text(center['x'], center['y'] - radius * 1.5, name,
             fontsize=6, ha='center', va='top', color='black', zorder=11)