import numpy as np
import matplotlib.pyplot as plt

A = np.array([0.0, 0.0])
B = np.array([6.0, 0.0])
C = np.array([2.0, 5.0])

mid_AB = (A + B) / 2
mid_BC = (B + C) / 2
mid_CA = (C + A) / 2
centroid = (A + B + C) / 3

fig, ax = plt.subplots(figsize=(9, 6))   # шире
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.6)

# Треугольник
ax.add_patch(plt.Polygon([A, B, C], fill=None, edgecolor='blue', lw=2))

# Медианы
ax.plot([A[0], mid_BC[0]], [A[1], mid_BC[1]], 'r--', lw=1.5)
ax.plot([B[0], mid_CA[0]], [B[1], mid_CA[1]], 'r--', lw=1.5)
ax.plot([C[0], mid_AB[0]], [C[1], mid_AB[1]], 'r--', lw=1.5)

# Точки
ax.scatter(*mid_AB, color='green', s=60, zorder=5)
ax.scatter(*mid_BC, color='green', s=60, zorder=5)
ax.scatter(*mid_CA, color='green', s=60, zorder=5)
ax.scatter(*centroid, color='orange', s=120, marker='*', zorder=6)

# Подписи вершин
ax.text(A[0]-0.3, A[1]-0.3, 'A', fontsize=12, fontweight='bold')
ax.text(B[0]+0.1, B[1]-0.3, 'B', fontsize=12, fontweight='bold')
ax.text(C[0]-0.2, C[1]+0.2, 'C', fontsize=12, fontweight='bold')

# Легенда — снаружи справа
ax.legend(
    handles=[
        plt.Line2D([0], [0], color='blue', lw=2, label='Треугольник'),
        plt.Line2D([0], [0], color='red', linestyle='--', lw=1.5, label='Медианы'),
        plt.scatter([0], [0], c='green', s=60, label='Середины сторон'),
        plt.scatter([0], [0], c='orange', s=120, marker='*', label='Центроид')
    ],
    loc='center left',
    bbox_to_anchor=(1, 0.5)
)

# Освободить место справа под легенду
plt.subplots_adjust(right=0.75)

# Границы осей (как раньше)
all_x = [A[0], B[0], C[0], centroid[0]]
all_y = [A[1], B[1], C[1], centroid[1]]
x_min, x_max = min(all_x), max(all_x)
y_min, y_max = min(all_y), max(all_y)
dx = (x_max - x_min) * 0.2
dy = (y_max - y_min) * 0.2
ax.set_xlim(x_min - dx, x_max + dx)
ax.set_ylim(y_min - dy, y_max + dy)

ax.set_title('Медианы треугольника и центроид', fontsize=14)
ax.set_xlabel('x')
ax.set_ylabel('y')

plt.savefig('docs/pic/medians_triangle.png', dpi=150, bbox_inches='tight')
# plt.show()