step 1: open main_1.py

step 2: adjust parameters under the PARAMETERS, to make sure your path to danger map, starting point and destination are correct. I have calculated the ship speed based on the formula, but it doesn't have a unit yet, cuz I don't know the size scale of the danger map to real world iceberg. Can you please let me know?

step 3: adjust parameters under SHIP PATH DIJKSTRA or SHIP PATH A-STAR, there are five versions for each of the algorithm, and there are the details of them:

        version1: it only considers 4 moving directions, inclding up, down, left and right. so the simplest one
        (matrix, limit=4) , limit is the value of which vertex you do not allow path to travel through. 

        version2: it considers 8 moving directions, with diagonal directions being added to the version1
        (matrix, limit=4) , limit is the value of which vertex you do not allow path to travel through. 

        version3: it introduces a penalty in algo, so it DOES allow path to travel through vertices which has higher danger level than what we set as threshold, but with a certain penalty added. This means lower danger level vertices with no penalty is preferred but high danger vertices also allowed in case there is no valid path.
        (matrix, threshold=3, penalty=5) threshold is when penalty start to be added, it is NOT limit. 

        version4: instead of a fixed penalty value added, we vary the number, so for example if threshold is set to be 3, and a vertex with level 4 will be added with a penalty of 2, and a vertex with level 5 will be added with a penalty of 4. 
        (matrix, threshold=3, penalty_rate=2) threshold is when penalty start to be added, it is NOT limit. 
        And penalty = penalty_rate*(real_danger_level - threshold)

        version5: This is a combined method, in addtion to version4, it also include limit in algo, so it both has penalty and a restriction.
        (matrix, limit=5, threshold=3, penalty_rate=2)


step 4: after complete all steps above, run main_1.py



if only visualise ship path:
empty drone_path list before visualisation

if only visualise drone path:
empty ship_path list before visualisation

