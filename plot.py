import matplotlib.pyplot as plt
import numpy as np

# Твои усредненные данные
n_values = np.array([200, 400, 800, 1200, 1600, 2000])
times = np.array([0.039, 0.315, 3.842, 15.222, 21.956, 71.847])
operations = 2 * n_values**3

# 1. График зависимости времени от размера
plt.figure(figsize=(8, 5))
plt.plot(n_values, times, marker='o', linestyle='-', color='b', label='Фактическое время')
plt.title('Зависимость времени выполнения от размера матрицы')
plt.xlabel('Размер матрицы N')
plt.ylabel('Время (секунды)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig('time_plot.png', dpi=300)
plt.show()

# 2. График зависимости операций от размера (Теоретический O(N^3))
plt.figure(figsize=(8, 5))
plt.plot(n_values, operations, marker='s', linestyle='-', color='r', label='Кол-во операций (2N³)')
plt.title('Зависимость количества операций от размера матрицы')
plt.xlabel('Размер матрицы N')
plt.ylabel('Количество операций')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig('ops_plot.png', dpi=300)
plt.show()