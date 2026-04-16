import matplotlib.pyplot as plt
import numpy as np

# Создаём фигуру и оси
fig, ax = plt.subplots(figsize=(6, 6))

# Задаём пределы осей
ax.set_xlim(-0.5, 5.5)
ax.set_ylim(-0.5, 5.5)

# Рисуем оси со стрелками
ax.axhline(0, color='black', linewidth=1.5)
ax.axvline(0, color='black', linewidth=1.5)

# Добавляем стрелки на концах осей
ax.annotate('', xy=(5.3, 0), xytext=(5, 0),
            arrowprops=dict(arrowstyle='->', lw=1.5))
ax.annotate('', xy=(0, 5.3), xytext=(0, 5),
            arrowprops=dict(arrowstyle='->', lw=1.5))

# Подписи осей
ax.text(5.4, 0.1, 'x', fontsize=14, fontstyle='italic')
ax.text(0.1, 5.4, 'y', fontsize=14, fontstyle='italic')

# Подпись начала координат O
ax.text(0.1, 0.1, 'O', fontsize=14, fontstyle='italic')

# Выбираем точку P (например, x=3.5, y=2)
x_p, y_p = 3.5, 2.0

# Рисуем точку P
ax.plot(x_p, y_p, 'ro', markersize=8, label='P')
ax.text(x_p + 0.1, y_p + 0.1, 'P', fontsize=14, fontstyle='italic', color='red')

# Пунктирные линии от точки P до осей
ax.plot([x_p, x_p], [0, y_p], 'r--', linewidth=1)
ax.plot([0, x_p], [y_p, y_p], 'r--', linewidth=1)

# Подписи координат x и y
# ax.text(x_p + 0.05, -0.2, f'{x_p}', fontsize=12, ha='center')
# ax.text(-0.3, y_p + 0.05, f'{y_p}', fontsize=12, va='center')

ax.text(x_p, -0.2, 'x', fontsize=12, ha='center')
ax.text(0.05, y_p + 0.1, 'y', fontsize=12, va='center')

# Убираем рамку и деления (как на классическом чертеже)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')

# Настройка отображения делений (оставляем только основные метки)
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_yticks([1, 2, 3, 4, 5])
ax.tick_params(axis='both', which='major', labelsize=10)

# Заголовок (опционально)
ax.set_title('Рис. 1. Декартова координатная плоскость', fontsize=12)

# Показываем сетку (слабая, для удобства)
ax.grid(True, linestyle=':', alpha=0.3)

# plt.show()
plt.savefig('docs/general_proect_geom/1.png', dpi=150)