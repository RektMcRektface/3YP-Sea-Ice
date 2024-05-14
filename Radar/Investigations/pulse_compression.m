clear; clc; close all

% generate an LFM and a tone
f1 = -20; f2 = 20;
N = 500;
t  = linspace(0,1,N);
f = (0:N-1)/(t(2)-t(1));
xc = exp(1i*pi*(f2-f1)*t.^2); % LFM
xf = exp(1i*pi*f1*t);         % tone


% calculate the matched filter output for the LFM
[pc_c,lags] =  xcorr(xc);

% plot the results
figure(1); hold off;
plot(lags,20*log10(abs((pc_c))));
hold on;
plot(lags,20*log10(abs(xcorr(xf))))
ylabel('Power (dB)'); xlabel('Range Bin'); xlim([-500 500]); grid on;
legend('Matched Filtered LFM','Matched Filtered Sinusoid', Location='south');
title('Comparison of Pulse Compressed Waveforms')

window = hamming(N).'; % Create a Hamming window of the same size as the signal
xc_windowed = xc .* window; % Apply the window to the LFM signal

figure; subplot(3,1,1)
plot(t, real(xc))
xlabel('Time')
ylabel('Signal')

subplot(3,1,2)
plot(t,real(xf))
xlabel('Time')
ylabel('Signal')

subplot(3,1,3)
plot(t,xc_windowed)
hold on
plot(t,window, '--')
xlabel('Time')
ylabel('Signal')
lgd = legend('Windowed LFM Waveform', 'Hamming Window');
fontsize(lgd,14,'points')
% 
% figure; plot(f, fftshift(abs(fft(xc))))
% figure; plot(f, fftshift(abs(fft(xf))))