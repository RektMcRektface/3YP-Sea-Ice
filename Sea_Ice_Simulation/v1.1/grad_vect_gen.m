function u = grad_vect_gen()
    %Function for the generation of random gradient vector
    
    %Set RNG seed for testing, unused
    %{
    setSeed();
    rng(getSeed());
    %}
    
    %Randomise direction, generate unit vector pointing in that direction
    direction = 2*pi*rand();
    u = [cos(direction), sin(direction)];
    
    %Validate unit vector for testing, unused
    %validation = sqrt(u(1)^2 + u(2)^2);