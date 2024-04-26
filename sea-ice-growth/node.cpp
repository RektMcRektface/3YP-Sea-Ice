//
// Created by oweng on 16/04/2024.
//

#include "node.hpp"
#include <iostream>
#include <math.h>
#include "windows.h"

void Node::stepNode(dataMap * map, double dt) {
    this->setConstants(map);
    std::vector<double> thicknessChanges = calcThicknessChange(map, 3600); //3600 seconds in an hour
    this->snowfallFunc(map);
    hs = hs + thicknessChanges[0];
    hi = hi + thicknessChanges[1];
    if (hs < 0) {hs = 0;}
    if (hi <= 0) {hi = 0; hs = 0;}
}

void Node::snowfallFunc(dataMap* map) {
    int month = floor(map->getTime()/730);
    std::vector<double> snowfallData{1.14109e-5, 1.14109e-5, 1.14109e-5, 1.14109e-5, 6.8493e-5, 0, 0, 0, 0.0001760272, 0.0001760272, 6.8493e-5, 6.8493e-5};
    if (map->getTime() >= 5568 && map->getTime() <= 5808) {
        month = 8; //Set to September
    }
    hs += snowfallData[month];
}

void Node::setVectorValues(dataMap *map, double value) {
    int month = floor(map->getTime()/730);

    //Cloud cover
    ccVect[month] = value;


}

void Node::setConstants(dataMap *map) {
    int month = floor(map->getTime()/730);


    Ta = TaVect[month];
    Vw = VwVect[month];
    cc = ccVect[month];
    Td = TdVect[month];


}

double Node::getIceThickness() const {
    return hi;
}

double Node::calccosSZA(dataMap* map) {
    double pi = M_PI;
    double n = floor(map->getTime()/24);
    double LST = map->getTime()%24;
    double declination = (23.44*cos((172-n)*(pi/180)))*pi/180;
    double cosSZA = (sin(latitude*pi/180) * sin(declination)) + (cos(latitude*pi/180)*cos(declination)*cos((12-LST)*pi/12));
    return cosSZA;

}

double Node::calcVapourPressure(dataMap *map, int mode = 0, double Tsat = 0) {
    double Tref;
    if (mode == 0) {
        Tref = Td;
    }
    else {
        Tref = Tsat;
    }
    double VapourPressure;

    //If no ice cover
    if (hi == 0) {
        //std::cout << "No ice cover detected!" << std::endl;
        VapourPressure = 611 * pow(10, (7.5 * (Tref - 273.16) / (Tref - 35.86)));
    }

    //If ice cover
    else {
        //std::cout << "Ice cover deteced!" << std::endl;
        VapourPressure = 611 * pow(10, (9.5 * (Tref - 273.16) / (Tref - 7.66)));
    }

    //std::cout << "Vapour Pressure: " << VapourPressure << std::endl;
    return VapourPressure;
}

double Node::calcSWI(dataMap* map) {
    double cosSZA = calccosSZA(map);
    if (cosSZA < 0) {
        return 0;
    }
    double vapourPre = calcVapourPressure(map);
    double SWI = (map->getSolarConst()*cosSZA*cosSZA)/((cosSZA+2.7)*vapourPre*0.00001 + 1.085*cosSZA + 0.1);
    SWI = SWI * (1-(0.6*(cc*cc*cc))); //Cloud cover correction
    //std::cout << "SWI: " << SWI << std::endl;
    return SWI;
}

double Node::calcSWT(dataMap* map) {
    double albedo = calcAlbedo(map);
    double SWT;
    SWT = calcSWI(map) * (1-albedo);
    if (hs == 0 && hi != 0) { //If no snow but there is ice
        SWT = SWT*(1-0.068); //I_0, 0.17 * 0.4 = 0.068
    }

    //std::cout << "SWT: " << SWT << std::endl;

    return SWT;
}

