import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate2d
from scipy.ndimage.measurements import label

from Ferromagnet import * 

#Counting magnetic domains:
def getBiggest(spins,updown):
    ups = (1+updown*spins)/2
    kernel = np.array([[0,1,0],[1,0,1],[0,1,0]]) #Defines connectivity
    
    #Number of neighbours around each up-spin
    ups = ups*correlate2d(ups,kernel,mode='same',boundary='wrap') 

    #Spins only loosely connected are set to zero to break the "spider-web"
    ups[ups!=4] = 0
    
    #Numbers each feature in the array with the same number
    labels,num_features = label(ups) 

    #Calculating sizes from the features:
    sizes = np.zeros(labels.shape)
    sizes1d = np.zeros(num_features)
    biggest = 0
    for n in np.arange(num_features):
        size_of_feature = np.abs(np.sum(ups[labels==n]))
        if size_of_feature > biggest:
            biggest = size_of_feature #Update biggest feature
    return biggest

N = 100
K = 20
Ts = Tc*np.linspace(0.5,2,K)
M = 1000
blob_sizes = np.zeros(K)

for n,T in enumerate(Ts):
    spins = reset(N,"up")
    blobs = np.zeros(M)
    for m in np.arange(M):
        spins = step(spins,T,0)
        minority = -np.sign(np.sum(spins)) #minority spin-state considered only
        blobs[m] = getBiggest(spins,minority)
    blob_sizes[n] = np.average(blobs[2*M//3:])

plt.plot(Ts/Tc,blob_sizes,'-o')
plt.ylabel('Average largest domain size',size=16)
plt.xlabel('Temperature, T/Tc',size=16)
plt.title('Largest domain size at temperatures around Tc',size=18)
plt.show()
