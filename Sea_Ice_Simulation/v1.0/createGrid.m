function grid = createGrid(totalSize, vectSpacing)
    %Align with top left
    totalSize = totalSize + 1; %Number of points inbetween the grid is 1 larger than number of grids.
    grid = cell(totalSize(1), totalSize(2));
    for ypos = 1:totalSize(1)
        if mod(ypos, vectSpacing) == 1 %Slight optimisation, only looks through xpos values if ypos matches spacing condition.
            for xpos = 1:totalSize(2)
                if mod(xpos, vectSpacing) == 1
                    grid{ypos,xpos} = grad_vect_gen;
                end
            end
        end
    end

    %On second thought, this function isn't necessary. However, it does
    %help significantly with visualisation at minimal time-complexity
    %increase. Space-complexity increase is more significant, but
    %realistically vectSpacing won't be that large, so we're talking around
    %vectSpacing times more memory for storing the whole cell array as
    %opposed to the most efficient method of just compacting it into as
    %small of a space as possible.