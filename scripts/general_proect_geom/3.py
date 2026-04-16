import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-2, 5)
ax.set_ylim(-2, 5)
ax.set_aspect('equal')
# ax.axis('off')

# Начало координат
ax.plot(0, 0, 'ko', markersize=4)
ax.text(-0.2, -0.2, 'O', fontsize=12)

# Ось X1 (вправо)
ax.annotate('', xy=(4, 0), xytext=(0, 0), arrowprops=dict(arrowstyle='->', lw=1.5))
ax.text(4.1, -0.2, '$X_1$', fontsize=14)

# Ось X2 (вверх)
ax.annotate('', xy=(0, 4), xytext=(0, 0), arrowprops=dict(arrowstyle='->', lw=1.5))
ax.text(-0.3, 4.1, '$X_2$', fontsize=14)

# Ось X3 (на нас — диагонально вниз-влево, угол -135°)
angle_x3 = -135
length = 1.5
dx = length * np.cos(np.radians(angle_x3))
dy = length * np.sin(np.radians(angle_x3))
ax.annotate('', xy=(dx, dy), xytext=(0, 0), arrowprops=dict(arrowstyle='->', lw=1.5))
ax.text(dx - 0.5, dy - 0.2, '$X_3$', fontsize=14)

# Координаты точки P (можно менять)
x1, x2, x3 = 2.5, 2.0, 1.8

# Единичные векторы осей
e1 = (1, 0)
e2 = (0, 1)
e3 = (np.cos(np.radians(angle_x3)), np.sin(np.radians(angle_x3)))

# 2D-координаты точки P
Px = x1*e1[0] + x2*e2[0] + x3*e3[0]
Py = x1*e1[1] + x2*e2[1] + x3*e3[1]

# Точка P
ax.plot(Px, Py, 'ro', markersize=8)
ax.text(Px + 0.15, Py + 0.15, '$P = (X_1, X_2, X_3)$', fontsize=12, color='red')

# Линии от P к осям (проекции)
# К плоскости X1X2 (параллельно X3)

ax.plot([0, Px], [0, Py], 'gray', linestyle='dotted', linewidth=1)
ax.text(Px/2, Py/2+0.1, 'l', fontsize=12, style='italic', color='red')

# # К оси X3 (параллельно плоскости X1X2)
# proj_x3 = (x3*e3[0], x3*e3[1])
# ax.plot([Px, proj_x3[0]], [Py, proj_x3[1]], 'gray', linestyle='dotted', linewidth=1)

# # Дополнительные линии от проекций до осей (для наглядности)
# ax.plot([proj_xy[0], x1*e1[0]], [proj_xy[1], x1*e1[1]], 'gray', linestyle='dotted', linewidth=0.7)
# ax.plot([proj_xy[0], x2*e2[0]], [proj_xy[1], x2*e2[1]], 'gray', linestyle='dotted', linewidth=0.7)

plt.title('Рисунок 3.', fontsize=10)
# plt.show()
plt.savefig('docs/general_proect_geom/3.png', dpi=150)