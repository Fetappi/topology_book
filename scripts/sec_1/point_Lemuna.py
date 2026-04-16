import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ==========================================
# Вершины треугольника
# ==========================================
A = np.array([0.0, 0.0])
B = np.array([6.0, 0.0])
C = np.array([2.0, 5.0])

# ==========================================
# Длины сторон
# ==========================================
a = np.linalg.norm(B - C)   # BC
b = np.linalg.norm(A - C)   # AC
c = np.linalg.norm(A - B)   # AB

# ---------- Для вершины A ----------
mid_BC = (B + C) / 2
t_bis_A = c / (b + c)
bis_A = B + t_bis_A * (C - B)
t_sym_A = c**2 / (b**2 + c**2)
sym_A = B + t_sym_A * (C - B)

# ---------- Для вершины B ----------
mid_AC = (A + C) / 2
t_bis_B = c / (a + c)   # деление AC: от A к C, отношение AB:BC = c:a
bis_B = A + t_bis_B * (C - A)
t_sym_B = c**2 / (a**2 + c**2)
sym_B = A + t_sym_B * (C - A)

# ---------- Для вершины C ----------
mid_AB = (A + B) / 2
t_bis_C = b / (a + b)   # деление AB: от A к B, отношение AC:BC = b:a
bis_C = A + t_bis_C * (B - A)
t_sym_C = b**2 / (a**2 + b**2)
sym_C = A + t_sym_C * (B - A)

# ---------- Точка Лемуана ----------
L = (a**2 * A + b**2 * B + c**2 * C) / (a**2 + b**2 + c**2)

# ==========================================
# Функция для бесконечной прямой
# ==========================================
def get_extended_line(p1, p2, ax, factor=3.0):
    v = p2 - p1
    length = np.linalg.norm(v)
    if length == 0:
        return [], []
    v = v / length
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    diag = max(xlim[1]-xlim[0], ylim[1]-ylim[0])
    extension = diag * factor
    p_start = p1 - extension * v
    p_end = p1 + extension * v
    return [p_start[0], p_end[0]], [p_start[1], p_end[1]]

# ==========================================
# Настройка графика
# ==========================================
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.6)

# Границы осей
all_pts = np.vstack([A, B, C])
x_min, x_max = all_pts[:,0].min(), all_pts[:,0].max()
y_min, y_max = all_pts[:,1].min(), all_pts[:,1].max()
dx = (x_max - x_min) * 0.3
dy = (y_max - y_min) * 0.3
ax.set_xlim(x_min - dx, x_max + dx)
ax.set_ylim(y_min - dy, y_max + dy)

# Элементы для анимации
triangle_line, = ax.plot([], [], 'b-', lw=2)
median_line, = ax.plot([], [], 'g-', lw=1.5)      # текущая медиана
bisector_line, = ax.plot([], [], 'b-', lw=1.5)    # текущая биссектриса
sym_line, = ax.plot([], [], 'r-', lw=1.5)         # текущая симедиана (для одной вершины)
# Симедианы, которые остаются после построения
sym_A_line, = ax.plot([], [], 'r-', lw=1.5, alpha=0.0)   # будет видна после шага A
sym_B_line, = ax.plot([], [], 'r-', lw=1.5, alpha=0.0)
sym_C_line, = ax.plot([], [], 'r-', lw=1.5, alpha=0.0)
lem_point = ax.scatter([], [], c='orange', s=150, marker='*', zorder=10)

# Подписи вершин
ax.text(A[0]-0.3, A[1]-0.3, 'A', fontsize=12, fontweight='bold')
ax.text(B[0]+0.1, B[1]-0.3, 'B', fontsize=12, fontweight='bold')
ax.text(C[0]-0.2, C[1]+0.2, 'C', fontsize=12, fontweight='bold')

# Легенда (будет обновляться)
legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.subplots_adjust(right=0.75)

