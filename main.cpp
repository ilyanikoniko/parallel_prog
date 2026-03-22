#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>
#include <random>
#include <string>

using namespace std;

void writeFullMatrix(ofstream& f, int n, const string& label, const vector<double>& mat) {
    f << "START_" << label << " SIZE: " << n << endl;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            f << mat[i * n + j] << " ";
        }
        f << endl;
    }
    f << "END_" << label << endl;
}

void multiply(int n, const vector<double>& A, const vector<double>& B, vector<double>& C) {
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
    vector<int> sizes = {200, 400, 800, 1200, 1600, 2000};
    
    ofstream inFile("input.txt");
    ofstream resFile("result.txt");
    ofstream dataFile("data.txt");

    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(1.0, 10.0);

    for (int n : sizes) {
        for (int exp = 1; exp <= 3; exp++) {
            cout << "Running: N=" << n << ", Exp=" << exp << "..." << endl;
            
            vector<double> A(n * n), B(n * n), C(n * n, 0.0);
            for (int i = 0; i < n * n; i++) {
                A[i] = dis(gen);
                B[i] = dis(gen);
            }

            inFile << "### EXPERIMENT_START N=" << n << " EXP=" << exp << " ###" << endl;
            writeFullMatrix(inFile, n, "A", A);
            writeFullMatrix(inFile, n, "B", B);
            inFile << "### EXPERIMENT_END ###" << endl;

            auto start = chrono::high_resolution_clock::now();
            multiply(n, A, B, C); 
            auto end = chrono::high_resolution_clock::now();

            double time_spent = chrono::duration<double>(end - start).count();
            long long ops = 2LL * n * n * n; //

            resFile << "### RESULT_START N=" << n << " EXP=" << exp << " ###" << endl;
            resFile << "Time: " << time_spent << "s, Operations: " << ops << endl;
            writeFullMatrix(resFile, n, "C", C);
            resFile << "### RESULT_END ###" << endl;

            dataFile << n << " " << time_spent << " " << ops << endl;
        }
    }
    cout << "DONE! Files created: input.txt, result.txt, data.txt" << endl;
    return 0;
}