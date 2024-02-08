function mapNorm = normaliseMap(map)
    %Function to normalise a given map
    totalVal = sum(sum(map));
    mapNorm = map./totalVal;