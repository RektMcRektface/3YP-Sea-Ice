% A script to model a moving sea surface and simulate RADAR returns from it
% Author: PH
% Based on example 'Simulating Radar Returns from Moving Sea Surfaces' by
% mathworks

clear; clc; close all

rng(2021)
%% Set up parameters

% Radar parameters
freq = 9.39e9;  % Center frequency (Hz)
prf = 500;      % PRF (Hz)
tpd = 100e-6;   % Pulse width (s)
azBw = 2;       % Azimuth beamwidth (deg)
depang = 30;    % Depression angle (deg)
antGain = 45.7; % Antenna gain (dB)
fs = 10e6;      % Sampling frequency (Hz)
bw = 5e6;       % Waveform bandwidth (Hz)
bw2rangeres(bw)

% Sea surface
seaState = 4;   % Sea state number 
vw = 19;        % Wind speed (knots)
L = 512;        % Sea surface length (m) 
resSurface = 2; % Resolution of sea surface (m)

% Calculate wavelength and get speed of light
[lambda,c] = freq2wavelen(freq);

% Setup sensor trajectory and simulation times
rdrht = 100;                                   % Radar platform height (m) 
rdrpos = [-L/2 0 rdrht];                       % Radar position [x y z] (m)
numPulses = 1024;                              % Number of pulses 
scenarioUpdateTime = 1/prf;                    % Scenario update time (sec) 
scenarioUpdateRate = prf;                      % Scenario update rate (Hz)
simTime = scenarioUpdateTime.*(numPulses - 1); % Overall simulation time (sec) 

%% Set up scenario and ocean model

% Create scenario
scene = radarScenario('UpdateRate',scenarioUpdateRate, ...
    'IsEarthCentered',false,'StopTime',simTime);

% Define Elfouhaily sea spectrum 
seaSpec = seaSpectrum('Resolution',resSurface); % See Elfouhaily reference

% Define reflectivity model
pol = 'V'; % Polarization 
reflectModel = surfaceReflectivity('Sea','Model','GIT','SeaState',seaState,'Polarization',pol);

% Configure sea surface
knots2mps = 0.514444; % Knots to meters/sec
vw = vw*knots2mps; % Wind speed (m/s)
seaSurf = seaSurface(scene,'SpectralModel',seaSpec,'RadarReflectivity',reflectModel, ...
    'WindSpeed',vw,'WindDirection',0,'Boundary',[-L/2 L/2; -L/2 L/2]);

%% Plot sea surface, wave height estimation, and movement visualisation

% Plot sea surface and radar 
x = -L/2:resSurface:(L/2 - 1); 
y = -L/2:resSurface:(L/2 - 1); 
[xGrid,yGrid] = meshgrid(x,y);
z = height(seaSurf,[xGrid(:).'; yGrid(:).'],scene.SimulationTime); 
helperSeaSurfacePlot(x,y,z,rdrpos)

% Significant wave height
actSigHgt = helperEstimateSignificantWaveHeight(x,y,z);

expectedSigHgt = [1.25 2.5]; % Sea state 4
actSigHgt >= expectedSigHgt(1) && actSigHgt <= expectedSigHgt(2)

% Plot sea surface motion
plotTime = 0:0.5:10; % Plot time (sec)
helperSeaSurfaceMotionPlot(x,y,seaSurf,plotTime);

%% Set up RADAR

% Create a radar platform using the trajectory information
rdrplat = platform(scene,'Position',rdrpos);

% Create a radar sensor looking to the East
rdr = radarTransceiver('MountingAngles',[0 depang 0],'NumRepetitions',1);

% Configure the LFM signal of the radar
rdr.Waveform = phased.LinearFMWaveform('SampleRate',fs,'PulseWidth',tpd, ...
    'PRF',prf,'SweepBandwidth',bw);

% Set receiver sample rate and noise figure
rdr.Receiver.SampleRate = fs;
rdr.Receiver.NoiseFigure = 10; 

% Define transmit and receive antenna and corresponding parameters
ant = phased.SincAntennaElement('Beamwidth',azBw);
rdr.TransmitAntenna.OperatingFrequency = freq;
rdr.ReceiveAntenna.OperatingFrequency = freq;
rdr.Transmitter.Gain = antGain;
rdr.Receiver.Gain = antGain;
rdr.TransmitAntenna.Sensor = ant;
rdr.ReceiveAntenna.Sensor = ant;

% Add radar to radar platform
rdrplat.Sensors = rdr;

% Collect clutter returns with the clutterGenerator
clutterGenerator(scene,rdr); 

%% Run RADAR return simulationz

% Run the scenario
numSamples = 1/prf*fs;
maxRange = 20e3; 
Trng = (0:1/fs:(numSamples-1)/fs);
rngGrid = [0 time2range(Trng(2:end),c)];
[~,idxTruncate] = min(abs(rngGrid - maxRange));
iqsig = zeros(idxTruncate,numPulses);
ii = 1; 
hRaw = helperPlotRawIQ(iqsig);
while advance(scene)
    tmp = receive(scene); % nsamp x 1
    iqsig(:,ii) = tmp{1}(1:idxTruncate); 
    if mod(ii,128) == 0
        helperUpdatePlotRawIQ(hRaw,iqsig);
    end
    ii = ii + 1;
