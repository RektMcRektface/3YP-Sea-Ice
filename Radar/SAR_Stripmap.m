% A script to model SAR Stripmap imaging with differnt algorithms
% Author: Panu Hietanen
clear; clc; close all

%% Set up parameters
c = physconst('LightSpeed');

fc = 10e9; % Centre frequency

rangeResolution = 1;
crossRangeResolution = 1;

bw = c/(2*rangeResolution);

prf = 1e3; % Pulse repetition frequency
aperture = 2; % Aperture size
tpd = 3*10^-6; % Pulse width / s
fs = 120*10^6; % Sampling frequency

%% Model RADAR platform
waveform = phased.LinearFMWaveform('SampleRate',fs, 'PulseWidth', tpd, 'PRF', prf, 'SweepBandwidth', bw);

speed = 100;
height = 500;
flightDuration = 4;
radarPlatform  = phased.Platform('InitialPosition', [0;-200;height], 'Velocity', [0; speed; 0]);
slowTime = 1/prf;
numpulses = flightDuration/slowTime +1;

maxRange = 2500;
truncrangesamples = ceil((2*maxRange/c)*fs);
fastTime = (0:1/fs:(truncrangesamples-1)/fs);
% Set the reference range for the cross-range processing.
Rc = 1000;

antenna = phased.CosineAntennaElement('FrequencyRange', [8e9 12e9]);
antennaGain = aperture2gain(aperture,c/fc);

transmitter = phased.Transmitter('PeakPower', 50e3, 'Gain', antennaGain);
radiator = phased.Radiator('Sensor', antenna,'OperatingFrequency', fc, 'PropagationSpeed', c);

collector = phased.Collector('Sensor', antenna, 'PropagationSpeed', c,'OperatingFrequency', fc);
receiver = phased.ReceiverPreamp('SampleRate', fs, 'NoiseFigure', 30);

channel = phased.FreeSpace('PropagationSpeed', c, 'OperatingFrequency', fc,'SampleRate', fs, 'TwoWayPropagation', true);


%% Create scenario with stationary targets
targetpos= [800,0,0;1000,0,0; 1300,0,0]';

targetvel = [0,0,0;0,0,0; 0,0,0]';

target = phased.RadarTarget('OperatingFrequency', fc, 'MeanRCS', [1,1,1]);
pointTargets = phased.Platform('InitialPosition', targetpos,'Velocity',targetvel);
% The figure below describes the ground truth based on the target
% locations.
figure;h = axes;plot(targetpos(2,1),targetpos(1,1),'*g');hold all;plot(targetpos(2,2),targetpos(1,2),'*r');hold all;plot(targetpos(2,3),targetpos(1,3),'*b');hold off;
set(h,'Ydir','reverse');xlim([-10 10]);ylim([700 1500]);
title('Ground Truth');ylabel('Range');xlabel('Cross-Range');

%% RADAR Simulation
% Define the broadside angle
refangle = zeros(1,size(targetpos,2));
rxsig = zeros(truncrangesamples,numpulses);
for ii = 1:numpulses
    % Update radar platform and target position
    [radarpos, radarvel] = radarPlatform(slowTime);
    [targetpos,targetvel] = pointTargets(slowTime);

    % Get the range and angle to the point targets
    [targetRange, targetAngle] = rangeangle(targetpos, radarpos);

    % Generate the LFM pulse
    sig = waveform();
    % Use only the pulse length that will cover the targets.
    sig = sig(1:truncrangesamples);

    % Transmit the pulse
    sig = transmitter(sig);

    % Define no tilting of beam in azimuth direction
    targetAngle(1,:) = refangle;

    % Radiate the pulse towards the targets
    sig = radiator(sig, targetAngle);

    % Propagate the pulse to the point targets in free space
    sig = channel(sig, radarpos, targetpos, radarvel, targetvel);

    % Reflect the pulse off the targets
    sig = target(sig);

    % Collect the reflected pulses at the antenna
    sig = collector(sig, targetAngle);

    % Receive the signal
    rxsig(:,ii) = receiver(sig);

end

%% Plot raw IQ
figure;imagesc(real(rxsig));title('SAR Raw Data')
xlabel('Cross-Range Samples')
ylabel('Range Samples')

%% Range compression algorithm
% This dechrips each row of our received signal using matched filtering
pulseCompression = phased.RangeResponse('RangeMethod', 'Matched filter', 'PropagationSpeed', c, 'SampleRate', fs);
matchingCoeff = getMatchedFilter(waveform);
[cdata, rnggrid] = pulseCompression(rxsig, matchingCoeff);

% Plot results
figure;imagesc(real(cdata));title('SAR Range Compressed Data')
xlabel('Cross-Range Samples')
ylabel('Range Samples')

%% Contrast different algortithms


