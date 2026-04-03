#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>
#include <random>
#include <string>
#include <numeric> // Для использования accumulate, если нужно
#include <omp.h>

using namespace std;

// Функция умножения с распараллеливанием
void multiply(int n, const vector<double>& A, const vector<double>& B, vector<double>& C, int num_threads) {
    omp_set_num_threads(num_threads); 
    
    // Обнуляем результирующую матрицу перед расчетом
    fill(C.begin(), C.end(), 0.0);

    #pragma omp parallel for
    for (int i = 0; i < n; i++) {
        for (int k = 0; k < n; k++) {
            double temp = A[i * n + k];
            for (int j = 0; j < n; j++) {
                C[i * n + j] += temp * B[k * n + j];
            }
        }
    }
}

int main() {
    // Параметры эксперимента
    vector<int> sizes = {200, 400, 800, 1200, 1600, 2000};
    vector<int> threads_opts = {1, 2, 4, 8, 12}; 
    const int NUM_EXPERIMENTS = 5; // Количество запусков для усреднения
    
    ofstream dataFile("data_openmp.txt");
    if (!dataFile.is_open()) {
        cerr << "Error opening file!" << endl;
        return 1;
    }

    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(1.0, 10.0);

    for (int n : sizes) {
        // Выделяем память под матрицы
        vector<double> A(n * n), B(n * n), C(n * n);
        
        // Генерируем случайные данные
        for (int i = 0; i < n * n; i++) {
            A[i] = dis(gen);
            B[i] = dis(gen);
        }

        for (int t : threads_opts) {
            cout << "Testing: N=" << n << ", Threads=" << t << " (" << NUM_EXPERIMENTS << " runs)..." << endl;
            
            double total_time = 0.0;

            // Проводим серию экспериментов
            for (int exp = 0; exp < NUM_EXPERIMENTS; exp++) {
                auto start = chrono::high_resolution_clock::now();
                multiply(n, A, B, C, t); 
                auto end = chrono::high_resolution_clock::now();

                total_time += chrono::duration<double>(end - start).count();
            }

            // Вычисляем среднее арифметическое
            double avg_time = total_time / NUM_EXPERIMENTS;
            
            // Записываем в файл: Размер | Потоки | Среднее время
            dataFile << n << " " << t << " " << avg_time << endl;
        }
        
        // Явно освобождаем память больших векторов перед следующим размером N
        A.clear(); A.shrink_to_fit();
        B.clear(); B.shrink_to_fit();
        C.clear(); C.shrink_to_fit();
    }

    dataFile.close(); // Закрываем файл корректно
    cout << "DONE! Results (averaged) saved to data_openmp.txt" << endl;
    
    return 0;
}