end
helperUpdatePlotRawIQ(hRaw,iqsig);

% Pulse compress
matchingCoeff = getMatchedFilter(rdr.Waveform);
rngresp = phased.RangeResponse('RangeMethod', 'Matched filter', ...
    'PropagationSpeed',c,'SampleRate',fs);
[pcResp,rngGrid] = rngresp(iqsig,matchingCoeff); 

% Plot
pcsigMagdB = mag2db(abs(pcResp));
[maxVal,maxIdx] = max(pcsigMagdB(:));
pcsigMagdB = pcsigMagdB - maxVal;
helperRangeTimePlot(rngGrid,prf,pcsigMagdB);

% Plot magnitude versus time
[idxRange,~] = ind2sub(size(pcsigMagdB),maxIdx); 
helperMagTimePlot(pcsigMagdB(idxRange,:),numPulses,prf,rngGrid(idxRange));

%% Analysis of data 

% STFT
[S,F,T] = stft(pcResp(idxRange,:),scenarioUpdateRate);
helperSTFTPlot(S,F,T,lambda,rngGrid(idxRange));

% Look at a subset of data in range and convert to decibel scale
[~,idxMin] = min(abs(rngGrid - 180)); 
[~,idxMax] = min(abs(rngGrid - 210)); 
pcsigMagdB = mag2db(abs(pcResp(idxMin:idxMax,:)));

% Remove any inf values
pcsigMagdB(isinf(pcsigMagdB(:))) = []; 

% Shift values to be positive
pcsigMagdB = pcsigMagdB(:) - min(pcsigMagdB(:)) + eps; 

% Weibull parameters
% Note: These values can be obtained if you use fitdist(pcsigMagdB,'weibull')
scale = 32.5013;
shape = 6.3313;

% Plot histogram with theoretical PDF overlay
helperHistPlot(pcsigMagdB,scale,shape);
%% Functions

function cmap = helperSeaColorMap(n)
% Color map for sea elevation plot

c = hsv2rgb([2/3 1 0.2; 2/3 1 1; 0.5 1 1]);
cmap = zeros(n,3);
cmap(:,1) = interp1(1:3,c(:,1),linspace(1,3,n)); 
cmap(:,2) = interp1(1:3,c(:,2),linspace(1,3,n));
cmap(:,3) = interp1(1:3,c(:,3),linspace(1,3,n)); 
end

function helperSeaSurfacePlot(x,y,z,rdrpos)
% Plot sea elevations

% Color map for sea elevation plot
seaColorMap = helperSeaColorMap(256);

% Plot
figure
z = reshape(z,numel(x),numel(y)); 
surf(x,y,z)
hold on
plot3(rdrpos(1),rdrpos(2),rdrpos(3),'ok','LineWidth',2,'MarkerFaceColor','k')
legend('Sea Surface','Radar','Location','Best')
shading interp
axis equal
xlabel('X (m)')
ylabel('Y (m)')
zlabel('Elevations (m)')
stdZ = std(z(:));
minC = -4*stdZ;
maxC = 4*stdZ;
minZ = min(minC,rdrpos(3)); 
maxZ = max(maxC,rdrpos(3)); 
title('Sea Surface Elevations')
axis tight
zlim([minZ maxZ])
hC = colorbar('southoutside');
colormap(seaColorMap)
hC.Label.String = 'Elevations (m)';
hC.Limits = [minC maxC];
drawnow
pause(0.25)
end

function sigHgt = helperEstimateSignificantWaveHeight(x,y,z)
% Plot an example showing how the wave heights are estimated and estimate
% the significant wave height 

% Plot wave height estimation
figure 
numX = numel(x);
z = reshape(z,numX,numel(y));
zEst = z(numX/2 + 1,:);
plot(x,zEst,'LineWidth',2)
grid on
hold on
xlabel('X (m)')
ylabel('Elevation (m)')
title('Wave Height Estimation')
axis tight
idxMin = islocalmin(z(numel(x)/2 + 1,:));
idxMax = islocalmax(z(numel(x)/2 + 1,:));
co = colororder; 
plot(x(idxMin),zEst(idxMin),'v', ...
    'MarkerFaceColor',co(2,:),'MarkerEdgeColor',co(2,:))
plot(x(idxMax),zEst(idxMax),'^', ...
    'MarkerFaceColor',co(3,:),'MarkerEdgeColor',co(3,:))
legend('Wave Elevation Data','Trough','Crest','Location','SouthWest')

