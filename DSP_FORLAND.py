import copy
import math
import random
import wave
import warnings

import matplotlib.pyplot as plt
import numpy as np
import scipy

try:
       from IPython.display import Audio
except:
       warnings.warn("Can't import Audio from IPython.display;")

PI2 = math.pi*2

def find_index(x, xs):
    n = len(xs)
    start = xs[0]
    end = xs[-1]
    i = round((n - 1) * (x - start) / (end - start))
    return int(i)

class Wave:
       def __init__(self, ys, ts=None, frame_rate= None):
              self.ys = np.asanyarray(ys)
              self.frame_rate = frame_rate if frame_rate is not None else 11025

              if ts is None:
                     self.ts = np.arange(len(ys))/self.frame_rate
              else:
                     self.ts = np.asanyarray(ts)

       def copy(self):
              return copy.deepcopy(self)

       def __len__(self):
              return len(self.ys)             
       def start(self):
              return self.ts[0]
       def end(self):
              return self.ts[-1]
       def duration(self):
              return len(self.ys)/self.frame_rate
       
       def __add__(self, other):
              if other == 0:
                     return self
              assert self.frame_rate == other.frame_rate

              start = min(self.start, other.start)
              end = max(self.end, other.end)
              n = int(round((end - start)*self.frame_rate))+1
              ys = np.zeros(n)
              ts = start+np.arange(n)/self.frame_rate

              def add_ys(wave):
                     i = find_index(wave.start, ts)
                     
                     diff = ts[i] - wave.start
                     dt = 1/wave.frame_rate
                     if(diff/dt)>0.1:
                            warnings.warn("Can't add these waveforms")
                     j = i + len(wave)
                     ys[i:j] += wave.ys

              add_ys(self)
              add_ys(other)
              return Wave(ys, ts, self.frame_rate)
       __radd__ = __add__

       def __or__(self, other):
              if self.frame_rate != other.frame_rate:
                     raise ValueError("Wave.__or__: framerates do not agree")

              ys = np.concatenate((self.ys, other.ys))
              return Wave(ys, frame_rate=self.frame_rate)
              

class Signal:
       # signal commom property
       #1. to plot as a figure
       #2. to add in math
       def __init__(self):
              pass
       def __add__(self, other):
              if other == 0:
                     return self
              return Sum_signal(self, other)
       
       __radd__ = __add__

       def period(self):
              """To reload in subclass"""
              return 0.1
       
       def plot(self, frame_rate=11025):
              duration = self.period * 3
              wave = self.make_wave(duration, start=0, frame_rate=frame_rate)
              wave.plot()

       def make_wave(self, duration=1, start=0, frame_rate=11025):
              n = round(duration*frame_rate)
              ts = start + np.arange(n)/frame_rate
              ys = self.evaluate(ts)
              return Wave(ys, ts, frame_rate=frame_rate)

       def evaluate(self, ts):
              return 1

class Sum_signal(Signal):
       def __init__(sefl, *args):
              self.signals = args

       def period(self):
              return max(sig.period for sig in self.signals)
       
       def evaluate(self, ts):
              ts = np.asarray(ts)
              return sum(sig.evaluate(ts) for sig in self.signals)

class Sinusoid(Signal):
       def __init__(self, freq=400, amp=1.0, offset=0, func=np.sin):
              self.freq = freq
              self.amp = amp
              self.offset = offset
              self.func = func

       def period(self):
              return 1.0/self.freq
       
       def evaluate(self, ts):
              ts = np.asarray(ts)
              phases = PI2*self.freq*ts + self.offset
              ys = self.amp*self.func(phases)
              return ys
def cos_signal(freq=440, amp=1.0, offset=0):
       return Sinusoid(freq, amp, offset, func=np.cos)

def sin_signal(freq=440, amp=1.0, offset=0):
       return Sinusoid(freq, amp, offset, func=np.sin)

def sinc(freq=440, amp=1.0, offset=0):
       return Sinusoid(freq, amp, offset, func=np.sinc)

class Complex_sinusoid(Sinusoid):
       def evaluate(self, ts):
              ts = np.asarray(ts)
              phases = PI2*self.freq*ts+self.offset
              ys = self.amp*np.exp(1j*phases)
              return ys      

class Square_signal(Sinusoid):
       def evaluate(self, ts):
              ts = np.asarray(ts)
              cycles = self.freq*ts + self.offset/PI2
              frac, _ = np.modf(cycles)
              ys = self.amp * np.sign(unbias(frac))
              return ys



              


print('Is Running!')