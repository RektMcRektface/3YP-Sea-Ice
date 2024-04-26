//
// Created by oweng on 15/04/2024.
//

#ifndef ICE_SIMULATION_NEW_NODE_HPP
#define ICE_SIMULATION_NEW_NODE_HPP

#include "dataMap.hpp"
#include <ostream>

class Node {
public:
    Node(double _hs, double _hi, double _latitude, int _age = 0) : hs(_hs), hi(_hi), latitude(_latitude), age(_age) {
        TaVect = {241.15, 237.65, 248.55, 254.25, 266.15, 276.15, 280.55, 280.55, 274.85, 267.65, 259.55, 252.75};
        VwVect = {1.25, 1.11, 1.06, 0.97, 4.17, 0, 3.81, 3.97, 4.14, 3.916667, 3.75, 4.22};
        ccVect = {0.375, 0.4375, 0.4375, 0.45, 0.6625, 0.725, 0.4875, 0.775, 0.675, 0.7375, 0.6125, 0.425};
        TdVect = {237.06, 233.16, 245.06, 251.36, 263.66, 271.75, 274.86, 276.76, 270.75, 264.65, 256.15, 248.95};}

    //Step method
    void stepNode(dataMap * map, double dt);

    //Variable fetchers
    double getIceThickness() const;
    void setConstants(dataMap* map);
    double getTa() {return Ta;}
    double getTd() {return Td;}
    double getVw() {return Vw;}
    double getcc() {return cc;}
    double geths() {return hs;}

    //Snowfall
    void snowfallFunc(dataMap* map);

    //Thermo functions
    double calccosSZA(dataMap* map);
    double calcAlbedo(dataMap* map);
    double calcSWI(dataMap* map);
    double calcSWT(dataMap* map);
    double calcVapourPressure(dataMap* map, int mode, double Tsat);
    double calcLWI(dataMap* map);
    double calcLWO(dataMap* map, double Tsh);
    double calcLatent(dataMap* map, double Tsh);
    double calcConduction(dataMap* map, double Tsh);
    double calcSensible(dataMap* map, double Tsh);
    double calcAirDensity(dataMap* map, double Tsh);

    double calcTotalBalance(dataMap* map, double Tsh);
    double calcTshEq(dataMap* map);

    std::vector<double> calcThicknessChange(dataMap* map, double dt);


    //Constant manipulation
    void setVectorValues(dataMap *map, double value);
    //Debugging
    void testNode(dataMap* map);




private:
    double hs;
    double hi;
    double Ta;
    double Vw;
    double cc;
    double Td = 264.45;
    double ki = 2.04;
    double ks = 0.31;
    double atm = 101325;
    int age;
    std::vector<double> TaVect;
    std::vector<double> VwVect;
    std::vector<double> ccVect;
    std::vector<double> TdVect;

    double latitude;


};



#endif //ICE_SIMULATION_NEW_NODE_HPP
