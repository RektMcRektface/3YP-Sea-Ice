clear; clc; close all

% Parameters for the LFM signal
f1 = -30; % starting frequency
f2 = 30;  % ending frequency
N = 500;  % number of samples
t = linspace(0, 1, N); % time vector

% Generate the base LFM signal
xc_base = exp(1i*pi*(f2-f1)*t.^2); % LFM
xf_base = exp(1i*pi*f1*t);         % tone

% Second Target Shifted by n
n = 100;
xc_shift = circshift(xc_base, n);
xc_shift([1:n,end+n+1:end]) = 0;

xf_shift = circshift(xf_base, n);
xf_shift([1:n,end+n+1:end]) = 0;

% Combined received signal
xc_combined = xc_base + xc_shift;
xf_combined = xf_base + xf_shift;

% Calculate the matched filter output for the combined signal
[pc_c, lags] = xcorr(xc_combined, xc_base); % Using the base LFM signal as the template

% Plot the results
figure(1); hold off;
plot(lags, 20*log10(abs(pc_c)));
hold on;
plot(lags,20*log10(abs(xcorr(xf_combined))))
ylabel('Power (dB)'); xlabel('Range Bin'); xlim([-500 500]); grid on;
title('Matched Filter Output for Two Targets');
legend('Matched Filtered LFM','Matched Filtered Sinusoid', 'Location', 'south');