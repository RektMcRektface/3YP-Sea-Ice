hello

compile and run, compilation configs in CMakeLists

program default directory is in c-make-debug.

reads ../map.txt, and outputs into some output directory.

input directory can be found in line 25 in dataMap.cpp
file.open("your file directory here");
output directory found in main.cpp line 54
fileName string is output directory, change to whatever you want.

at the start of main.cpp, there is a timehour variable. set this to the hour of the year (ranging from 0 - 8760). this is because sun exposure changes throughout the year, and hence changes the growth/abalation of ice.

