import time

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate2d

from Ferromagnet import * 

#Evaluating the performance of three time-step algorithms

#Method 1
Ns = np.arange(2,100,2)
ts = np.zeros(Ns.size)
M = 5000

for n in np.arange(Ns.size):
    N = Ns[n]
    spins = reset(N,"random")
    t0 = time.clock()
    for m in np.arange(M):
        #Perform a step using method 1
        spins = step(spins,Tc,0) 
    t1 = time.clock()
    ts[n] = t1-t0
    if n % 10 == 0:
        print(N)
        
ts = ts / M #Time taken per step
plt.loglog(Ns,ts,'x')

#Method 2
Ns = np.arange(2,100,2)
ts = np.zeros(Ns.size)
M = 5000

for n in np.arange(Ns.size):
    N = Ns[n]
    spins = reset(N,"random")
    t0 = time.clock()
    for m in np.arange(M):
        #Perform a step using single flips, method 2
        spins = step2(spins,Tc,0) 
    t1 = time.clock()
    ts[n] = t1-t0
    if n % 10 == 0:
        print(N)

#N**2 steps in this method = 1 step in the other two        
ts = ts*Ns**2 / M 
        
plt.loglog(Ns,ts,'x')


#Method 3
Ns = np.arange(2,100,2)
ts = np.zeros(Ns.size)
M = 5000

for n in np.arange(Ns.size):
    N = Ns[n]
    spins = reset(N,"random")
    t0 = time.clock()
    for m in np.arange(M):
        #Perform a step using method 3
        spins = step3(spins,Tc,0) 
    t1 = time.clock()
    ts[n] = t1-t0
    if n % 10 == 0:
        print(N)
ts = ts / M
        
plt.loglog(Ns,ts,'x')
plt.legend(['Method 1', 'Method 2', 'Method 3'])
plt.xlabel('N',size=16)
plt.ylabel('Time taken per step / s',size=16)
plt.title('Time taken per step for the three algorithms',size=18)
plt.show() 