import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate2d
from scipy.ndimage.measurements import label
from scipy.interpolate import splrep, splev
from scipy.optimize import curve_fit

from Ferromagnet import * 

Ns = np.arange(4,60,4) #Size of the ferromagnet
Tcs = np.zeros(Ns.size)

NT = 100
Ts = np.linspace(0.1*Tc,2*Tc,NT)
M = 500
H = 0
I = 10
for i in np.arange(I):
    for n in np.arange(Ns.size):
        N = Ns[n]
        spins = np.ones((N,N)) #All spin up
        #Investigating temperature dependence, zero field
        E = np.zeros(NT)
        for x in np.arange(500): #Initial step 
            spins = step(spins,0.1*Tc,H)

        for m in np.arange(Ts.size):
            T = Ts[m]
            energy_array = np.zeros(M,dtype='float')
            for k in np.arange(M):
                a,b = getEnergy(spins,H)
                energy_array[k] = np.sum(a+b)
                spins = step(spins,T,H)
            E[m] = np.mean(energy_array[2*M//3:])

        Tcs[n] += getTc(Ts,E)
    #    plt.plot([Tcs[n],Tcs[n]],plt.ylim())
    #    plt.show()
        print(N)

Tcs /= I
        
def fittingf(x,a,b):
    return Tc + a*x**(-1/b)


p,cov = curve_fit(fittingf,Ns,Tcs)
new_N = np.linspace(np.min(Ns),np.max(Ns),100)
new_Tcs = fittingf(new_N,p[0],p[1])

plt.plot(new_N,new_Tcs)
plt.plot(Ns,Tcs,'x')
plt.plot(plt.xlim(),[Tc,Tc])
plt.title('Critical temperature as a function of lattice size',size=18)
plt.xlabel('N',size=18)
plt.ylabel('Tc',size=18)
plt.show()
print(p[0])
print(p[1])