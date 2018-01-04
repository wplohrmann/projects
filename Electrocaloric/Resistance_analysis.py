import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from os import listdir
import pdb
import scipy.signal
import scipy.integrate
import scipy.interpolate
import scipy.optimize
import scipy.optimize

save_dir = r'/home/william/Dropbox/Materials Internship/Presentations/Presentation Leakage Analysis/'
directory = r'/home/william/Dropbox/Materials Internship/Data/PMNPT/PMNPT 011 Indirect/PMNPT011/700Vheating2/'

directory_name = directory.split('/')[-2]

def last_first_diff(arr):
    return arr[-1] - arr[0]

def shift_slice(the_slice,n):
    try:
        the_slice = the_slice[0]
    except:
        pass
    return slice(the_slice.start + n, the_slice.stop + n)

def info_loss(arr,n):
    for n in np.arange(n):
        arr = np.correlate(arr,np.ones(2)/2)
    return arr

def force_spacing(arr):
    new_arr = np.array([arr[0]])
    minimum_spacing = 20 #0.5*np.mean(np.diff(np.sort(arr)))
    for a in arr:
        #pdb.set_trace()
        if np.any(np.abs(new_arr-a)<minimum_spacing):
            continue
            print('Discarded')
        new_arr = np.append(new_arr,a)
    return new_arr

def voltage_slice(V,start,stop):
    #Finding the zeros of the driving profile
    
    #IS THIS OKAY?
    shift = np.mean((np.max(V),np.min(V)))
    V = V - shift

    zero_threshold = np.max(V)/50
    indices = np.where(np.abs(V)<zero_threshold)[0]
    zero_indices = force_spacing(indices)
    
    
    try:
        assert zero_indices.size == 7
    except:
        raise ZeroDivisionError
    
    V = np.abs(V)
    
    if start % 2 == 0:
        start_index = zero_indices[start//2]
    if stop % 2 == 0:
        stop_index = zero_indices[stop//2]
    
    
    
    if start % 2 == 1:
        index1 = zero_indices[(start-1)//2]
        index2 = zero_indices[(start+1)//2]
        start_index = index1 + np.argmax(V[index1:index2])
    if stop % 2 == 1:
        index1 = zero_indices[(stop-1)//2]
        index2 = zero_indices[(stop+1)//2]
        stop_index = index1 + np.argmax(V[index1:index2]).astype('int32')
        
    assert stop_index>start_index+5
    
    return np.index_exp[start_index:(stop_index+1)]

def leakage_correction(P,V,t,diagnose=True,no_correction=False,the_slice='upper'):
    #P,V,t are arrays in the same order
    #Units as given. No corrections

    
    #Finding R as a function of t and V
    minor_branch_plus = voltage_slice(V,5,8)
    R_array_plus = find_R(P[minor_branch_plus],V[minor_branch_plus],t[minor_branch_plus])
    R_plus = np.median(R_array_plus)
    
   
    minor_branch_minus = voltage_slice(V,9,12)
    R_array_minus = find_R(P[minor_branch_minus],V[minor_branch_minus],t[minor_branch_minus])
    R_minus = np.median(R_array_minus)
         
    
    #Leakage correction:
    #R = np.where(V>0,R_plus,R_minus)
    R = (R_plus+R_minus)/2

    
    return (P_return,V_return)


def find_R(P,V,t):
    #P,V and t are arrays from V=something to the next time V=something
    minimum_interval = np.round((t[-1]-t[0])*1.1/3).astype('int32')
    DP_array = np.array([])
    VInt_array = np.array([])
    
    for n in np.arange(P.size):
        if n + minimum_interval >= P.size:
            break
        rest = V[n+minimum_interval:]
        closest_ind = np.argmin(np.abs(rest-V[n]))
        closest_ind = closest_ind + n+minimum_interval
#        if np.abs(V[closest_ind]-V[n]) > 2:
#            continue
#            print(V[closest_ind]-V[n])
        
        DP_array = np.append(DP_array,P[closest_ind]-P[n])
        VInt = np.trapz(V[n:closest_ind+1],t[n:closest_ind+1])
        VInt_array = np.append(VInt_array,VInt)
       
        
        
        
    R = VInt_array / DP_array
  
    
    return R



def isNotValid(file,bad_files):
    if file[-3:] != 'tab':
        return True
    if file in bad_files:
        return True
    return False


def extractPVt(filename):
    df_temp = pd.read_table(filename,engine='python')
    P = np.array(df_temp['Measured Polarization'])
    V = np.array(df_temp['#Drive Voltage'])
    t = np.array(df_temp['Time (ms)'])
    
    #sample_area = 0.072938 #in square cm, 111
    sample_area = 0.0133726 #in square cm, 011
    #sample_area = 0.014410  #in square cm, 001
    P = P / sample_area #micro C per cm^2
    P = P * 1e-2 #convert to SI
    
    thickness = 300e-6 #in m
    V = V / thickness #To field instead of voltage
    
    
    return (P,V,t)

def extractT(s):
    s = s.split('/')[-1][8:14]
    T = int(s[:-3]) + int(s[-2:])/100 # for 500V and 700V
    #s = s.split('/')[-1]
    #T = int(s[:3]) + int(s[4:6])/100
    return T




bad_files = []
for file in listdir(directory):
    filename = directory+file
    try:
        P,V,t = extractPVt(filename)
        bla = voltage_slice(V,1,5)
    except ZeroDivisionError:
        bad_files.append(file)


T_array = np.array([])
for file in listdir(directory):
    if isNotValid(file,bad_files):
        continue
    T = extractT(file)
    T_array = np.append(T_array,T)
T_array = np.sort(T_array)

