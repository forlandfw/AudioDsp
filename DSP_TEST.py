from ThinkDSP.code.thinkdsp import CosSignal, SinSignal, decorate

cos_sig = CosSignal(freq=440, amp=1.0, offset=0)
sin_sig = SinSignal(freq=880, amp=0.5, offset=0)

cos_sig.plot()
decorate(xlabel='Time (s)')
