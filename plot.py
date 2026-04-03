import matplotlib.pyplot as plt
import numpy as np
import os

# Настройки стиля для отчета
plt.rcParams.update({
    'font.size': 11,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'figure.titlesize': 14,
    'legend.fontsize': 9,
    'figure.autolayout': False  # Отключаем, так как используем ручные отступы
})


def read_data(filename):
    data = {}
    if not os.path.exists(filename):
        print(f"Ошибка: Файл {filename} не найден!")
        return None
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split()
            if len(parts) < 3: continue
            try:
                n, t, val = int(parts[0]), int(parts[1]), float(parts[2])
                if n not in data: data[n] = {'t': [], 'v': []}
                data[n]['t'].append(t)
                data[n]['v'].append(val)
            except ValueError:
                continue
    return data


def create_plot(title, xlabel, ylabel):
    """Создает холст с местом под внешнюю легенду справа"""
    fig = plt.figure(figsize=(12, 6))
    # [отступ слева, снизу, ширина, высота] в долях от 1.0
    ax = fig.add_axes([0.1, 0.12, 0.65, 0.78])
    ax.set_title(title, pad=15)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return fig, ax


def save_final_plot(fig, name):
    # bbox_inches='tight' гарантирует, что внешняя легенда попадет в файл
    fig.savefig(f"{name}.png", dpi=300, bbox_inches='tight')
    print(f"Сохранено: {name}.png")
    plt.close(fig)


data = read_data('data_openmp.txt')
if data:
    sizes = sorted(data.keys())
    all_threads = sorted(list(set(t for n in data for t in data[n]['t'])))

    # 1. График: Время от потоков
    fig, ax = create_plot('Зависимость времени выполнения от количества потоков', 'Количество потоков', 'Время (сек)')
    for n in sizes:
        ax.plot(data[n]['t'], data[n]['v'], 'o-', label=f'N={n}')
    ax.legend(title='Размер матрицы', loc='upper left', bbox_to_anchor=(1.02, 1))
    save_final_plot(fig, 'time_vs_threads')

    # 2. График: Время от размера N (ТОТ САМЫЙ ГРАФИК)
    fig, ax = create_plot('Зависимость времени от размера матрицы (N)', 'Размер матрицы (N x N)', 'Время (сек)')
    for t in all_threads:
        n_vals = sorted([n for n in sizes if t in data[n]['t']])
        t_times = [data[n]['v'][data[n]['t'].index(t)] for n in n_vals]
        ax.plot(n_vals, t_times, 's-', label=f'Потоков: {t}')
    ax.legend(title='Конфигурация', loc='upper left', bbox_to_anchor=(1.02, 1))
    save_final_plot(fig, 'time_vs_size')

    # 3. График: Ускорение
    fig, ax = create_plot('Коэффициент ускорения S = T1 / Tn', 'Количество потоков', 'Ускорение (раз)')
    for n in sizes:
        threads = np.array(data[n]['t'])
        times = np.array(data[n]['v'])
        if 1 in threads:
            t1 = times[threads == 1][0]
            ax.plot(threads, t1 / times, 'o-', label=f'N={n}')
    ax.plot(all_threads, all_threads, '--', color='gray', alpha=0.5, label='Идеал (S=p)')
    ax.legend(title='Размер матрицы', loc='upper left', bbox_to_anchor=(1.02, 1))
    save_final_plot(fig, 'speedup')

    # 4. График: Эффективность (с авто-подстройкой под 150%)
    fig, ax = create_plot('Эффективность использования ресурсов E = S / n * 100%', 'Количество потоков',
                          'Эффективность (%)')
    max_eff = 110
    for n in sizes:
        threads = np.array(data[n]['t'])
        times = np.array(data[n]['v'])
        if 1 in threads:
            t1 = times[threads == 1][0]
            eff = (t1 / times / threads) * 100
            ax.plot(threads, eff, 'D-', label=f'N={n}')
            max_eff = max(max_eff, np.max(eff))

    ax.axhline(y=100, color='red', linestyle='--', alpha=0.5, label='100% Limit')
    ax.set_ylim(0, max_eff + 10)  # Динамический лимит Y
    ax.legend(title='Размер матрицы', loc='upper left', bbox_to_anchor=(1.02, 1))
    save_final_plot(fig, 'efficiency')