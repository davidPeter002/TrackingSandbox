import scipy.stats as st
import numpy as np
from math import sqrt 
import math

class Simulator:
    'Simulate object track with motion model'
    def simulate(self, model, param, num=50, dt=1, noiseVol=[1,1], start=[0,0], startT=0):
        truth = self.genTruth(model, param, num, dt, start, startT)
        noiseX = self.genNoise(num, noiseVol[0])
        noiseY = self.genNoise(num, noiseVol[1])
        signal = [[truth[i][0] + noiseX[i], truth[i][1] + noiseY[i], 
                   startT + dt * i] for i in range(num)]
        return [np.array(signal), truth, noiseX, noiseY]

    def genNoise(self, num, noiseVol, noiseMean=0):
        if isinstance(noiseVol, list):
            assert(len(noiseVol) == num)
            noise = [st.norm.rvs(noiseMean, noiseVol[i]) for i in range(num)]
            noise = np.array(noise)
        elif (isinstance(noiseVol, float) or isinstance(noiseVol, int)):
            noise = st.norm.rvs(noiseMean, noiseVol, num)
        else:
            print("noiseVol format not supported")
            noise = np.array()
        return noise
    
    def genTruth(self, model, param, num, dt, start, startT):
        if model == 'stationary':
            return np.array([start + [dt * i + startT] for i in range(num)])
        if model == 'cv':
            assert(len(param) == 2)
            v = param[0]
            theta = param[1]
            return np.array(
                    [[start[0] + v * dt * i * math.cos(theta), 
                     start[1] + v * dt * i * math.sin(theta),
                     dt * i + startT] 
                     for i in range(num)])
        if model == 'ca':
            assert(len(param) == 3)
            v0 = param[0]
            a = param[1]
            theta = param[2]
            return np.array(
                    [[start[0] + (v0 * dt + 0.5 * a * (dt * i) ** 2) * math.cos(theta), 
                     start[1] + (v0 * dt + 0.5 * a * (dt * i) ** 2) * math.sin(theta),
                     dt * i + startT]
                     for i in range(num)])

# start = [100, 100]
# num = 20
# dt = 1
# model = 'cv'
# param = [10, math.radians(90)]
# model = 'ca'
# param = [10, 1.5, math.radians(90)]
# noise = [0.5, 5]

# s = Simulator()
# truth, noiseX, noiseY, track = s.simulate(model, param, num, dt, noise, start)

# import matplotlib.pyplot as plt
# fig = plt.figure(1)
# plt.axes(adjustable='datalim', aspect='equal')
# plt.scatter(track[:,0], track[:,1])
# plt.scatter(truth[:,0], truth[:,1])
# plt.plot(track[:,0], track[:,1])
# plt.plot(truth[:,0], truth[:,1])

# plt.figure(2)
# plt.plot(noiseX, 'o-b')
# plt.plot(noiseY, 'o-r')
# plt.show()