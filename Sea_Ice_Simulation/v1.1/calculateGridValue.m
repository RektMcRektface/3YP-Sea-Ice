function output = calculateGridValue(nearestData)
%Function for finding individual cell values given nearestData

    %Taking out nearestData distance data
    dist = abs(cell2mat(nearestData(5)));

    %Taking dot products
    topLeft = dot(cell2mat(nearestData(1)),cell2mat(nearestData(5)));
    topRight = dot(cell2mat(nearestData(2)),cell2mat(nearestData(6)));
    botLeft = dot(cell2mat(nearestData(3)),cell2mat(nearestData(7)));
    botRight = dot(cell2mat(nearestData(4)),cell2mat(nearestData(8)));
    
    
    %Bilinear interpolation - this can be changed for more smoothness
    topInterpolation = topLeft * (1-dist(1)) + topRight * dist(1);
    botInterpolation = botLeft * (1-dist(1)) + botRight * dist(1);
    yInterpolation = topInterpolation * (1-dist(2)) + botInterpolation * dist(2);

    output = yInterpolation;