import scipy.stats as st
from scipy.optimize import curve_fit
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
from simulator import Simulator

class Smoother:
    def smooth(self, track, model='auto'):
        if model == 'stationary':
            return self.stationaryModel(track)
        if model == 'cv':
            return self.cvModel(track)
        if model == 'ca':
            return self.caModel(track)

    def stationaryModel(self, track):
        func = lambda t : [st.tmean(track[:,0]), st.tmean(track[:,1])]
        smoothTrack = np.array([func(t) for t in track[:,2]])
        smoothTrack = np.append(smoothTrack, np.array([track[:,2]]).T, axis=1)
        rms = sqrt(np.sum(np.power((track - smoothTrack), 2)) / track.shape[0])
        return [func, smoothTrack, rms]

    def cvModel(self, track):
        def cvFunc(t, a, b):
            return a * t + b
        px, _ = curve_fit(cvFunc, track[:,2], track[:,0])
        py, _ = curve_fit(cvFunc, track[:,2], track[:,1])
        func = lambda t : [cvFunc(t, px[0], px[1]), cvFunc(t, px[0], px[1])]
        smoothTrack = np.array([func(t) for t in track[:,2]])
        smoothTrack = np.append(smoothTrack, np.array([track[:,2]]).T, axis=1)
        rms = sqrt(np.sum(np.power((track - smoothTrack), 2)) / track.shape[0])
        return [func, smoothTrack, rms]
    
    def caModel(self, track):
        def caFunc(t, a, b, c):
            return 0.5 * a * t**2 + b * t + c
        px, _ = curve_fit(caFunc, track[:,2], track[:,0])
        py, _ = curve_fit(caFunc, track[:,2], track[:,1])
        func = lambda t : [caFunc(t, px[0], px[1], px[2]), caFunc(t, py[0], py[1], py[2])]
        smoothTrack = np.array([func(t) for t in track[:,2]])
        smoothTrack = np.append(smoothTrack, np.array([track[:,2]]).T, axis=1)
        rms = sqrt(np.sum(np.power((track - smoothTrack), 2)) / track.shape[0])
        return [func, smoothTrack, rms]