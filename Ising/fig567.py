import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate2d
from scipy.interpolate import splrep, splev


from Ferromagnet import * 

#E vs T and C vs T
NT = 100
Ts = np.linspace(0.1*Tc,2*Tc,NT)
M = 250
H = 0
N = 50


spins = reset(N,"up")
#Investigating temperature dependence, zero field
E = np.zeros(NT)
C = np.zeros(NT) #C obtained from fluctuations
mag = np.zeros(NT)

for x in np.arange(500): #Initial step 
    spins = step(spins,0.1*Tc,H)

for m in np.arange(Ts.size):
    T = Ts[m]
    energy_array = np.zeros(M,dtype='float')
    net_mag = np.zeros(M,dtype='float')
    for k in np.arange(M):
        a,b = getEnergy(spins,H)
        energy_array[k] = np.sum(a+b)
        net_mag[k] = np.sum(spins)/N**2
        spins = step(spins,T,H)
    E[m] = np.mean(energy_array[2*M//3:])
    C[m] = np.std(energy_array[2*M//3:])**2/T**2
    mag[m] = np.mean(net_mag[2*M//3:])



fig, ax1 = plt.subplots()
ax1.plot(Ts, E, 'kx')
ax1.set_xlabel('Temperature',size=16)

tck = splrep(Ts,E,s=6*np.abs(np.min(E)))
new_T = np.linspace(np.min(Ts),np.max(Ts),1000)
E_smooth = splev(new_T,tck)
ax1.plot(new_T,E_smooth,'g-')
ax1.set_ylabel('Total energy', color='g',size=16)


ax2 = ax1.twinx()
ax2.plot(Ts,mag,'ro')
ax2.set_ylabel('Net magnetisation', color='r',size=16)

plt.title('Total energy and net magnetisation as a function of temperature',
          size = 18,
          y = 1.03)
plt.show()


#Plot
plt.plot(Ts,C,'x')

C2 = np.diff(E)/np.diff(Ts) #C obtained by differentiating E
plt.plot(reduce(Ts),C2,'o')


C_smooth = np.diff(E_smooth)/np.diff(new_T) #C from interpolated E
plt.plot(reduce(new_T),C_smooth,'-')



plt.legend(['C (fluctuations)', 'C(derivative)','Interpolated'])
plt.ylabel('Heat capacity',size=16)
plt.xlabel('Temperature',size=16)
plt.title('Heat capacity as a function of temperature',size=18)
plt.show()


#Snapshots at various T
Ts = np.array([0.1,0.5,1.5,10])
N = 100
M = 500
for n in np.arange(Ts.size):
    spins = reset(N,"random")
    for m in np.arange(M):
        spins = step(spins,Ts[n]*Tc,0)
    plt.subplot(221+n)
    plt.imshow(spins,interpolation='none',clim=(-1,1))
    plt.axis('off')
    plt.title("T = "+str(Ts[n])+" Tc")
    


plt.show()








    

