#include <iostream>
#include "node.hpp"
#include <cmath>
#include "utilities.hpp"


int main() {
    std::cout << "Hello, World!" << std::endl;

    //6570, 3650
    int timehour = 3650;
    dataMap map(timehour);
    /*dataMap map3(timehour);
    dataMap map4(timehour);
    dataMap map5(timehour);
    dataMap map6(timehour);
     */

    map.loadMap();


    /*
    map3.loadMap();
    map4.loadMap();
    map5.loadMap();
    map6.loadMap();
     */


    /*
    map3.mapVectorChange(0.25);
    map4.mapVectorChange(0.5);
    map5.mapVectorChange(0.75);
    map6.mapVectorChange(1.0);

     */

    for (int loops = 0; loops <= 730; loops++) {
        map.stepMap();
        /*
        map3.stepMap();
        map4.stepMap();
        map5.stepMap();
        map6.stepMap();

         */

        std::cout << "Looping! Time = " << loops << std::endl;
    }




    std::string fileName = "../maps4/map0VwJune.txt";
    writeMatrix(map.getMapMatrix(), fileName);
    std::cout << "Done!";




    return 0;
}


//Measuring
/*
    std::vector<double> monthlySWTVect;
    std::vector<double> monthlyLWTVect;
    std::vector<double> swtVect;
    std::vector<double> lwtVect;

    for (int loops = 0; loops <= 730; loops++) {
        map.stepMap();
        std::cout << "Still here! Loop: " << loops << std::endl;
        if (loops%2 == 0) {
            std::cout << "Measuring SWT! " << std::endl;
            monthlySWTVect.push_back(map.measureFunc(3));
            std::cout << "Measuring LWT! " << std::endl;
            monthlyLWTVect.push_back(map.measureFunc(4));
        }

        if (loops%730 == 0) {
            std::cout << "Still running!" << std::endl;
            int month = floor(map.getTime()/730) + 1;
            std::string fileName = "../maps3/map_" + std::to_string(month) + ".txt";
            writeMatrix(map.getMapMatrix(), fileName);
            swtVect.push_back(averageMatrix(monthlySWTVect));
            lwtVect.push_back(averageMatrix(monthlyLWTVect));
            monthlySWTVect.clear();
            monthlyLWTVect.clear();
            std::cout << "Calculated average SWT and LWT, and cleared vectors!" << std::endl;

        }


    }


    std::string fileName1 = "../maps3/swtMonthAvg.txt";
    writeVector(swtVect, fileName1);
    std::string fileName2 = "../maps3/lwtMonthAvg.txt";
    writeVector(lwtVect, fileName2);


 */