import copy
import math
import random
import wave

import matplotlib.pyplot as plt
import numpy as np
import scipy

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

       def period(self):
              """To reload in subclass"""
              return 0.1
       
       def plot(self, frame_rate=11025):
              duration = self.period * 3
              wave = self.make_wave(duration, start=0, frame_rate=frame_rate)
       
       def make_wave(self, duration=1, start=0, frame_rate=11025):
              n = round(duration*frame_rate)
              ts = start + np.arange(n)/frame_rate
              ys = self.evaluate(ts)
              return Wave(ys, ts, frame_rate=frame_rate)

       def evaluate(self, ts):
              return 1

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
              assert self.frame_rate = other.frame_rate

              start = min(self.start, other.start)
              end = max(self.end, other.end)
              n = int(round((end - start)*self.frame_rate))+1
              ys = np.zeros(n)
              ts = start+np.arange(n)/self.frame_rate
              

class Sum_signal（Signal):
       def __init__(sefl, *args):
              self.signals = args
       def period(self):
              return max(sig.period for sig in self.signals)
       def evaluate(self, ts):
              ts = np.asarray(ts)
              return sum(sig.evaluate(ts) for sig in self.signals)

class Sinusoid(Signal):
       def __init__(self, freq=400, amp=1.0, offset=0, func=np.sin):
