clear; clc; close all

% Generate an LFM signal
f1 = -10; f2 = 10;
N = 500;
t = linspace(0, 1, N);
xc = exp(1i*pi*(f2-f1)*t.^2); % LFM

% Apply a window function to reduce sidelobes (Hamming window as example)
window = hamming(N).'; % Create a Hamming window of the same size as the signal
xc_windowed = xc .* window; % Apply the window to the LFM signal

% Calculate the matched filter output for the windowed LFM
[pc_c, lags] = xcorr(xc_windowed); % Autocorrelation (matched filter output) for the windowed LFM signal

% Plot the results with two different scales
figure(1); clf; % Clear figure window and create a new figure

% yyaxis left; % Use left y-axis for the matched filter output
plot(lags, 20*log10(abs(pc_c))); % Plot the LFM signal's matched filter output in dB
ylabel('Matched Filter Output Power (dB)');
% 
% yyaxis right; % Use right y-axis for the window
% plot(lags, hamming(length(lags)), '--'); % Plot the Hamming window (dashed line for visibility)
% ylabel('Window Amplitude');

xlabel('Range Bin'); % Common x-label
xlim([-500 500]); % Adjust x-axis limits to match the range of lags
grid on;
% legend('Matched Filter Output', 'Hamming Window', 'Location', 'south');
% title('LFM Matched Filter Output and Hamming Window');
title('Windowed LFM Matched Filter Output');
