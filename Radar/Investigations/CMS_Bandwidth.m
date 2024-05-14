% A script in order to investigate the relationship between bandwidth and
% pulse width in a square wave
% Author: PH

clear; clc; close all

N = 1000;
t = linspace(0, 1e-4, N);

fs = 1/(t(2)-t(1));
f = fs*(0:(N-1));

n = 100;
s = ones(n, 1);
s = [zeros((numel(t)-n)/2,1); s; zeros((numel(t)-n)/2,1)];

plot(t, s)
axis('tight')
ylim([0,2])
xlabel('Time')
ylabel('Signal')
title('Constant Magnitude Signal, \tau = 50ms')

F = fftshift(abs(fft(s)));
figure; plot(f, fftshift(abs(fft(s))))
xlabel('Frequency')
ylabel('FFT Magnitude')
title('Constant Magnitude FFT, \tau = 50ms')
xlim([3 7]*1e9)