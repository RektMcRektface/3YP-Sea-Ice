% A script to find the necessary parameters for an SAR RADAR system given
% certain parameters
% Author: PH

clear; clc; close all

% Basic requirements:
% Specifications
slantrngres = 1;        % Required slant range resolution (m)
azres = 1;              % Required azimuth resolution (m)
maxrng = 5e3;          % Maximum unambiguous slant range (m)
pd = 0.9;               % Probability of detection
pfa = 1e-6;             % Probability of false alarm
v = 30;                % Velocity (m/s)
h = 1e3;               % Radar altitude (m)

% We have our frequency centred at 10 GHz, helping with ice detection
freq = 10e9;                 % Radar Frequency within X-band (Hz)
lambda = freq2wavelen(freq); % Wavelength (m)

% We can find our required pulse bandwidth with the slant range resolution
pulse_bw = rangeres2bw(slantrngres);    % Pulse bandwidth (Hz)


% We can find the graze angle, assuming that we have a flat earth
grazang = grazingang(h,maxrng,'Curved');  % Grazing angle (in degrees)

%% Azimuth dimensions

% Investigate different azimuth dimensions
dazv = [1 1.5 2 2.5 3];    % Antenna azimuth dimensions (m)
striplenv = zeros(1,numel(dazv));
stripazresv = zeros(1,numel(dazv));
for i=1:numel(dazv)
    striplenv(i) = sarlen(maxrng,lambda,dazv(i));
    stripazresv(i) = sarazres(maxrng,lambda,striplenv(i));
end

% Plot azimuth resolution vs. synthetic aperture length
subplot(1,2,1)
plot(stripazresv,striplenv)
grid on
xline(azres,'-.',{[num2str(round(azres)),' m']}); % Selected azimuth resolution
xlabel('Azimuth or Cross-range Resolution (m)')
ylabel('Synthetic Length (m)')

stripidx = find(abs(striplenv-75)<1); % Index corresponding to required azimuth resolution

% Plot synthetic aperture length vs. antenna azimuth dimensions
subplot(1,2,2)
plot(striplenv,dazv)
grid on
xline(striplenv(stripidx),'-.',{[num2str(round(striplenv(stripidx),2)),' m']}); % Selected synthetic length
xlabel('Synthetic Length (m)')
ylabel('Antenna Azimuth Dimension (m)')

% We can now set the results we found
daz = 2
striplen = 75

%% Antenna Elevation Dimensions

% Investigate different antenna elevations, using a swath range of 2.4km
rngswath = 1e3;
delv = [0.15 0.2 0.25 0.3 0.35];    % Elevation Dimensions (m)
rangeswathv = zeros(1,numel(delv));
for i=1:numel(delv)
    [rangeswathv(i),crngswath] = aperture2swath(maxrng,lambda,[delv(i) daz],grazang);
end
figure
plot(rangeswathv,delv)
grid on
xline(rngswath,'-.',{[num2str(round(rngswath,2)),' m']}); % Selected range swath
xlabel('Swath Length (m)')
ylabel('Antenna Elevation Dimension (m)')

% We can see that this gives us our antenna elevation 
del = 0.31

% We can find the real beamwidth and antenna gain
realAntBeamwidth = ap2beamwidth([daz del],lambda); % [Az El] (deg)
antGain = aperture2gain(daz*del, lambda); % dBi

%% SAR Synthetic Beamwidth, Processing Time, and Constraints

stripsynbw = sarbeamwidth(lambda,striplen); % Synthetic beamwidth (degrees)
stripinttime = sarinttime(v,striplen);      % Integration time (sec)
stripcovrate = sarmaxcovrate(azres,grazang);      % Upper bound on coverage rate (m^2/sec)
stripswlen = sarmaxswath(v,azres,grazang);        % Upper bound on swath length (m)

RealAntenna = [realAntBeamwidth(1); NaN; NaN; NaN];
Parameters = ["Synthetic Beamwidth";"Integration Time";"Upper Bound on Swath Length";...
    "Upper Bound on Area Coverage Rate"];
StripmapSAR = [stripsynbw;stripinttime;round(stripcovrate/1e6,1);round(stripswlen/1e3)];
Units = ["degrees";"sec";"km^2/sec";"km"];
sarparams = table(Parameters,RealAntenna,StripmapSAR,Units)

%% Azimuth Chirp Signal Parameters

% calculate the rate at which the azimuth signal changes frequency
azchirp = sarchirprate(maxrng,lambda,v); % (Hz/sec)

