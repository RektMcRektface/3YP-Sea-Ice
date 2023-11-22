function output = findNearest(xPos, yPos, vectGrid, vectSpacing)
%Function to find the nearest grid vector given an xPos and a yPos
%Technically vectSpacing isn't required, but it saves some calculation.
%Output in terms of {[xMagnitude, yMagnitude], ... , [xDistLeft, xDistRight, yDistTop, yDistBot]}
%{Top left, top right, bottom left, bottom right, distances}

    %Calculation of relative x and y positions relative to nearest vectors.
    xPosRelative = mod(xPos, vectSpacing);
    if xPosRelative == 0
        xPosRelative = vectSpacing;
    end
    yPosRelative = mod(yPos, vectSpacing);
    if yPosRelative == 0
        yPosRelative = vectSpacing;
    end

    %Calculation of distances
    xDistLeft = (2 * xPosRelative - 1) / (vectSpacing * 2);
    xDistRight = 1 - xDistLeft;
    yDistTop = (2 * yPosRelative - 1) / (vectSpacing * 2);
    yDistBot = 1 - yDistTop;

    %Find the nearest vectors (Top left)
    xPosVect = (floor((xPos-1)/vectSpacing)*vectSpacing)+1;
    yPosVect = (floor((yPos-1)/vectSpacing)*vectSpacing)+1;

    vectTopLeft = cell2mat(vectGrid(yPosVect, xPosVect));
    vectTopRight = cell2mat(vectGrid(yPosVect, xPosVect + vectSpacing));
    vectBotLeft = cell2mat(vectGrid(yPosVect + vectSpacing, xPosVect));
    vectBotRight = cell2mat(vectGrid(yPosVect + vectSpacing, xPosVect + vectSpacing));
    
    %Output, negative signs to account for direction
    output = {vectTopLeft, vectTopRight, vectBotLeft, vectBotRight, [xDistLeft, -yDistTop], [-xDistRight, -yDistTop], [xDistLeft, yDistBot], [-xDistRight, yDistBot]};

%Formula for distance to nearest vector given relative x and y:
%(2 * xPosRelative - 1) / (vectSpacing * 2) = x Direction
%Similar for y
%Then calculate appropriate magnitudes.

