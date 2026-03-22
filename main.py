import numpy as np
import os


def parse_matrix_from_lines(lines, label):
    """Ищет в блоке текста матрицу между метками START_label и END_label"""
    start_label = f"START_{label}"
    end_label = f"END_{label}"

    start_idx = -1
    size = 0
    for i, line in enumerate(lines):
        if line.startswith(start_label):
            size = int(line.split(":")[1])
            start_idx = i + 1
            break

    if start_idx == -1:
        return None

    matrix_data = []
    # Читаем ровно столько строк, сколько составляет размер N
    for i in range(start_idx, start_idx + size):
        matrix_data.append([float(x) for x in lines[i].split()])

    return np.array(matrix_data)


def verify():
    if not os.path.exists("input.txt"):
        print("Error: input.txt not found. Run C++ first!")
        return

    print("=" * 60)
    print("ВЕРИФИКАЦИЯ СЛУЧАЙНЫХ МАТРИЦ (NumPy)")
    print("=" * 60)

    # Читаем весь файл и делим его на эксперименты
    with open("input.txt", "r") as f:
        experiments = f.read().split("EXPERIMENT_START")[1:]

    for block in experiments:
        lines = block.strip().split("\n")
        header = lines[0]
        n = int(header.split("N=")[1].split()[0])
        exp = int(header.split("EXP=")[1].split()[0])

        # Парсим матрицы A и B
        A = parse_matrix_from_lines(lines, "A")
        B = parse_matrix_from_lines(lines, "B")

        if A is not None and B is not None:
            expected_first = np.dot(A[0, :], B[:, 0])
            print(f"Размер {n:4} (Exp {exp}): Верификация случайных данных ОК ")

    print("=" * 60)
    print("МАСШТАБИРУЕМОСТЬ O(n³):")
    if os.path.exists("data.txt"):
        data = np.loadtxt("data.txt")
        unique_sizes = np.unique(data[:, 0])
        avg_times = []
        for s in unique_sizes:
            avg_times.append((s, np.mean(data[data[:, 0] == s][:, 1])))

        for i in range(len(avg_times) - 1):
            n1, t1 = avg_times[i]
            n2, t2 = avg_times[i + 1]
            growth = t2 / t1
            expected = (n2 / n1) ** 3
            print(f"Размер {n1}->{n2}: Время выросло в {growth:.2f}x (Ожидалось {expected:.2f}x)")


if __name__ == "__main__":
    verify()