% Estimate significant wave height
waveHgts = [];
for ii = 1:numX
    zEst = z(ii,:);
    idxMin = islocalmin(zEst);
    troughs = zEst(idxMin);
    numTroughs = sum(double(idxMin)); 
    idxMax = islocalmax(zEst);
    crests = zEst(idxMax);
    numCrests = sum(double(idxMax)); 
    numWaves = min(numTroughs,numCrests); 
    waveHgts = [waveHgts ...
        abs(crests(1:numWaves) - troughs(1:numWaves))]; %#ok<AGROW> 
end
waveHgts = sort(waveHgts); 
idxTopThird = floor(numel(waveHgts)*2/3);
sigHgt = mean(waveHgts(idxTopThird:end));
drawnow
pause(0.25)
end

function helperSeaSurfaceMotionPlot(x,y,seaSurf,plotTime)
% Color map for sea elevation plot
seaColorMap = helperSeaColorMap(256);

% Get initial height 
[xGrid,yGrid] = meshgrid(x,y);
z = height(seaSurf,[xGrid(:).'; yGrid(:).'],plotTime(1)); 

% Plot
hFig = figure;
hS = surf(x,y,reshape(z,numel(x),numel(y)));
hold on
shading interp
axis equal
xlabel('X (m)')
ylabel('Y (m)')
zlabel('Elevations (m)')
stdZ = std(z(:));
minZ = -4*stdZ; 
maxZ = 4*stdZ; 
title('Sea Surface Motion Plot')
xlim([-50 50])
ylim([-50 50])
zlim([minZ maxZ])
hC = colorbar('southoutside');
colormap(seaColorMap)
hC.Label.String = 'Elevations (m)';
hC.Limits = [minZ maxZ];
view([-45 12])

% Change figure size
ppos0 = get(hFig,'Position');
figWidth = 700;
figHeight = 300;
set(gcf,'position',[ppos0(1),ppos0(2),figWidth,figHeight])

numTimes = numel(plotTime);
for ii = 2:numTimes
    % Update plot
    z = height(seaSurf,[xGrid(:).'; yGrid(:).'],plotTime(ii));
    hS.ZData = reshape(z,numel(x),numel(y));
    drawnow
    pause(0.1)
end
pause(0.25)
end

function hRaw = helperPlotRawIQ(iqsig)
% Plot raw IQ magnitude

figure()
hRaw = pcolor(mag2db(abs(iqsig)));
hRaw.EdgeColor = 'none';
title('Raw IQ')
xlabel('Pulses')
ylabel('Samples')
hC = colorbar;
hC.Label.String = 'Magnitude (dB)'; 
drawnow
pause(0.25)
end

function helperUpdatePlotRawIQ(hRaw,iqsig)
% Update the raw IQ magnitude plot

hRaw.CData = mag2db(abs(iqsig)); 
drawnow
pause(0.25)
end

function helperRangeTimePlot(rngGrid,prf,pcsigMagdB)
% Range-Time Plot

figure() 
numPulses = size(pcsigMagdB,2); 
hImage = pcolor((1:numPulses)*1/prf,rngGrid,pcsigMagdB);
hImage.EdgeColor = 'none';
shading interp
xlabel('Time (sec)')
ylabel('Range (m)')
hC = colorbar;
hC.Label.String = 'Magnitude (dB)'; 
axis tight
title('Range versus Time')
clim([-20 0])
ylim([140 260])
drawnow
pause(0.25)
end

function helperMagTimePlot(magVals,numPulses,prf,rngVal)
% Magnitude vs. Time Plot

figure() 
plot((1:numPulses)*1/prf,magVals,'LineWidth',2)
grid on
xlabel('Time (sec)')
ylabel('Magnitude (dB)')
axis tight
title(sprintf('Magnitude versus Time at Range %.2f (m)',rngVal))
ylim([-20 0])
drawnow
pause(0.25)
end

function helperSTFTPlot(S,F,T,lambda,rngVal)
% Time-Frequency Plot 

figure()
S = mag2db(abs(S)); % Convert to dB
S = S - max(S(:)); % Normalize
Speed = dop2speed(F,lambda)/2; % Speed (m/s)
hSTFT = pcolor(T,Speed,S);
hold on
hSTFT.EdgeColor = 'none';
colorbar
xlabel('Time (sec)')
ylabel('Speed (m/s)')
title(sprintf('STFT at Range %.2f (m)',rngVal))
clim([-20 0])
ylim([-1 1])
drawnow
pause(0.25)
end

function helperHistPlot(pcsigMagdB,scale,shape)
% Amplitude Distribution

% Histogram
figure
hHist = histogram(pcsigMagdB,'Normalization','pdf'); % Create histogram
grid on
hold on
xlabel('Normalized Magnitude (dB)')
ylabel('PDF')
title('Amplitude Histogram')

% Lognormal overlay
edges = hHist.BinEdges;
x = (edges(2:end) + edges(1:end-1))./2;
z = x./scale;
w = exp(-(z.^shape));
y = z.^(shape - 1).*w .*shape./scale;
plot(x,y,'-r')
end