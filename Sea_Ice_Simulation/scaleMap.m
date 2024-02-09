function mapScaled = scaleMap(map)
    %Function to scale a normalised map from values 0 -> 1
    map = map - min(min(map));
    mapScaled = map./max(max(map));

    

    