def update_legend(frame):
    """Обновляет легенду в зависимости от кадра"""
    # frame: 0 - только треугольник
    # 1: медиана A; 2: +биссектриса A; 3: +симедиана A; 4: оставить симедиану A
    # 5: медиана B; 6: +биссектриса B; 7: +симедиана B; 8: оставить симедиану B
    # 9: медиана C; 10: +биссектриса C; 11: +симедиана C; 12: оставить симедиану C
    # 13: все три симедианы + точка Лемуана
    if frame == 0:
        handles = [plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник')]
    elif frame == 1:
        handles = [plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
                   plt.Line2D([0], [0], color='green', lw=1.5, label='Медиана (A)')]
    elif frame == 2:
        handles = [plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
                   plt.Line2D([0], [0], color='green', lw=1.5, label='Медиана (A)'),
                   plt.Line2D([0], [0], color='blue', lw=1.5, label='Биссектриса (A)')]
    elif frame == 3:
        handles = [plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
                   plt.Line2D([0], [0], color='green', lw=1.5, label='Медиана (A)'),
                   plt.Line2D([0], [0], color='blue', lw=1.5, label='Биссектриса (A)'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (A) – отражение')]
    elif frame == 4:
        handles = [plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (A)')]
    elif frame == 5:
        handles = [plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (A)'),
                   plt.Line2D([0], [0], color='green', lw=1.5, label='Медиана (B)')]
    elif frame == 6:
        handles = [plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (A)'),
                   plt.Line2D([0], [0], color='green', lw=1.5, label='Медиана (B)'),
                   plt.Line2D([0], [0], color='blue', lw=1.5, label='Биссектриса (B)')]
    elif frame == 7:
        handles = [plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (A)'),
                   plt.Line2D([0], [0], color='green', lw=1.5, label='Медиана (B)'),
                   plt.Line2D([0], [0], color='blue', lw=1.5, label='Биссектриса (B)'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (B)')]
    elif frame == 8:
        handles = [plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (A)'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (B)')]
    elif frame == 9:
        handles = [plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (A)'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (B)'),
                   plt.Line2D([0], [0], color='green', lw=1.5, label='Медиана (C)')]
    elif frame == 10:
        handles = [plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (A)'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (B)'),
                   plt.Line2D([0], [0], color='green', lw=1.5, label='Медиана (C)'),
                   plt.Line2D([0], [0], color='blue', lw=1.5, label='Биссектриса (C)')]
    elif frame == 11:
        handles = [plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (A)'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (B)'),
                   plt.Line2D([0], [0], color='green', lw=1.5, label='Медиана (C)'),
                   plt.Line2D([0], [0], color='blue', lw=1.5, label='Биссектриса (C)'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (C)')]
    elif frame == 12:
        handles = [plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (A)'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (B)'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедиана (C)')]
    else:  # frame == 13
        handles = [plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
                   plt.Line2D([0], [0], color='red', lw=1.5, label='Симедианы (A, B, C)'),
                   plt.scatter([0], [0], c='orange', s=150, marker='*', label='Точка Лемуана')]
    legend = ax.legend(handles=handles, loc='center left', bbox_to_anchor=(1, 0.5))
    return legend

# ==========================================
# Анимация (14 кадров: 0..13)
# ==========================================
def init():
    triangle_line.set_data([], [])
    median_line.set_data([], [])
    bisector_line.set_data([], [])
    sym_line.set_data([], [])
    sym_A_line.set_data([], [])
    sym_B_line.set_data([], [])
    sym_C_line.set_data([], [])
    lem_point.set_offsets(np.empty((0, 2)))
    update_legend(0)
    return (triangle_line, median_line, bisector_line, sym_line,
            sym_A_line, sym_B_line, sym_C_line, lem_point)

def update(frame):
    # frame 0: только треугольник
    triangle_line.set_data([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]])

    # По умолчанию все вспомогательные линии не видны
    median_line.set_data([], [])
    bisector_line.set_data([], [])
    sym_line.set_data([], [])

    # Симедианы, которые уже построены, показываем всегда (кроме случая frame=0)
    # Они становятся видимыми после соответствующих шагов
    if frame >= 4:
        x, y = get_extended_line(A, sym_A, ax)
        sym_A_line.set_data(x, y)
        sym_A_line.set_alpha(1.0)
    else:
        sym_A_line.set_data([], [])

    if frame >= 8:
        x, y = get_extended_line(B, sym_B, ax)
        sym_B_line.set_data(x, y)
        sym_B_line.set_alpha(1.0)
    else:
        sym_B_line.set_data([], [])

    if frame >= 12:
        x, y = get_extended_line(C, sym_C, ax)
        sym_C_line.set_data(x, y)
        sym_C_line.set_alpha(1.0)
    else:
        sym_C_line.set_data([], [])

    # Логика для каждого кадра
    if frame == 1:          # медиана A
        x, y = get_extended_line(A, mid_BC, ax)
        median_line.set_data(x, y)
    elif frame == 2:        # биссектриса A
        x, y = get_extended_line(A, mid_BC, ax)
        median_line.set_data(x, y)
        xb, yb = get_extended_line(A, bis_A, ax)
        bisector_line.set_data(xb, yb)
    elif frame == 3:        # симедиана A (все три линии)
        x, y = get_extended_line(A, mid_BC, ax)
        median_line.set_data(x, y)
        xb, yb = get_extended_line(A, bis_A, ax)
        bisector_line.set_data(xb, yb)
        xs, ys = get_extended_line(A, sym_A, ax)
        sym_line.set_data(xs, ys)
    elif frame == 4:        # убрать медиану и биссектрису A, оставить симедиану A
        # симедиана A уже показана через sym_A_line, ничего дополнительного
        pass
    elif frame == 5:        # медиана B
        x, y = get_extended_line(B, mid_AC, ax)
        median_line.set_data(x, y)
    elif frame == 6:        # биссектриса B
        x, y = get_extended_line(B, mid_AC, ax)
        median_line.set_data(x, y)
        xb, yb = get_extended_line(B, bis_B, ax)
        bisector_line.set_data(xb, yb)
    elif frame == 7:        # симедиана B
        x, y = get_extended_line(B, mid_AC, ax)
        median_line.set_data(x, y)
        xb, yb = get_extended_line(B, bis_B, ax)
        bisector_line.set_data(xb, yb)
        xs, ys = get_extended_line(B, sym_B, ax)
        sym_line.set_data(xs, ys)
    elif frame == 8:        # убрать медиану и биссектрису B
        pass
    elif frame == 9:        # медиана C
        x, y = get_extended_line(C, mid_AB, ax)
        median_line.set_data(x, y)
    elif frame == 10:       # биссектриса C
        x, y = get_extended_line(C, mid_AB, ax)
        median_line.set_data(x, y)
        xb, yb = get_extended_line(C, bis_C, ax)
        bisector_line.set_data(xb, yb)
    elif frame == 11:       # симедиана C
        x, y = get_extended_line(C, mid_AB, ax)
        median_line.set_data(x, y)
        xb, yb = get_extended_line(C, bis_C, ax)
        bisector_line.set_data(xb, yb)
        xs, ys = get_extended_line(C, sym_C, ax)
        sym_line.set_data(xs, ys)
    elif frame == 12:       # убрать медиану и биссектрису C
        pass
    elif frame == 13:       # добавить точку Лемуана
        lem_point.set_offsets([L])
        # также можно дополнительно подчеркнуть симедианы, но они уже видны
    else:
        lem_point.set_offsets(np.empty((0, 2)))

    # Обновить легенду
    update_legend(frame)

    # Заголовки
    titles = [
        "Треугольник",
        "Шаг 1: Медиана из A",
        "Шаг 2: Биссектриса из A",
        "Шаг 3: Симедиана из A (отражение медианы относительно биссектрисы)",
        "Шаг 4: Осталась симедиана A",
        "Шаг 5: Медиана из B",
        "Шаг 6: Биссектриса из B",
        "Шаг 7: Симедиана из B",
        "Шаг 8: Остались симедианы A и B",
        "Шаг 9: Медиана из C",
        "Шаг 10: Биссектриса из C",
        "Шаг 11: Симедиана из C",
        "Шаг 12: Все три симедианы построены",
        "Шаг 13: Точка Лемуана – пересечение симедиан"
    ]
    ax.set_title(titles[frame])

    return (triangle_line, median_line, bisector_line, sym_line,
            sym_A_line, sym_B_line, sym_C_line, lem_point)

ani = FuncAnimation(fig, update, frames=14, init_func=init,
                    interval=2000, blit=False, repeat=False)

# plt.show()
ani.save('docs/pic/symmedian_all_vertices.gif', writer='pillow', fps=0.5)