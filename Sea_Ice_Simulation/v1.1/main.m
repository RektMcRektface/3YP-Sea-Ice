%Setting parameters, creating grid
gridSize = [100,100];
vectSpacing = 30;
%Gaussian smoothing parameters
hsize = 15;
sigma = 10;

noiseMap = gaussNoiseMap(gridSize,vectSpacing,hsize,sigma);

imagesc(noiseMap);
