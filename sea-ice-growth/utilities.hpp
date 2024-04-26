//
// Created by oweng on 15/04/2024.
//

#ifndef ICE_SIMULATION_NEW_UTILITIES_HPP
#define ICE_SIMULATION_NEW_UTILITIES_HPP

#include <fstream>
#include <sstream>
#include <vector>
#include <windows.h>
#include <string>
#include <iostream>
#include <iomanip>
#include <cmath>

template<typename T>
void printMatrix(T matrix) {

    typename T::iterator it;
    for(it = matrix.begin(); it < matrix.end(); it++) {

        typename T::value_type row = *it;
        typename T::value_type::iterator it2;
        for(it2 = row.begin(); it2 < row.end(); it2++) {
            std::cout << *it2 << " ";
        }
        std::cout << std::endl;

    };
}

template<typename T>
void writeMatrix(T matrix, std::string fileName) {

    std::ofstream outFile(fileName);

    if (outFile.is_open()) {

        typename T::iterator it;
        for (it = matrix.begin(); it < matrix.end(); it++) {
            typename T::value_type row = *it;
            typename T::value_type::iterator it2;
            for (it2 = row.begin(); it2 < row.end(); it2++) {
                outFile << std::setprecision(15) << it2->getIceThickness() << ",";//Write value and a comma to the txt file
            }
            outFile << "\n";//Write an endl to the txt file

        }
    }

}

template<typename T>
void writeVector(T vect, std::string fileName) {

    std::ofstream outFile(fileName);

    if (outFile.is_open()) {

        typename T::iterator it;
        for (it = vect.begin(); it < vect.end(); it++) {
            outFile << std::setprecision(15) << *it << ",";//Write value and a comma to the txt file

        }
    }

}

template<typename T>
double averageMatrix(T vect) {
    typename T::iterator it;
    double sum = 0;
    double counter = 0;
    for (it = vect.begin(); it < vect.end(); it++) {
        sum += *it;
        counter++;
    }
    return (sum/counter);
}

template<typename T>
double rmsErr(T mat1, T mat2) {
    //Assert that mat1 and mat2 are of the same size.
    int columns = mat1.size();
    int rows = mat1[0].size();
    double rmsErr;
    int counter = 0;

    for (int ind = 0; ind < columns; ind++) {
        for (int ind2 = 0; ind2 < rows; ind2++) {
            std::cout << "Made it here! Calculating column " << ind << " and row " << ind2 << std::endl;
            rmsErr += pow(mat1[ind][ind2].getIceThickness(),2) - pow(mat2[ind][ind2].getIceThickness(), 2);
            counter++;
        }
    }

    rmsErr = sqrt(rmsErr);

    std::cout << "Returning " << rmsErr/counter << std::endl;

    return (rmsErr/counter);


}

#endif //ICE_SIMULATION_NEW_UTILITIES_HPP
