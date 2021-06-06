from simulator import Simulator
from smoother import Smoother
import math
import matplotlib.pyplot as plt

start = [100, 100]
num = 20
dt = 1
model = 'stationary'
param = []
model = 'cv'
param = [10, math.radians(90)]
model = 'ca'
param = [10, 1.5, math.radians(90)]

noise = [0.5, 5]

sim = Simulator()
smoother = Smoother()

track, truth, noiseX, noiseY = sim.simulate(model, param, num, dt, noise, start)
func, smooth, rms = smoother.smooth(track, model)
errorX = smooth[:, 0] - truth[:, 0]
errorY = smooth[:, 1] - truth[:, 1]

ax1 = plt.subplot(231)
ax1.set_adjustable('datalim')
ax1.set_aspect('equal')
ax1.plot(truth[:, 0], truth[:, 1], 'o-g')
ax1.plot(track[:, 0], track[:, 1], 'o-y')
ax1.plot(smooth[:, 0], smooth[:, 1], 'o-b')

ax2 = plt.subplot(232)
ax2.plot(truth[:,2], truth[:, 0], 'g')
ax2.plot(track[:,2], track[:, 0], 'y')
ax2.plot(smooth[:, 2], smooth[:, 0], 'b')

ax3 = plt.subplot(233)
ax3.plot(truth[:,2], truth[:, 1], 'g')
ax3.plot(track[:,2], track[:, 1], 'y')
ax3.plot(smooth[:, 2], smooth[:, 1], 'b')

ax4 = plt.subplot(223)
ax4.plot(errorX, 'b')
ax4.plot(noiseX, 'r')

ax5 = plt.subplot(224)
ax5.plot(errorY, 'b')
ax5.plot(noiseY, 'r')

plt.show()
pass
