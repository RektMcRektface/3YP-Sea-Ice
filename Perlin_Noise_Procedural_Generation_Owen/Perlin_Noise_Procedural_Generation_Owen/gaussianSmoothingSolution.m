%Setting parameters, creating grid
gridSize = [100,100];
vectSpacing = 20;
vectGridSize = [0,0];
%Gaussian smoothing
hsize = 15;
sigma = 10;

extraPadding = ceil(hsize/vectSpacing)*vectSpacing;

%Reshape vectGridSize to be a full multiple of vectSpacing
while vectGridSize(1) < gridSize(1)
    vectGridSize(1) = vectGridSize(1) + vectSpacing;
end

while vectGridSize(2) < gridSize(2)
    vectGridSize(2) = vectGridSize(2) + vectSpacing;
end


vectGrid = createGrid(vectGridSize + extraPadding,vectSpacing);

%Generating noise map
noiseMap = generateNoiseMap(gridSize + hsize*2, vectGrid, vectSpacing);

gaussKernel = fspecial('gaussian', hsize, sigma);
noiseMapFiltered = imfilter(noiseMap, gaussKernel,"replicate");

for ind = 0:hsize-1
    noiseMapFiltered(:,end-ind) = [];
    noiseMapFiltered(end-ind, :) = [];
    noiseMapFiltered(:,ind+1) = [];
    noiseMapFiltered(ind+1,:) = [];
end

imagesc(noiseMapFiltered);



