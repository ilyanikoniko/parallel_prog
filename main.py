import numpy as np
import matplotlib.pyplot as plt
import os


def analyze():
    if not os.path.exists("data_openmp.txt"):
        print("Error: data_openmp.txt not found!")
        return

    # Загружаем данные: [Размер, Потоки, Время]
    data = np.loadtxt("data_openmp.txt")
    sizes = np.unique(data[:, 0])
    threads = np.unique(data[:, 1])

    plt.figure(figsize=(10, 6))

    for n in sizes:
        # Фильтруем данные для конкретного размера матрицы
        subset = data[data[:, 0] == n]
        subset = subset[subset[:, 1].argsort()]  # Сортируем по потокам

        t1 = subset[subset[:, 1] == 1][0, 2]  # Время на 1 потоке
        speedup = t1 / subset[:, 2]  # Ускорение S = T1 / Tn

        plt.plot(subset[:, 1], speedup, marker='o', label=f'Size {int(n)}x{int(n)}')

    # Линия идеального ускорения (S = n)
    plt.plot(threads, threads, 'k--', label='Ideal Speedup', alpha=0.5)

    plt.title('OpenMP Speedup Analysis')
    plt.xlabel('Number of Threads')
    plt.ylabel('Speedup (T1 / Tn)')
    plt.legend()
    plt.grid(True, ls='--')
    plt.savefig('speedup_results.png')
    print("Analysis complete. Chart saved as speedup_results.png")
    plt.show()


if __name__ == "__main__":
    analyze()