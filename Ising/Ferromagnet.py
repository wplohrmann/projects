import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate2d
from matplotlib import animation
from scipy.ndimage.measurements import label
from scipy.interpolate import splrep, splev

Tc = 2/np.log(1+np.sqrt(2)) #Theoretical critical temperature

def reset(N,IC):
    if IC=="random":
        return 2*np.random.randint(0,2,size=(N,N))-1 #Each spin randomly up/down
    if IC=="up":
        return np.ones((N,N)) #All up

    

def step2(spins,T,H): #Flips one spin according to the Metropolis algorithm 
    N = spins.shape[0]
    #for n in np.arange(N**2):
    a,b = np.random.randint(0,N,size=2)
    neighbours = spins[np.array([(a+1) % N,a-1,a,a]),np.array([b,b,(b+1) % N,b-1])]
    dIE = np.sum(neighbours)*spins[a,b]
    dFE = H*spins[a,b]
    if np.exp(-(dIE+dFE)/T)>np.random.rand():
        spins[a,b] = -spins[a,b]
    return spins

def step3(spins,T,H): #Does the N^2 in two batches, independently of each other
    
    dFE, dIE = getEnergy(spins,H)
    rand_array = np.random.rand(spins.shape[0],spins.shape[1])
    p_array = np.exp(4*(dFE+dIE)/T)
    flip_array = -2*(p_array>rand_array)+1
    flip_array[1::2,1::2] = 1
    flip_array[0:-1:2,0:-1:2] = 1
    spins = flip_array*spins
    
    dFE, dIE = getEnergy(spins,H)
    rand_array = np.random.rand(spins.shape[0],spins.shape[1])
    p_array = np.exp(4*(dFE+dIE)/T)
    flip_array = -2*(p_array>rand_array)+1
    flip_array[1::2,0:-1:2] = 1
    flip_array[0:-1:2,1::2] = 1
    spins = flip_array*spins
    
    return spins

def step(spins,T,H): #Method 1 using np.roll()
    dFE, dIE = getEnergy2(spins,H)
    rand_array = np.random.rand(spins.shape[0],spins.shape[1])
    p_array = np.exp(4*(dFE+dIE)/T)
    flip_array = -2*(p_array>rand_array)+1
    flip_array[1::2,1::2] = 1
    flip_array[0:-1:2,0:-1:2] = 1
    spins = flip_array*spins
    
    dFE, dIE = getEnergy2(spins,H)
    rand_array = np.random.rand(spins.shape[0],spins.shape[1])
    p_array = np.exp(4*(dFE+dIE)/T)
    flip_array = -2*(p_array>rand_array)+1
    flip_array[1::2,0:-1:2] = 1
    flip_array[0:-1:2,1::2] = 1
    spins = flip_array*spins
    
    return spins
    

def reduce(arr):
    return np.convolve(arr,np.ones(2)/2,mode='valid')

def getEnergy(spins,H): #The energy contribution from each lattice site
    mu = 1
    field_energy = -mu*H*spins 

    J = 1
    #Nearest neighbours (not counting diagonally)
    kernel = np.array([[0,1,0],[1,0,1],[0,1,0]]) 
    
    correlation =  correlate2d(spins,kernel,mode='same',boundary='wrap')
    
    interaction_energy = -J * correlation * spins / 2 
    #Factor of 2 to avoid double counting
    
    return (field_energy,interaction_energy)

def getEnergy2(spins,H):
    mu = 1
    field_energy = -mu*H*spins 

    J = 1
    correlation = spins*(np.roll(spins,1,axis=0) +
                   np.roll(spins,-1,axis=0) +
                   np.roll(spins,1,axis=1) +
                   np.roll(spins,-1,axis=1))
    interaction_energy = -J * correlation / 2 
    #Factor of 2 to avoid double counting
    
    return (field_energy,interaction_energy)
    

def symmetric_max(x,y):
    p = np.polyfit(x,y,2)
    return -p[1]/(2*p[0])

def getTc(T,E): #Using interpolation to smooth E(T), then differentiating
    tck = splrep(T,E,s=1.5*np.abs(np.min(E)))
    new_T = np.linspace(np.min(T),np.max(T),1000)
    E_smooth = splev(new_T,tck)
    
    C = np.diff(E_smooth)/np.diff(new_T)
    return reduce(new_T)[np.argmax(C)]