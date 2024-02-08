function noiseMap = generateNoiseMap(gridSize, vectGrid, vectSpacing)
%Function for generating a full noise map.

noiseMap = zeros(gridSize(1), gridSize(2));
for y = 1:gridSize(1)
    for x = 1:gridSize(2)
        nearestData = findNearest(x, y, vectGrid, vectSpacing);
        noiseMap(y,x) = calculateGridValue(nearestData);
    end
end

if min(noiseMap) < 0
    noiseMap = noiseMap + abs(min(noiseMap));
end

if min(noiseMap) > 0
    noiseMap = noiseMap - abs(min(noiseMap));
end



