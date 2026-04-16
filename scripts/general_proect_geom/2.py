import matplotlib.pyplot as plt

# Определяем линии (каждая линия — список кортежей (x, y))
# Исправлены очевидные опечатки в координатах (например, -7.99.0 → -7.99, 0)

points = {
    'Q': (-8.0, -4.1),
    'P': (-7.97, 7.88),
    'S': (7.63, 7.88),
    'R': (7.63, -4.1)
}

lines = [
    # линия 1 (сплошная)
    [points['Q'], points['P']],
    # линия 2 (сплошная)
    [points['Q'],  points['R']],
    # линия 3 (пунктир)
    [points['Q'], points['S']],
    # линия 4 (сплошная)
    [points['P'], points['S']],
    # линия 5 (пунктир)
    [points['P'],  points['R']],
    # линия 6 (сплошная)
    [points['S'], points['R']],
    # линия 7 — дубль линии 6 (игнорируем, но можно нарисовать ещё раз — не повредит)
    [points['S'],  points['R']]
]

# Типы линий: сплошные '-' и пунктирные '--'
line_styles = ['-', '-', '--', '-', '--', '-', '-']

# Точки с подписями
points = {
    'Q': (-8.0, -4.1),
    'P': (-7.97, 7.88),
    'S': (7.63, 7.88),
    'R': (7.63, -4.1)
}

# Создаём рисунок
plt.figure(figsize=(8, 6))

# Рисуем линии
for pts, style in zip(lines, line_styles):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    plt.plot(xs, ys, color='black', linestyle=style, linewidth=1.5)

# Рисуем точки и подписи
for name, (x, y) in points.items():
    plt.plot(x, y, 'ro', markersize=6)   # красные точки
    plt.text(x + 0.1, y + 0.1, name, fontsize=12, fontweight='bold', va='bottom')

# Настройка отображения
plt.axis('equal')           # одинаковый масштаб по осям
plt.grid(True, linestyle=':', alpha=0.5)
plt.title('рисунок 2.', fontsize=14)

# Показать
# plt.show()
plt.savefig('docs/general_proect_geom/2.png', dpi=150)
