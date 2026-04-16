import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ======================== Геометрические функции ========================
def line_intersection(p1, p2, p3, p4):
    """Пересечение прямых (p1-p2) и (p3-p4)"""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    
    denom = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
    if abs(denom) < 1e-10:
        return None
    t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / denom
    x = x1 + t*(x2 - x1)
    y = y1 + t*(y2 - y1)
    return np.array([x, y])

def foot_of_perpendicular(point, line_start, line_end):
    """Проекция точки на прямую (line_start - line_end)"""
    p = np.array(point)
    a = np.array(line_start)
    b = np.array(line_end)
    ab = b - a
    t = np.dot(p - a, ab) / np.dot(ab, ab)
    return a + t * ab

def orthocenter(A, B, C):
    """Ортоцентр треугольника"""
    # Высоты: из A на BC, из B на AC
    foot_A = foot_of_perpendicular(A, B, C)
    foot_B = foot_of_perpendicular(B, A, C)
    return line_intersection(A, foot_A, B, foot_B)

def nine_point_circle(A, B, C):
    """Возвращает центр и радиус окружности девяти точек"""
    # Центр описанной окружности (пересечение серединных перпендикуляров)
    mid_AB = (A + B) / 2
    mid_AC = (A + C) / 2
    perp_AB = np.array([-(B[1]-A[1]), B[0]-A[0]])  # перпендикуляр к AB
    perp_AC = np.array([-(C[1]-A[1]), C[0]-A[0]])  # перпендикуляр к AC
    
    def line_from_point_and_dir(p, d):
        return p, p + d
    
    O_circ = line_intersection(mid_AB, mid_AB + perp_AB, mid_AC, mid_AC + perp_AC)
    R_circ = np.linalg.norm(O_circ - A)  # радиус описанной окружности
    
    H = orthocenter(A, B, C)
    N = (O_circ + H) / 2  # центр окружности девяти точек
    R = R_circ / 2
    return N, R

# ======================== Данные треугольника ========================
# Задайте координаты вершин треугольника (изменяйте для экспериментов)
A = np.array([0.0, 0.0])
B = np.array([6.0, 0.0])
C = np.array([2.0, 5.0])

# Вычисление всех точек
mid_AB = (A + B) / 2
mid_BC = (B + C) / 2
mid_CA = (C + A) / 2

foot_A = foot_of_perpendicular(A, B, C)
foot_B = foot_of_perpendicular(B, A, C)
foot_C = foot_of_perpendicular(C, A, B)

H = orthocenter(A, B, C)
mid_AH = (A + H) / 2
mid_BH = (B + H) / 2
mid_CH = (C + H) / 2

# Все девять точек
nine_points = [mid_AB, mid_BC, mid_CA, foot_A, foot_B, foot_C, mid_AH, mid_BH, mid_CH]

N, R = nine_point_circle(A, B, C)

# ======================== Настройка анимации ========================
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.6)

# Пределы осей с отступом
all_points = np.vstack([A, B, C, H] + nine_points)
x_min, x_max = all_points[:, 0].min(), all_points[:, 0].max()
y_min, y_max = all_points[:, 1].min(), all_points[:, 1].max()
dx, dy = (x_max - x_min)*0.2, (y_max - y_min)*0.2
ax.set_xlim(x_min - dx, x_max + dx)
ax.set_ylim(y_min - dy, y_max + dy)
ax.set_title("Построение окружности девяти точек (окружности Эйлера)")

# Элементы, которые будут обновляться
triangle_line = None
mid_points_scat = None
foot_points_scat = None
euler_points_scat = None
circle_artist = None

def init():
    """Инициализация (пустой график)"""
    global triangle_line, mid_points_scat, foot_points_scat, euler_points_scat, circle_artist
    triangle_line, = ax.plot([], [], 'b-', lw=2, label='Треугольник')
    mid_points_scat = ax.scatter([], [], c='green', s=80, zorder=5, label='Середины сторон')
    foot_points_scat = ax.scatter([], [], c='orange', s=80, zorder=5, label='Основания высот')
    euler_points_scat = ax.scatter([], [], c='purple', s=80, zorder=5, label='Середины отрезков от ортоцентра')
    circle_artist = ax.plot([], [], 'r--', lw=2, label='Окружность девяти точек')[0]
    ax.legend(loc='upper right')
    return triangle_line, mid_points_scat, foot_points_scat, euler_points_scat, circle_artist

def update(frame):
    """
    frame: 0 - только треугольник
           1 + середины сторон
           2 + основания высот
           3 + середины отрезков AH, BH, CH
           4 + окружность
    """
    # Треугольник (всегда рисуем)
    triangle_line.set_data([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]])
    
    # Середины сторон (кадр >= 1)
    if frame >= 1:
        mid_points_scat.set_offsets([mid_AB, mid_BC, mid_CA])
    else:
        mid_points_scat.set_offsets(np.empty((0, 2)))
    
    # Основания высот (кадр >= 2)
    if frame >= 2:
        foot_points_scat.set_offsets([foot_A, foot_B, foot_C])
    else:
        foot_points_scat.set_offsets(np.empty((0, 2)))
    
    # Середины отрезков от ортоцентра до вершин (кадр >= 3)
    if frame >= 3:
        euler_points_scat.set_offsets([mid_AH, mid_BH, mid_CH])
    else:
        euler_points_scat.set_offsets(np.empty((0, 2)))
    
    # Окружность (кадр == 4)
    if frame == 4:
        theta = np.linspace(0, 2*np.pi, 100)
        x_circ = N[0] + R * np.cos(theta)
        y_circ = N[1] + R * np.sin(theta)
        circle_artist.set_data(x_circ, y_circ)
    else:
        circle_artist.set_data([], [])
    
    # Заголовок в зависимости от шага
    titles = [
        "Шаг 1: Треугольник",
        "Шаг 2: Середины сторон",
        "Шаг 3: Основания высот",
        "Шаг 4: Точки Эйлера (середины от ортоцентра)",
        "Шаг 5: Окружность девяти точек"
    ]
    ax.set_title(titles[frame])
    
    return triangle_line, mid_points_scat, foot_points_scat, euler_points_scat, circle_artist

# Создание анимации (5 кадров, пауза 1.5 секунды между шагами)
ani = FuncAnimation(fig, update, frames=5, init_func=init, interval=1500, blit=False, repeat=False)

# Отображение анимации
# plt.show()

# Чтобы сохранить анимацию в GIF (раскомментируйте при необходимости)
ani.save('docs/pic/nine_point_circle.gif', writer='pillow', fps=1)