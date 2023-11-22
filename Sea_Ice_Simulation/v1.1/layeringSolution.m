%Setting parameters, creating grid
gridSize = [100,100];
vectSpacing = 20;
vectGridSize = [0,0];
layers = 3;
noiseMapTotal = zeros(gridSize(1), gridSize(2));

%Reshape vectGridSize to be a full multiple of vectSpacing
while vectGridSize(1) < gridSize(1)
    vectGridSize(1) = vectGridSize(1) + vectSpacing;
end

while vectGridSize(2) < gridSize(2)
    vectGridSize(2) = vectGridSize(2) + vectSpacing;
end


vectGrid = createGrid(vectGridSize*layers,vectSpacing);

%Generating noise map
for ind = 1:layers
    noiseMap = generateNoiseMap(gridSize, vectGrid, vectSpacing*2^(layers-1));
    noiseMapTotal = noiseMapTotal + noiseMap;
end

imagesc(noiseMapTotal);
