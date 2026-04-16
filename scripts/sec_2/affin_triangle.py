import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ==========================================
# Исходный треугольник (ABC)
# ==========================================
A = np.array([0.0, 0.0])
B = np.array([4.0, 0.0])
C = np.array([1.0, 3.0])

# ==========================================
# Целевой треугольник (A'B'C')
# ==========================================
A_prime = np.array([2.0, 1.0])
B_prime = np.array([5.0, 2.0])
C_prime = np.array([3.0, 5.0])

# ==========================================
# Подготовка данных для линейного преобразования
# ==========================================
# Векторы исходного треугольника (от A)
v_B = B - A
v_C = C - A
# Векторы целевого треугольника (от A')
w_B = B_prime - A_prime
w_C = C_prime - A_prime

# Матрица линейного преобразования M: [w_B w_C] = M * [v_B v_C]
V = np.column_stack((v_B, v_C))
W = np.column_stack((w_B, w_C))
M = W @ np.linalg.inv(V)   # матрица 2×2

# ==========================================
# Функции для двух этапов
# ==========================================
def translate(t):
    """Параллельный перенос: t=0 → исходный, t=1 → вершина A в A'"""
    shift = t * (A_prime - A)
    return A + shift, B + shift, C + shift

def deform(t):
    """Линейное преобразование (после переноса): t=0 → без изменений, t=1 → целевые векторы"""
    # Интерполяция матрицы: M(t) = (1-t)*I + t*M
    I = np.eye(2)
    Mt = (1 - t) * I + t * M
    # Применяем к векторам, фиксируя A'
    B_new = A_prime + Mt @ v_B
    C_new = A_prime + Mt @ v_C
    return A_prime, B_new, C_new

# ==========================================
# Настройка графика
# ==========================================
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.6)

# Границы осей (с запасом)
all_points = np.vstack([A, B, C, A_prime, B_prime, C_prime])
x_min, x_max = all_points[:, 0].min(), all_points[:, 0].max()
y_min, y_max = all_points[:, 1].min(), all_points[:, 1].max()
dx = (x_max - x_min) * 0.2
dy = (y_max - y_min) * 0.2
ax.set_xlim(x_min - dx, x_max + dx)
ax.set_ylim(y_min - dy, y_max + dy)

# Элементы анимации
triangle = plt.Polygon(np.empty((0, 2)), fill=None, edgecolor='blue', linewidth=2, label='Текущий треугольник')
ax.add_patch(triangle)

# Статические вспомогательные треугольники (пунктир)
init_tri = plt.Polygon([A, B, C], fill=None, edgecolor='gray', linestyle=':', linewidth=1.5, label='Исходный')
final_tri = plt.Polygon([A_prime, B_prime, C_prime], fill=None, edgecolor='red', linestyle=':', linewidth=1.5, label='Целевой')
ax.add_patch(init_tri)
ax.add_patch(final_tri)

# Подписи вершин
ax.text(A[0]-0.2, A[1]-0.2, 'A', fontsize=10, color='gray')
ax.text(B[0]+0.1, B[1]-0.2, 'B', fontsize=10, color='gray')
ax.text(C[0]-0.1, C[1]+0.1, 'C', fontsize=10, color='gray')
ax.text(A_prime[0]-0.2, A_prime[1]-0.2, "A'", fontsize=10, color='red')
ax.text(B_prime[0]+0.1, B_prime[1]-0.2, "B'", fontsize=10, color='red')
ax.text(C_prime[0]-0.1, C_prime[1]+0.1, "C'", fontsize=10, color='red')

ax.legend(loc='upper left')
ax.set_title('Этап 1: Параллельный перенос')

# ==========================================
# Анимация: 200 кадров (100 перенос, 100 деформация)
# ==========================================
def init_anim():
    triangle.set_xy(np.empty((0, 2)))
    return triangle,

def update(frame):
    if frame < 100:
        t = frame / 100.0
        A_t, B_t, C_t = translate(t)
        ax.set_title(f'Этап 1: Параллельный перенос (A → A\') t = {t:.2f}')
    else:
        t = (frame - 100) / 100.0
        A_t, B_t, C_t = deform(t)
        ax.set_title(f'Этап 2: Линейное преобразование (фиксируем A\') t = {t:.2f}')
    triangle.set_xy([A_t, B_t, C_t])
    return triangle,

ani = FuncAnimation(fig, update, frames=200, init_func=init_anim,
                    interval=50, blit=False, repeat=False)

# plt.show()

# Сохранить в GIF (раскомментируйте при необходимости)
ani.save('docs/pic/affine_two_steps.gif', writer='pillow', fps=20)