import matplotlib.pyplot as plt
import numpy as np
import os

def load_data(filename="data_mpi.txt"):
    """Загрузка данных из файла"""
    if not os.path.exists(filename):
        print(f"Ошибка: файл {filename} не найден!")
        return None
    
    data = np.loadtxt(filename)
    sizes = np.unique(data[:, 0]).astype(int)
    cores = np.unique(data[:, 1]).astype(int)
    
    return data, sizes, cores

def print_tables(data, sizes, cores):
    """Вывод таблиц с результатами"""
    
    print("\n" + "="*70)
    print("ТАБЛИЦА 1: Время выполнения (секунды)")
    print("="*70)
    
    # Заголовок
    header = f"{'N':>8}"
    for p in cores:
        header += f"{p:>12} proc"
    print(header)
    print("-"*70)
    
    for n in sizes:
        row = f"{n:>8}"
        for p in cores:
            val = data[(data[:, 0] == n) & (data[:, 1] == p)][0][2]
            row += f"{val:>12.5f}"
        print(row)
    
    # Таблица ускорения
    print("\n" + "="*70)
    print("ТАБЛИЦА 2: Ускорение (Speedup) — формула: S = T1 / Tp")
    print("="*70)
    
    print(f"{'N':>8}", end="")
    for p in cores:
        if p != 1:
            print(f"{p:>12} proc", end="")
    print()
    print("-"*70)
    
    for n in sizes:
        row = f"{n:>8}"
        t1 = data[(data[:, 0] == n) & (data[:, 1] == 1)][0][2]
        for p in cores:
            if p != 1:
                tp = data[(data[:, 0] == n) & (data[:, 1] == p)][0][2]
                speedup = t1 / tp
                row += f"{speedup:>12.2f}x"
        print(row)
    
    # Таблица эффективности
    print("\n" + "="*70)
    print("ТАБЛИЦА 3: Эффективность (%) — формула: E = S / p * 100%")
    print("="*70)
    
    print(f"{'N':>8}", end="")
    for p in cores:
        if p != 1:
            print(f"{p:>12} proc", end="")
    print()
    print("-"*70)
    
    for n in sizes:
        row = f"{n:>8}"
        t1 = data[(data[:, 0] == n) & (data[:, 1] == 1)][0][2]
        for p in cores:
            if p != 1:
                tp = data[(data[:, 0] == n) & (data[:, 1] == p)][0][2]
                speedup = t1 / tp
                efficiency = (speedup / p) * 100
                row += f"{efficiency:>12.1f}%"
        print(row)

def plot_graphs(data, sizes, cores):
    """Построение графиков"""
    
    # График 1: Время выполнения
    plt.figure(figsize=(10, 6))
    for p in cores:
        subset = data[data[:, 1] == p]
        subset = subset[subset[:, 0].argsort()]
        plt.plot(subset[:, 0], subset[:, 2], marker='o', linewidth=2, label=f'{p} процессов')
    
    plt.xlabel('Размер матрицы (N)', fontsize=12)
    plt.ylabel('Время выполнения (секунды)', fontsize=12)
    plt.title('Зависимость времени выполнения от размера матрицы', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('time_vs_size.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # График 2: Ускорение
    plt.figure(figsize=(10, 6))
    max_cores = max(cores)
    plt.plot([1, max_cores], [1, max_cores], 'k--', linewidth=2, label='Идеальное ускорение')
    
    for n in sizes:
        subset = data[data[:, 0] == n]
        subset = subset[subset[:, 1].argsort()]
        p_vals = subset[:, 1]
        t1 = subset[subset[:, 1] == 1][0][2]
        speedup = t1 / subset[:, 2]
        plt.plot(p_vals, speedup, marker='o', linewidth=2, label=f'N = {n}')
    
    plt.xlabel('Количество процессов', fontsize=12)
    plt.ylabel('Ускорение', fontsize=12)
    plt.title('Зависимость ускорения от количества процессов', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('speedup.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # График 3: Эффективность
    plt.figure(figsize=(10, 6))
    plt.plot([1, max_cores], [100, 100], 'k--', linewidth=2, label='100% эффективность')
    
    for n in sizes:
        subset = data[data[:, 0] == n]
        subset = subset[subset[:, 1].argsort()]
        p_vals = subset[:, 1]
        t1 = subset[subset[:, 1] == 1][0][2]
        speedup = t1 / subset[:, 2]
        efficiency = (speedup / p_vals) * 100
        plt.plot(p_vals, efficiency, marker='o', linewidth=2, label=f'N = {n}')
    
    plt.xlabel('Количество процессов', fontsize=12)
    plt.ylabel('Эффективность (%)', fontsize=12)
    plt.title('Зависимость эффективности от количества процессов', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(bottom=0)
    plt.savefig('efficiency.png', dpi=150, bbox_inches='tight')
    plt.show()

def main():
    data, sizes, cores = load_data("data_mpi.txt")
    
    if data is None:
        return
    
    print(f"\nЗагружено: {len(data)} записей")
    print(f"Размеры матриц: {sizes}")
    print(f"Количество процессов: {cores}")
    
    # Вывод таблиц
    print_tables(data, sizes, cores)
    
    # Построение графиков
    print("\n" + "="*70)
    print("ПОСТРОЕНИЕ ГРАФИКОВ")
    print("="*70)
    plot_graphs(data, sizes, cores)
    
    print("\nГотово! Сохранены файлы:")
    print("  - time_vs_size.png")
    print("  - speedup.png")
    print("  - efficiency.png")

if __name__ == "__main__":
    main()