% Range migration
rma_processed = helperRangeMigration(cdata,fastTime,fc,fs,prf,speed,numpulses,c,Rc);
figure;
imagesc((abs((rma_processed(1700:2300,600:1400).'))));
title('SAR Data focused using Range Migration algorithm ')
xlabel('Cross-Range Samples')
ylabel('Range Samples')

% Back projection
bpa_processed = helperBackProjection(cdata,rnggrid,fastTime,fc,fs,prf,speed,crossRangeResolution,c);
figure;
imagesc((abs(bpa_processed(600:1400,1700:2300))));
title('SAR Data focused using Back-Projection algorithm ')
xlabel('Cross-Range Samples')
ylabel('Range Samples')

%% Functions

function azcompresseddata = helperRangeMigration(sigData,fastTime,fc,fs,prf,speed,numPulses,c,Rc)
frequencyRange = linspace(fc-fs/2,fc+fs/2,length(fastTime));
krange = 2*(2*pi*frequencyRange)/c;
% Set the cross-range wavenumber.
kaz = 2*pi*linspace(-prf/2,prf/2,numPulses)./speed;

% Generate a matrix of the cross-range wavenumbers to match the size of the
% received two-dimensional SAR signal.

kazimuth = kaz.';
kx = krange.^2-kazimuth.^2;

% Set the final wavenumber to achieve azimuth focusing.

kx = sqrt(kx.*(kx > 0));
kFinal = exp(1i*kx.*Rc);

% Perform a two-dimensional FFT on the range compressed signal.

sdata =fftshift(fft(fftshift(fft(sigData,[],1),1),[],2),2);

% Perform bulk compression to get the azimuth compression at the reference range.
% Perform filtering of the 2-D FFT signal with the new cross-range wavenumber
% to achieve complete focusing at the reference range and as a by-product, partial
% focusing of targets not lying at the reference range.

fsmPol = (sdata.').*kFinal;

% Perform Stolt interpolation to achieve focusing for targets that are not lying
% at the reference range.

stoltPol = fsmPol;
for i = 1:size((fsmPol),1)
    stoltPol(i,:) = interp1(kx(i,:),fsmPol(i,:),krange(1,:));
end
stoltPol(isnan(stoltPol)) = 1e-30;
stoltPol = stoltPol.*exp(-1i*krange.*Rc);
azcompresseddata = ifft2(stoltPol);
end

% Back-Projection Algorithm
function data = helperBackProjection(sigdata,rnggrid,fastTime,fc,fs,prf,speed,crossRangeResolution,c)
% This function demonstrates the time-domain back projection algorithm for imaging
% the side-looking synthetic aperture radar. The pulsed compressed synthetic aperture
% data is taken as input in this algorithm. Initialize the output matrix.

data = zeros(size(sigdata));
azimuthDist = -200:speed/prf:200;%azimuth distance

% Limit the range and cross-range pixels being processed to reduce processing
% time.

rangelims = [700 1400];
crossrangelims = [-10 10];

% Index the range grid in accordance with the range limits.

rangeIdx =  [find(rnggrid>rangelims(1), 1) find(rnggrid<rangelims(2),1,'last')];

% Index the azimuth distance in accordance with the cross-range limits.

crossrangeIdxStart = find(azimuthDist>crossrangelims(1),1);
crossrangeIdxStop = find(azimuthDist<crossrangelims(2),1,'last');
for i= rangeIdx(1):rangeIdx(2)  % Iterate over the range indices

    % Using desired cross-range resolution, compute the synthetic aperture
    % length
    lsynth= (c/fc)* (c*fastTime(i)/2)/(2*crossRangeResolution);
    lsar = round(lsynth*length(azimuthDist)/azimuthDist(end)) ;
    % Ensure lsar is an odd number
    lsar = lsar + mod(lsar,2);

    % Construct hanning window for cross-range processing, to suppress the
    % azimuthal side lobes
    hn= hanning(lsar).';
    % Iterate over the cross-range indices
    for j= crossrangeIdxStart:crossrangeIdxStop
        % azimuth distance in x direction over cross-range indices
        posx= azimuthDist(j);
        % range in y-direction over range indices
        posy= c*fastTime(i)/2;
        % initializing count to zero
        count= 0;
        % Iterate over the synthetic aperture
        for k= j-lsar/2 +1:j+ lsar/2
            % Time delay for each of range and cross-range indices
            td= sqrt((azimuthDist(k)- posx)^2 + posy^2)*2/c;
            cell= round(td*fs) +1 ;
            signal = sigdata(cell,k);
            count= count + hn(k -(j-lsar/2))*signal *exp(1j*2*pi*fc*(td));
        end
        % Processed data at each of range and cross-range indices
        data(i,j)= count;
    end

end
end

