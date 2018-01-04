import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate2d

from Ferromagnet import * 

#Reset
N = 50 #Size of the ferromagnet
spins = reset(N,"up") #All spin up

Ts = np.array([0.1,0.4,2.5,10]) #Temperatures
for T in Ts:
    NH = 30 #Number of field-values
    H_extreme = 10
    Hs = np.linspace(-H_extreme,H_extreme,NH)
    Hs = np.hstack((Hs,Hs[::-1])) #A full loop
    M = 500 #Number of time-steps
    mag = np.zeros(2*NH)
    for n in np.arange(M):
        spins = step(spins,T,-H_extreme)

    for m in np.arange(2*NH):
        H = Hs[m]
        net_mag = np.zeros(M,dtype='float')
        for n in np.arange(M):
            net_mag[n] = np.sum(spins) #Sampling magnetisation
            spins = step(spins,T,H)
        mag[m] = np.mean(net_mag[M//2:])
        #print(H)

    plt.plot(Hs,mag/N**2,'-')
plt.ylim([-1.1,1.1])
plt.legend(np.asarray(Ts,dtype='str'))
plt.xlim([-H_extreme*1.1,H_extreme*1.1])
plt.xlabel('Magnetic field, H',size=16)
plt.ylabel('Net magnetisation per lattice point',size=16)
plt.title('Ferromagnetic hysteresis loops over a range of temperatures',size=18)
plt.show()
