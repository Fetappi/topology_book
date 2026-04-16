import numpy as np
import matplotlib.pyplot as plt

# ======================== Задаём вершины треугольника ========================
A = np.array([0.0, 0.0])
B = np.array([6.0, 0.0])
C = np.array([2.0, 5.0])

# ======================== Вычисляем длины сторон ========================
a = np.linalg.norm(B - C)   # сторона напротив A
b = np.linalg.norm(A - C)   # сторона напротив B
c = np.linalg.norm(A - B)   # сторона напротив C

# ======================== Инцентр (центр вписанной окружности) ========================
# Формула: (a*A + b*B + c*C) / (a+b+c)
incenter = (a * A + b * B + c * C) / (a + b + c)

# ======================== Точки касания биссектрис с противоположными сторонами ========================
# Биссектриса из A делит BC в отношении AB:AC = c:b
t_A = c / (b + c)   # доля от B к C
point_on_BC = B + t_A * (C - B)

# Биссектриса из B делит AC в отношении BA:BC = c:a
t_B = c / (a + c)   # доля от A к C
point_on_AC = A + t_B * (C - A)

# Биссектриса из C делит AB в отношении CA:CB = b:a
t_C = b / (a + b)   # доля от A к B
point_on_AB = A + t_C * (B - A)

# ======================== Настройка графики с запасом места для легенды ========================
fig, ax = plt.subplots(figsize=(9, 6))
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.6)

# Рисуем треугольник (синий)
triangle = plt.Polygon([A, B, C], fill=None, edgecolor='blue', linewidth=2)
ax.add_patch(triangle)

# Рисуем биссектрисы (красные сплошные линии)
ax.plot([A[0], point_on_BC[0]], [A[1], point_on_BC[1]], 'red', linewidth=1.5, label='Биссектрисы')
ax.plot([B[0], point_on_AC[0]], [B[1], point_on_AC[1]], 'red', linewidth=1.5)
ax.plot([C[0], point_on_AB[0]], [C[1], point_on_AB[1]], 'red', linewidth=1.5)

# Отмечаем инцентр (зелёная звезда)
ax.scatter(*incenter, color='green', s=120, marker='*', zorder=6, label='Инцентр (пересечение биссектрис)')

# Подписываем вершины
ax.text(A[0]-0.3, A[1]-0.3, 'A', fontsize=12, fontweight='bold')
ax.text(B[0]+0.1, B[1]-0.3, 'B', fontsize=12, fontweight='bold')
ax.text(C[0]-0.2, C[1]+0.2, 'C', fontsize=12, fontweight='bold')

# ======================== Легенда снаружи справа ========================
handles = [
    plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
    plt.Line2D([0], [0], color='red', lw=1.5, label='Биссектрисы'),
    plt.scatter([0], [0], c='green', s=120, marker='*', label='Инцентр')
]
ax.legend(handles=handles, loc='center left', bbox_to_anchor=(1, 0.5))
plt.subplots_adjust(right=0.75)   # освободить место справа

# ======================== Границы осей с отступом ========================
all_x = [A[0], B[0], C[0], incenter[0]]
all_y = [A[1], B[1], C[1], incenter[1]]
x_min, x_max = min(all_x), max(all_x)
y_min, y_max = min(all_y), max(all_y)
dx = (x_max - x_min) * 0.2
dy = (y_max - y_min) * 0.2
ax.set_xlim(x_min - dx, x_max + dx)
ax.set_ylim(y_min - dy, y_max + dy)

ax.set_title('Биссектрисы треугольника и инцентр', fontsize=14)
ax.set_xlabel('x')
ax.set_ylabel('y')

# Сохранить картинку (раскомментируйте при необходимости)
plt.savefig('docs/pic/bisectors_triangle.png', dpi=150, bbox_inches='tight')

# plt.show()