% A script in order to investigate the effects of matched filtering
% Author: PH

clear; clc; close all

% Define Parameters
pw = 1e-4;
prf = 5e3;
fs = 1/1e7;

% Create chirp
chirped_waveform = phased.LinearFMWaveform('PulseWidth',pw,'PRF',prf,...
    'SampleRate',1/fs,'OutputFormat','Pulses','NumPulses',1,...
    'SweepBandwidth',1e5);
chirp = chirped_waveform();
chirp = [zeros(numel(chirp)/2,1) ; chirp];
chirp_filter = phased.MatchedFilter('Coefficients', getMatchedFilter(chirped_waveform));

% Get timescale
t = linspace(0,3*pw,numel(chirp));

% Create beep
beep_waveform = ones(numel(chirp)/3,1);
beep = [zeros(numel(chirp)/3,1) ; beep_waveform ; zeros(numel(chirp)/3,1)];

% Plot original signals
figure; subplot(2,1,1)
plot(t,real(chirp))
axis('tight')
title('Chirped signal')
xlabel('Time')
ylabel('Signal')

subplot(2,1,2)
plot(t,beep)
axis('tight')
title('Beeped signal')
xlabel('Time')
ylabel('Signal')

% Plot filtered signals
figure; subplot(2,1,1)
plot(t,chirp_filter(chirp))
axis('tight')
title('Chirp after matched filtering')
xlabel('Time')
ylabel('Signal')

subplot(2,1,2)
plot(t,conv(beep, beep_waveform, 'same'))
axis('tight')
title('Beep after matched filtering')
xlabel('Time')
ylabel('Signal')