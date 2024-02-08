%TUTORIAL

%Setting parameters, creating grid.
gridSize = [100,100]; %Grid size refers to how big the output image is.
vectSpacing = 25; %How "spaced apart" you want the features to be. Lower
                  %values result in noiser images. Higher values result in
                  %smoother images.


grid = createGrid(gridSize, vectSpacing);
noiseMap = generateNoiseMap(gridSize,grid,vectSpacing);
noiseMap = discreteMap2(scaleMap(noiseMap));

writematrix(noiseMap, 'map.txt')

wgn = wgn(gridSize(1), gridSize(2), 1);


%imagesc(noiseMap) %Output image

