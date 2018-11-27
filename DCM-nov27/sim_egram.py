import scipy
import scipy.signal as sig
import matplotlib.pyplot as plt


def sim_egram(bpm):
    rr = [60/bpm, 60/bpm, 60/bpm, 60/bpm, 60/bpm, 60/bpm, 60/bpm] # time before next pace in seconds
    fs = 50.0 # sampling rate
    pqrst = sig.wavelets.daub(10) # just to simulate a signal, whatever
    ecg = scipy.concatenate([sig.resample(pqrst, int(r*fs)) for r in rr])
    t = scipy.arange(len(ecg))/fs

    return t,ecg
