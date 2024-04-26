//
// Created by oweng on 16/04/2024.
//

#ifndef ICE_SIMULATION_NEW_DATAMAP_HPP
#define ICE_SIMULATION_NEW_DATAMAP_HPP

#include <vector>
#include <iostream>

class Node;

class dataMap {
public:
    dataMap(int _time): time(_time) {std::cout << "Data map created." << std::endl;}
    void loadMap();
    void dispMap();
    void stepMap();
    double getSolarConst() {return solarConst;};
    double getTf() {return Tf;};
    double getEpsilon() {return epsilon;};
    std::vector<std::vector<Node>> getMapMatrix() {return mapMatrix;}
    double measureFunc(int mode);

    Node* getNodePtr(int row, int col);

    void mapVectorChange(double value);

    int getTime() const;
    void incrementTime() {time++; if (time > 8759) {time = 1;}};

private:
    int time; //Time in hours, 8760 hours in a year. Leap years ignored.
    double dt = 1; //One hour steps.
    double epsilon = 0.622;
    double solarConst = 1361; // W/m^2
    double Tf = 271.35; // Freezing Temp
    std::vector<std::vector<Node>> mapMatrix;
};

#endif //ICE_SIMULATION_NEW_DATAMAP_HPP