double Node::calcLWI(dataMap* map) {
    const double sigma = 5.670374419e-8;
    double LWClear = sigma*pow(Ta,4)*(0.179*pow(calcVapourPressure(map), 1/7)*exp(350/Ta));
    //std::cout << "LWIClear: " << LWClear << std::endl;
    double LWtotal = LWClear * (1.07 + 0.34*cc);
    //std::cout<< "LWITotal: " << LWtotal << std::endl;
    return LWtotal;
}




double Node::calcAlbedo(dataMap *map) {
    double albedo;
    if (hi == 0) { //No ice
        albedo = 0.1;
    }
    else if (hs == 0) { //No snow
        albedo = 0.5;
    }
    else { //Snow
        albedo = 0.75;
    }
    return albedo;
}

double Node::calcConduction(dataMap *map, double Tsh) {
    if (hs == 0 && hi == 0) {return 0;}
    return ((ks*ki)/((ks*hi)+(ki*hs)))*(map->getTf() - Tsh);
}

double Node::calcLWO(dataMap *map, double Tsurface) {
    const double sigma = 5.670374419e-8;
    double emissivity;
    if (hi == 0) {
        emissivity = 0.97; //emissivity of water
    }
    else if (hs == 0) {
        emissivity = 0.97; //emissivity of ice
    }
    else {
        emissivity = 0.99; //emissivity of snow
    }

    return -(sigma*emissivity*pow(Tsurface, 4));

}

double Node::calcAirDensity(dataMap *map, double Ta) {
    double R = 287.052874; //Specific gas constant for dry air
    return atm/(R*Ta);
}

double Node::calcLatent(dataMap *map, double Tsh) {
    double q10;
    double q0;
    double latentHeat;
    double vapourPressure = calcVapourPressure(map, 0);
    double satVapourPressure = calcVapourPressure(map, 1, Tsh);
    q10 = (map->getEpsilon()*vapourPressure)/(atm - (1 - map->getEpsilon())*vapourPressure);
    q0 = (map->getEpsilon()*satVapourPressure)/(atm - (1 - map->getEpsilon())*satVapourPressure);
    double airDensity = calcAirDensity(map, Ta);
    //std::cout << "Air Density: " << airDensity << std::endl;

    if (hi == 0) { //If no ice cover
        latentHeat = 2.834e6;
    }
    else {
        latentHeat = 2.5e6;
    }

    double heatConstant = 1.75e-3;

    return airDensity*latentHeat*heatConstant*Vw*(q10-q0);

}

double Node::calcSensible(dataMap *map, double Tsh) {
    double airDensity = calcAirDensity(map, Ta);
    double heatTransferConst = 1004;
    double heatConstant = 1.75e-3;
    return airDensity*heatTransferConst*heatConstant*Vw*(Ta-Tsh);
}


//All defined as inwards positive
double Node::calcTotalBalance(dataMap *map, double Tsh) {
    return calcSWT(map) + calcLWI(map) + calcLWO(map, Tsh) + calcSensible(map, Tsh) + calcLatent(map, Tsh) +
            calcConduction(map, Tsh);
}

double Node::calcTshEq(dataMap* map) {
    //Newton-Raphson iterative procedure
    double TfUpper;
    if (hi == 0) { //Case for open water, can be expanded to deal with non-freezing water temperatures.
        return map->getTf();
    }
    else if (hs == 0) { //Case for no snow
        TfUpper = map->getTf();
    }
    else { //Case for ice and snow
        TfUpper = 273.15;
    }

    double guessTsh = TfUpper; //Freezing point, initial guess
    double h = 0.001;
    double guessTshdiff = guessTsh - h;
    int counter = 0;

    while (true) {
        double guessVal = calcTotalBalance(map, guessTsh);

        if (abs(guessVal) < 0.0001) {
            return guessTsh;
        }
        else {
            double guessTshdiffVal = calcTotalBalance(map, guessTshdiff);
            double guessGrad = (guessVal - guessTshdiffVal)/h;


            guessTsh = guessTsh - (guessVal/guessGrad);
            guessTshdiff = guessTsh - h;

            if (guessTsh > TfUpper) {
                return TfUpper;
            }
        }

        counter++;
        if (counter >= 1000) {
            std::cout << "Something's gone terribly wrong in the iterative procedure..." << std::endl;
            std::cout << "Time: " << map->getTime() << std::endl;

            break;
        }

    }
}

