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
f = fs*(0:(numel(chirp)-1));

% Create beep
beep_waveform = ones(numel(chirp)/3,1);
beep = [zeros(numel(chirp)/3,1) ; beep_waveform ; zeros(numel(chirp)/3,1)];

chirp_f = fftshift(abs(fft(chirp)));
beep_f = fftshift(abs(fft(beep)));

% Plot original signals
figure;
plot(t,real(chirp))
axis('tight')
title('LFM Waveform')
xlabel('Time')
ylabel('Signal')

figure
plot(t,beep)
axis('tight')
title('Constant Magnitude Waveform')
xlabel('Time')
ylabel('Signal')
ylim([0,2])

% Plot filtered signals
figure; subplot(2,1,1)
plot(t,real(chirp_filter(chirp)))
axis('tight')
title('LFM Waveform after matched filtering')
xlabel('Time')
ylabel('Signal')

subplot(2,1,2)
plot(t,conv(beep, beep_waveform, 'same'))
axis('tight')
title('CMW after matched filtering')
xlabel('Time')
ylabel('Signal')

figure; plot(f, chirp_f)
title('FFT of LFM Waveform')
xlabel('Frequency')
ylabel('FFT')
xlim([1.3 1.7]*1e-4)

figure; plot(f, beep_f)
title('FFT of Constant Magnitude Waveform')
xlabel('Frequency')
ylabel('FFT')
xlim([1.3 1.7]*1e-4)