import numpy as np
import matplotlib.pyplot as plt

# ======================== Вершины треугольника ========================
A = np.array([0.0, 0.0])
B = np.array([6.0, 0.0])
C = np.array([2.0, 5.0])   # остроугольный треугольник

# ======================== Функция проекции точки на прямую ========================
def foot_of_perpendicular(P, X, Y):
    """Основание перпендикуляра из точки P на прямую XY"""
    P = np.array(P)
    X = np.array(X)
    Y = np.array(Y)
    XY = Y - X
    t = np.dot(P - X, XY) / np.dot(XY, XY)
    foot = X + t * XY
    return foot

# ======================== Вычисляем основания высот ========================
foot_A = foot_of_perpendicular(A, B, C)   # из A на BC
foot_B = foot_of_perpendicular(B, A, C)   # из B на AC
foot_C = foot_of_perpendicular(C, A, B)   # из C на AB

# ======================== Ортоцентр (пересечение двух высот) ========================
# Решение системы: пересечение прямых (A - foot_A) и (B - foot_B)
def line_intersection(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    denom = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
    if abs(denom) < 1e-12:
        return None
    t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / denom
    x = x1 + t*(x2 - x1)
    y = y1 + t*(y2 - y1)
    return np.array([x, y])

orthocenter = line_intersection(A, foot_A, B, foot_B)

# ======================== Построение графика ========================
fig, ax = plt.subplots(figsize=(9, 6))
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.6)

# Треугольник
triangle = plt.Polygon([A, B, C], fill=None, edgecolor='blue', linewidth=2)
ax.add_patch(triangle)

# Высоты (красные пунктирные линии)
ax.plot([A[0], foot_A[0]], [A[1], foot_A[1]], 'r--', linewidth=1.5)
ax.plot([B[0], foot_B[0]], [B[1], foot_B[1]], 'r--', linewidth=1.5)
ax.plot([C[0], foot_C[0]], [C[1], foot_C[1]], 'r--', linewidth=1.5)

# Основания высот (зелёные точки)
ax.scatter(*foot_A, color='green', s=60, zorder=5)
ax.scatter(*foot_B, color='green', s=60, zorder=5)
ax.scatter(*foot_C, color='green', s=60, zorder=5)

# Ортоцентр (оранжевая звезда)
ax.scatter(*orthocenter, color='orange', s=120, marker='*', zorder=6, label='Ортоцентр')

# Подписи вершин
ax.text(A[0]-0.3, A[1]-0.3, 'A', fontsize=12, fontweight='bold')
ax.text(B[0]+0.1, B[1]-0.3, 'B', fontsize=12, fontweight='bold')
ax.text(C[0]-0.2, C[1]+0.2, 'C', fontsize=12, fontweight='bold')

# Подписи оснований (по желанию)
ax.text(foot_A[0]+0.1, foot_A[1]+0.1, "H_A", fontsize=9, color='green')
ax.text(foot_B[0]-0.3, foot_B[1]+0.2, "H_B", fontsize=9, color='green')
ax.text(foot_C[0]+0.1, foot_C[1]-0.2, "H_C", fontsize=9, color='green')

# Обозначения прямых углов (маленькие квадратики)
def draw_right_angle(ax, p, foot, vertex, size=0.2):
    """Рисует квадратик прямого угла в точке foot между отрезками foot-vertex и foot-p"""
    # Векторы от foot к вершине и к точке p (основание перпендикуляра не нужно, у нас foot и есть основание)
    # Нам нужно показать угол между стороной треугольника (например, BC) и высотой (A-foot_A).
    # Проще: рисуем квадратик в точке foot, повёрнутый соответственно.
    v1 = np.array(vertex) - np.array(foot)
    v2 = np.array(p) - np.array(foot)
    # Нормируем
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    # Точки квадратика
    corner = foot + v1 * size
    corner2 = foot + v2 * size
    corner3 = foot + v1 * size + v2 * size
    # Рисуем две линии и дугу (упрощённо: ломаная)
    ax.plot([foot[0], corner[0]], [foot[1], corner[1]], 'k', lw=1)
    ax.plot([foot[0], corner2[0]], [foot[1], corner2[1]], 'k', lw=1)
    ax.plot([corner[0], corner3[0]], [corner[1], corner3[1]], 'k', lw=1)
    ax.plot([corner2[0], corner3[0]], [corner2[1], corner3[1]], 'k', lw=1)

# Рисуем прямые углы только для острых углов (чтобы не рисовать на продолжениях)
# В остроугольном треугольнике все основания лежат на сторонах, можно рисовать.
draw_right_angle(ax, A, foot_A, B, size=0.15)  # угол между BC и высотой из A
draw_right_angle(ax, B, foot_B, A, size=0.15)
draw_right_angle(ax, C, foot_C, A, size=0.15)

# ======================== Легенда снаружи ========================
handles = [
    plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
    plt.Line2D([0], [0], color='red', linestyle='--', lw=1.5, label='Высоты'),
    plt.scatter([0], [0], c='green', s=60, label='Основания высот'),
    plt.scatter([0], [0], c='orange', s=120, marker='*', label='Ортоцентр')
]
ax.legend(handles=handles, loc='center left', bbox_to_anchor=(1, 0.5))
plt.subplots_adjust(right=0.75)

# ======================== Границы ========================
all_points = np.vstack([A, B, C, foot_A, foot_B, foot_C, orthocenter])
x_min, x_max = all_points[:,0].min(), all_points[:,0].max()
y_min, y_max = all_points[:,1].min(), all_points[:,1].max()
dx = (x_max - x_min) * 0.2
dy = (y_max - y_min) * 0.2
ax.set_xlim(x_min - dx, x_max + dx)
ax.set_ylim(y_min - dy, y_max + dy)

ax.set_title('Высоты треугольника и ортоцентр', fontsize=14)
ax.set_xlabel('x')
ax.set_ylabel('y')

# Сохранить (раскомментируйте)
plt.savefig('docs/pic/altitudes_triangle.png', dpi=150, bbox_inches='tight')

# plt.show()