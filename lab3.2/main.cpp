#include "fix_mpi.h"
#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>
#include <random>

using namespace std;

void fill_matrix(vector<double>& mat, int n, int seed) {
    mt19937 gen(seed);
    uniform_real_distribution<> dis(1.0, 10.0);
    for (int i = 0; i < n * n; i++) {
        mat[i] = dis(gen);
    }
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int REPEATS = 3;

    vector<int> sizes = {200, 400, 800, 1200, 1600, 2000};

    // Очистка файла только при запуске на 1 процессе
    if (rank == 0 && size == 1) {
        ofstream clearFile("data_mpi.txt", ios::trunc);
        clearFile.close();
    }

    for (int n : sizes) {
        if (n % size != 0) continue;

        int rows_per_proc = n / size;
        
        vector<double> A, B(n * n), C;
        vector<double> sub_A(rows_per_proc * n), sub_C(rows_per_proc * n, 0.0);

        // Суммарное время для усреднения
        double total_time = 0.0;

        for (int repeat = 0; repeat < REPEATS; repeat++) {
            if (rank == 0) {
                A.resize(n * n);
                fill_matrix(A, n, 123 + repeat);  
                fill_matrix(B, n, 456 + repeat);
            }

            MPI_Barrier(MPI_COMM_WORLD);
            auto start = chrono::high_resolution_clock::now();

            // Рассылка данных
            MPI_Bcast(B.data(), n * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
            MPI_Scatter(A.data(), rows_per_proc * n, MPI_DOUBLE,
                        sub_A.data(), rows_per_proc * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);

            // Обнуляем sub_C перед вычислениями
            fill(sub_C.begin(), sub_C.end(), 0.0);

            // Умножение (порядок i-k-j)
            for (int i = 0; i < rows_per_proc; i++) {
                for (int k = 0; k < n; k++) {
                    double temp = sub_A[i * n + k];
                    for (int j = 0; j < n; j++) {
                        sub_C[i * n + j] += temp * B[k * n + j];
                    }
                }
            }

            // Сбор результата на процесс 0
            if (rank == 0) C.resize(n * n);
            MPI_Gather(sub_C.data(), rows_per_proc * n, MPI_DOUBLE,
                       C.data(), rows_per_proc * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);

            MPI_Barrier(MPI_COMM_WORLD);
            auto end = chrono::high_resolution_clock::now();

            // Замер времени на процессе 0
            if (rank == 0) {
                double time_spent = chrono::duration<double>(end - start).count();
                total_time += time_spent;
                cout << "  Replay " << repeat + 1 << ": " << time_spent << "s" << endl;
            }
        }

        // Запись среднего времени в файл (только на процессе 0)
        if (rank == 0) {
            double avg_time = total_time / REPEATS;
            ofstream dataFile("data_mpi.txt", ios::app);
            dataFile << n << " " << size << " " << avg_time << endl;
            cout << "N: " << n << " | Cores: " << size 
                 << " | Average time: " << avg_time << "s" << endl;
            cout << "------------------------" << endl;
        }
    }

    MPI_Finalize();
    return 0;
}