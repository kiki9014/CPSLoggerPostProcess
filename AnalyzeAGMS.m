close all;

deviceType = 'Iron2';

addpath(deviceType);

load([deviceType, '/', 'AccData_2016_05_12.mat']);
load([deviceType, '/', 'GyroData_2016_05_12.mat']);
load([deviceType, '/', 'MagData_2016_05_12.mat']);
load([deviceType, '/', 'StepData_2016_05_12.mat']);
% 
% load(['AccData_2016_05_02.mat']);
% load(['GyroData_2016_05_02.mat']);
% load(['MagData_2016_05_02.mat']);
% load(['StepData_2016_05_02.mat']);

timeAcc = Acc(:,1) * 3600 + Acc(:,2)*60 + Acc(:,3);
timeGyro = Gyro(:,1) * 3600 + Gyro(:,2)*60 + Gyro(:,3);
timeMag = Mag(:,1) * 3600 + Mag(:,2)*60 + Mag(:,3);

figure;
plot(timeAcc);
figure;
plot(timeGyro);
figure;
plot(timeMag);
figure;
plot(Acc(:,5:end));
figure;
plot(Gyro(:,5:end));
figure;
plot(Mag(:,5:end));

freqAcc = diff(timeAcc);
freqGyro = diff(timeGyro);
freqMag = diff(timeMag);

slowAcc = freqAcc(freqAcc>1);
slowGyro = freqGyro(freqGyro>1);
slowMag = freqMag(freqMag>1);

slowTimeAcc = Acc(freqAcc>1,1:3);
slowTimeGyro = Gyro(freqGyro>1,1:3);
slowTimeMag = Mag(freqMag>1,1:3);

windowSize = 10;

b = (1/windowSize)*ones(windowSize,1);
a = 1;

magF = filter(b,a,Mag(:,5:end));

freqAccF = smooth(freqAcc);

figure;
plot(freqAcc);
figure;
plot(Mag(:,2));

figure;
plot(magF);