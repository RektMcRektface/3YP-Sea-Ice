% A script in order to investigate the effects of matched filtering
% Author: PH

clear; clc; close all
rng(2002);

% Define Parameters
pw = 1e-4;
prf = 5e3;
fs = 1/1e7;
N = 9;

% Create chirp
chirped_waveform = phased.LinearFMWaveform('PulseWidth',pw,'PRF',prf,...
    'SampleRate',1/fs,'OutputFormat','Pulses','NumPulses',1,...
    'SweepBandwidth',1e5);
chirp = chirped_waveform();
chirp = [zeros(numel(chirp)/2,1) ; chirp];
chirp = chirp + N*(randn(length(chirp),1) + 1j*randn(length(chirp),1));
chirp_filter = phased.MatchedFilter('Coefficients', getMatchedFilter(chirped_waveform));

% Get timescale
t = linspace(0,3*pw,numel(chirp));

% Create beep
beep_waveform = ones(numel(chirp)/3,1);
beep = [zeros(numel(chirp)/3,1) ; beep_waveform ; zeros(numel(chirp)/3,1)];
beep = beep + N*(randn(length(beep),1));

% Plot original signals
figure; subplot(2,1,1)
plot(t,real(chirp))
axis('tight')
title('LFM Waveform with added Gaussian noise')
xlabel('Time')
ylabel('Signal')

subplot(2,1,2)
plot(t,real(beep))
axis('tight')
title('CMW with added Gaussian noise')
xlabel('Time')
ylabel('Signal')

% Plot filtered signals
figure; subplot(2,1,1)
plot(t,real(chirp_filter(chirp)))
axis('tight')
title('Noisy LFM Waveform after matched filtering')
xlabel('Time')
ylabel('Signal')

subplot(2,1,2)
plot(t,conv(beep, beep_waveform, 'same'))
axis('tight')
title('Noisy CMW after matched filtering')
xlabel('Time')
ylabel('Signal')