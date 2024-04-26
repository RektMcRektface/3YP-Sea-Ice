//
// Created by oweng on 16/04/2024.
//

#include "dataMap.hpp"
#include "node.hpp"
#include "utilities.hpp"
#include <fstream>
#include <string>
#include <iostream>
#include <iomanip>
#include <sstream>

int dataMap::getTime() const {
    return time;
}

void dataMap::loadMap() {
    //Assumed variables for simulation purposes, may require further detection.

    double snowCover = 0.10; //10 cm snow
    double latitude = 73.04; //Taken from data

    std::ifstream file;
    file.open("../map.txt");
    if (file.is_open()) {

        std::string line;

        while (std::getline(file, line)) {

            std::istringstream ss(line);
            std::vector<Node> row;

            while (ss) {
                std::string temp;
                if (!getline(ss, temp, ',')) break;
                if (std::stod(temp) < 0) {
                    row.emplace_back(0, 0, latitude);
                }
                else {row.emplace_back(snowCover, std::stod(temp), latitude);}
            }
            mapMatrix.push_back(row);

        }
    }

}

void dataMap::dispMap() {
    for (std::vector<std::vector<Node>>::iterator it1 = mapMatrix.begin(); it1 < mapMatrix.end(); it1++) {
        for (std::vector<Node>::iterator it2 = it1->begin(); it2 < it1->end(); it2++) {
            std::cout << it2->getIceThickness() << " ";
        }
        std::cout << std::endl;
    }
}


Node* dataMap::getNodePtr(int row, int col) {
    Node *nodePtr = &mapMatrix[row][col];
    return nodePtr;
}

void dataMap::stepMap() {
    for (std::vector<std::vector<Node>>::iterator it1 = mapMatrix.begin(); it1 < mapMatrix.end(); it1++) {
        for (std::vector<Node>::iterator it2 = it1->begin(); it2 < it1->end(); it2++) {
            it2->stepNode(this, 1);
        }
    }

    this->incrementTime();
}

double dataMap::measureFunc(int mode) {

    double returnVal;
    int counter = 0;
    for (std::vector<std::vector<Node>>::iterator it1 = mapMatrix.begin(); it1 < mapMatrix.end(); it1++) {
        for (std::vector<Node>::iterator it2 = it1->begin(); it2 < it1->end(); it2++) {
            if (mode == 0) { //Measuring SWIavg.
                returnVal += it2->calcSWI(this);
                counter++;
            }
            if (mode == 1) { //Measuring LWTavg
                returnVal += (it2->calcLWI(this));
                counter++;
            }
            if (mode == 2) { //Measuring ice thickness
                returnVal += it2->getIceThickness();
                counter++;
            }
            if (mode == 3) { //Measuring SWT.
                returnVal += it2->calcSWT(this);
                counter++;
            }
            if (mode == 4) { //Measuring LWT.
                returnVal += (it2->calcLWI(this) + it2->calcLWO(this, it2->calcTshEq(this)));
                counter++;
            }

        }
    }

    return (returnVal/counter);

}

void dataMap::mapVectorChange(double value) {
    std::vector<std::vector<Node>>::iterator it;
    for(it = mapMatrix.begin(); it < mapMatrix.end(); it++) {

        std::vector<Node> row = *it;
        std::vector<Node>::iterator it2;
        for(it2 = row.begin(); it2 < row.end(); it2++) {
            it2->getcc();
            it2->setVectorValues(this, value);
        }

    };
}