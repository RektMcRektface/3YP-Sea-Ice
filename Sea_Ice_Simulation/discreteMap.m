function mapDiscrete = discreteMap(map)
    %Discretisises map into preset classifiers (changeable params). Map
    %must be normalised, then scaled.

    %Test 1: constant map scaling. Probably won't look great - assumes
    %natural perlin generation will match real life terrain generation.
    
    c1 = 0.45;
    c2 = 0.5;
    c3 = 0.55;
    c4 = 0.6;
    c5 = 0.7;
    c6 = 0.75;
    c7 = 0.8;

    map(map <= c1) = 0;
    map((map > c1) & (map <= c2)) = 0.15;
    map((map > c2) & (map <= c3)) = 0.3;
    map((map > c3) & (map <= c4)) = 0.5;
    map((map > c4) & (map <= c5)) = 0.7;
    map((map > c5) & (map <= c6)) = 0.8;
    map((map > c6) & (map <= c7)) = 0.9;
    map((map > c7) & (map <= 1)) = 0.95;

    mapDiscrete = map;