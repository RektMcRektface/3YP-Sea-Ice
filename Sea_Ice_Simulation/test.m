topLeft = -0.1;
topRight = -0.9;
botLeft = 0;
botRight = -0.2;

dist = [1/6, 1/2];

%Bilinear interpolation - this can be changed for more smoothness
topInterpolation = topLeft * (1-dist(1)) + topRight * dist(1);
botInterpolation = botLeft * (1-dist(1)) + botRight * dist(1);
yInterpolation = topInterpolation * (1-dist(2)) + botInterpolation * dist(2);