std::vector<double> Node::calcThicknessChange(dataMap* map, double dt) {
    double eqTemp = calcTshEq(map);
    double totalBalance = calcTotalBalance(map, eqTemp);
    double conductionTotal;
    std::vector<double> thicknessChange(2);
    if (totalBalance > 0.0001) {
        conductionTotal = -totalBalance;
        }
    else {
        conductionTotal = calcConduction(map, eqTemp);
        }

    if (hi == 0) { //No ice case
        thicknessChange[0] = 0;
        thicknessChange[1] = (-totalBalance/(917*334000))*dt;
        return thicknessChange;
    }

    if (hs == 0) { //No snow case
        thicknessChange[0] = 0;
        thicknessChange[1] = (conductionTotal/(917*334000))*dt;
        return thicknessChange;
    }


    else { //Snow case

        double Tih = ((ks*hi*eqTemp)+(hs*ki*map->getTf()))/((ks*hi)+(hs*ki));
        if (Tih > map->getTf()) {
            Tih = map->getTf();
        }
        //std::cout << "Tih: " << Tih << std::endl;
        if (eqTemp >= 273.15) { //Snow melt case

            double snowDelta = -(ks/hs)*(eqTemp-Tih);

            //std::cout << "Snow Delta: " << snowDelta << " Conduction Total: " << conductionTotal << std::endl;
            thicknessChange[0] = ((snowDelta)/(330*334000))*dt;
            thicknessChange[1] = ((conductionTotal - snowDelta)/(917*334000))*dt;
        }
        else { //Snow growth

            thicknessChange[0] = 0;
            thicknessChange[1] = (conductionTotal/(917*334000))*dt;

        }

        return thicknessChange;
    }

}

void Node::testNode(dataMap *map) {


    for (int loops = 0; loops < 8760; loops++) {
        this->stepNode(map, 1);

        if (loops % 100 == 0) {
            std::cout << "Acquired Ice Thickness: " << this->getIceThickness() << std::endl;
            double Tsh = this->calcTshEq(map);
            std::cout << "Acquired Snow Thickness: " << this->geths() << std::endl;
            std::cout << "Estimated Tsh balance: " << Tsh << " and freezing temperature: "
                      << map->getTf() << std::endl;
            std::cout << "SWT: " << this->calcSWT(map) << std::endl;
            std::cout << "LWI: " << this->calcLWI(map) << std::endl;
            std::cout << "Conduction: " << this->calcConduction(map, Tsh) << std::endl;
            std::cout << "Latent Heat: " << this->calcLatent(map, Tsh) << std::endl;
            std::cout << "Sensible Heat: " << this->calcSensible(map, Tsh) << std::endl;
            std::cout << "LWO: " << this->calcLWO(map, Tsh) << std::endl;
            std::cout << "Total balance: " << this->calcTotalBalance(map, Tsh) << std::endl;
            std::vector<double> thicknessChanges = this->calcThicknessChange(map, 3600);
            std::cout << "Snow thickness change: " << thicknessChanges[0] << std::endl << "Ice Thickness Change: "
                      << thicknessChanges[1] << std::endl;
            std::cout << "Node Constants, (Ta, Vw, cc, Td): " << this->getTa() << " | " << this->getVw() << " | "
                      << this->getcc() << " | " << this->getTd() << std::endl;
            std::cout << "Current month: " << floor(map->getTime() / 730) << std::endl;
            std::cout << "==============================" << std::endl;
        }


    }
}
