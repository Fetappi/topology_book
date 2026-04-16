import numpy as np
import matplotlib.pyplot as plt

# ======================== Вершины треугольника ========================
A = np.array([0.0, 0.0])
B = np.array([6.0, 0.0])
C = np.array([2.0, 5.0])   # можно менять

# ======================== Середины сторон ========================
mid_AB = (A + B) / 2
mid_BC = (B + C) / 2
mid_CA = (C + A) / 2

# ======================== Функция для построения серединного перпендикуляра ========================
def perpendicular_bisector(p1, p2, mid):
    """
    Возвращает две точки (далеко) на прямой, проходящей через mid
    и перпендикулярной отрезку p1-p2.
    """
    direction = p2 - p1
    # Вектор, перпендикулярный direction (поворот на 90°)
    perp = np.array([-direction[1], direction[0]])
    # Нормируем для масштаба
    perp = perp / np.linalg.norm(perp) * 5   # длина 5 для выхода за пределы
    return mid - perp, mid + perp

# ======================== Центр описанной окружности ========================
# Пересечение двух серединных перпендикуляров (например, к AB и к AC)
def line_intersection(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    denom = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
    if abs(denom) < 1e-12:
        return None
    t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / denom
    x = x1 + t*(x2 - x1)
    y = y1 + t*(y2 - y1)
    return np.array([x, y])

# Две прямые: через mid_AB перпендикулярно AB, через mid_AC перпендикулярно AC
p1, p2 = perpendicular_bisector(A, B, mid_AB)
p3, p4 = perpendicular_bisector(A, C, mid_CA)
circumcenter = line_intersection(p1, p2, p3, p4)

# Радиус описанной окружности
radius = np.linalg.norm(circumcenter - A)

# ======================== Построение графики ========================
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_aspect('equal')

ax.grid(True, linestyle='--', alpha=0.6)

# Треугольник
triangle = plt.Polygon([A, B, C], fill=None, edgecolor='blue', linewidth=2)
ax.add_patch(triangle)

# Серединные перпендикуляры (зелёные пунктирные линии)
# Для каждой стороны строим прямую, проходящую через середину и перпендикулярную стороне
bis_AB = perpendicular_bisector(A, B, mid_AB)
ax.plot([bis_AB[0][0], bis_AB[1][0]], [bis_AB[0][1], bis_AB[1][1]], 'g--', linewidth=1.5)

bis_BC = perpendicular_bisector(B, C, mid_BC)
ax.plot([bis_BC[0][0], bis_BC[1][0]], [bis_BC[0][1], bis_BC[1][1]], 'g--', linewidth=1.5)

bis_CA = perpendicular_bisector(C, A, mid_CA)
ax.plot([bis_CA[0][0], bis_CA[1][0]], [bis_CA[0][1], bis_CA[1][1]], 'g--', linewidth=1.5)

# Середины сторон (зелёные точки)
ax.scatter(*mid_AB, color='lime', s=60, zorder=5)
ax.scatter(*mid_BC, color='lime', s=60, zorder=5)
ax.scatter(*mid_CA, color='lime', s=60, zorder=5)

# Центр описанной окружности (красная звезда)
ax.scatter(*circumcenter, color='red', s=120, marker='*', zorder=6, label='Центр описанной окружности')

# Описанная окружность (красная сплошная линия)
theta = np.linspace(0, 2*np.pi, 200)
circle_x = circumcenter[0] + radius * np.cos(theta)
circle_y = circumcenter[1] + radius * np.sin(theta)
ax.plot(circle_x, circle_y, 'r-', linewidth=2, label='Описанная окружность')

# Подписи вершин
ax.text(A[0]-0.3, A[1]-0.3, 'A', fontsize=12, fontweight='bold')
ax.text(B[0]+0.1, B[1]-0.3, 'B', fontsize=12, fontweight='bold')
ax.text(C[0]-0.2, C[1]+0.2, 'C', fontsize=12, fontweight='bold')

# Подписи середин (по желанию)
ax.text(mid_AB[0]+0.2, mid_AB[1]-0.3, "M_AB", fontsize=9, color='green')
ax.text(mid_BC[0]+0.2, mid_BC[1]-0.2, "M_BC", fontsize=9, color='green')
ax.text(mid_CA[0]-0.3, mid_CA[1]+0.1, "M_CA", fontsize=9, color='green')

# ======================== Легенда снаружи ========================
handles = [
    plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
    plt.Line2D([0], [0], color='green', linestyle='--', lw=1.5, label='Серединные перпендикуляры'),
    plt.scatter([0], [0], c='lime', s=60, label='Середины сторон'),
    plt.scatter([0], [0], c='red', s=120, marker='*', label='Центр описанной окружности'),
    plt.Line2D([0], [0], color='red', lw=2, label='Описанная окружность')
]
ax.legend(handles=handles, loc='center left', bbox_to_anchor=(1, 0.5))
plt.subplots_adjust(right=0.75)

# ======================== Границы осей ========================
all_x = [A[0], B[0], C[0], circumcenter[0]]
all_y = [A[1], B[1], C[1], circumcenter[1]]
x_min, x_max = min(all_x), max(all_x)
y_min, y_max = min(all_y), max(all_y)
# Добавляем запас с учётом радиуса
margin_x = max(radius*0.4, (x_max - x_min)*0.4)
margin_y = max(radius*0.4, (y_max - y_min)*0.4)
ax.set_xlim(x_min - margin_x, x_max + margin_x)
ax.set_ylim(y_min - margin_y, y_max + margin_y)

ax.set_title('Серединные перпендикуляры и описанная окружность', fontsize=14)
ax.set_xlabel('x')
ax.set_ylabel('y')

# Сохранить (раскомментируйте)
plt.savefig('docs/pic/perpendicular_bisectors.png', dpi=150, bbox_inches='tight')

# plt.show()