%Setting parameters, creating grid
gridSize = [100,100];
vectSpacing = 50;
vectGrid = createGrid(gridSize,vectSpacing);

%Generating noise map
noiseMap = generateNoiseMap(gridSize, vectGrid, vectSpacing);

imagesc(noiseMap);