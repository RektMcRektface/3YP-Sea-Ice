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
t = tiledlayout(1,1);
ax1 = axes(t);

plot(ax1, lags, 20*log10(abs(pc_c))); % Plot the LFM signal's matched filter output in dB
ylabel(ax1,'Matched Filter Output Power (dB)');
xlabel(ax1,'Sample Number');
ax1.XColor = '[0 0.4470 0.7410]';

ax2 = axes(t);

hold on
ax2.XAxisLocation = 'top';
ax2.YAxisLocation = 'right';
plot(ax2, t, window, '--'); % Plot the Hamming window (dashed line for visibility)
ylabel(ax2, 'Window Amplitude');
xlabel(ax2,'Time');
ax2.Color = 'none';

ax1.Box = 'off';
ax2.Box = 'off';

 % Common x-label
xlim([-500 500]); % Adjust x-axis limits to match the range of lags
grid on;
legend('Matched Filter Output', 'Hamming Window', 'Location', 'south');
title('LFM Matched Filter Output and Hamming Window');
