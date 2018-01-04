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

save_dir = r'/home/william/Dropbox/Materials Internship/Presentations/Presentation 111 take III/'
directory = r'/home/william/Dropbox/Materials Internship/Data/PMNPT/PMNPT 111 Indirect/PMNPT111 Take III/PMNPT111heating3/'

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

    
    
    
    P_leakage = scipy.integrate.cumtrapz(V/R,t)
    P_leakage = np.append(P_leakage,P_leakage[-1])
    P_corrected = P - P_leakage
    
    
    
    
    #upper
    upper_slice = voltage_slice(V,1,2) #Normally 1,2
    
    
    #major_loop
    recentering_slice = voltage_slice(V,1,3)
    
    
    #new_major = np.vstack((,))
    new_major_slice = voltage_slice(V,2,6)
    #P_return = P_corrected[zero_indices[1]:zero_indices[3]]
    #V_return = V[zero_indices[1]:zero_indices[3]]
    
    #All of the loop
    all_slice = np.index_exp[:]
    
    if no_correction:
        print('No leakage correction')
        P_return = P
        
    else:
        P_return = P_corrected
    
    #Recentering
    major_loop = P_corrected[recentering_slice]
    
    shift = np.mean((major_loop[0],major_loop[-1]))
    if np.isnan(shift):
        pdb.set_trace()
    P_return = P_return - shift

    if the_slice == 'upper':
        return_slice = upper_slice
    elif the_slice == 'major':
        return_slice = new_major_slice
    else:
        print(the_slice)
        raise Exception
    
    P_return = P_return[return_slice]
    V_return = V[return_slice]
    
    
    
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

#File diagnosis
def diagnose(P,V,t):
    plt.subplot(211)
    plt.plot(t,V)
    plt.ylim([np.min(V), np.max(V)])
    plt.xlim([np.min(t),np.max(t)])

    plt.subplot(212)
    plt.plot(t,P)
    plt.ylim([np.min(P),np.max(P)])
    plt.xlim([np.min(t),np.max(t)])

    plt.show()



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



#Make sure you use upper_slice
for file in listdir(directory):
    if isNotValid(file,bad_files):
        continue
    filename = directory+file
    T = extractT(filename)
    T_color = (T-np.min(T_array))/(np.max(T_array)-np.min(T_array))
    P,V,t = extractPVt(filename)
    P_new,V_new = leakage_correction(P,V,t)
    plt.plot(V_new,P_new,color=(T_color,T_color*0.3,T_color*0.8))


plt.title(directory_name)
plt.xlabel('E / V m$^{-1}$')
plt.ylabel('P / C m$^{-2}$')
plt.xlim([0,2.5e6])
plt.ylim([0,0.9])
plt.savefig(save_dir+directory_name+'upper.png',dpi=300)
plt.show()


#Plot 5 loops across the temperature range
loops = T_array[::T_array.size//5]
for file in listdir(directory):
    if isNotValid(file,bad_files):
        continue
    filename = directory+file
    T = extractT(filename)
    if T not in loops:
        continue
    T_color = (T-np.min(T_array))/(np.max(T_array)-np.min(T_array))
    P,V,t = extractPVt(filename)
    P_new,V_new = leakage_correction(P,V,t,no_correction=False,the_slice='major')
    plt.plot(V_new,P_new,color=(T_color,T_color*0.3,T_color*0.8))



plt.title(directory_name)
plt.xlabel('E / V m$^{-1}$')
plt.ylabel('P / C m$^{-2}$')
plt.xlim([-2.5e6,2.5e6])
plt.ylim([-0.9,0.9])
plt.savefig(save_dir+directory_name+'loops.png',dpi=300)
plt.show()



#Find absolute least extrema

V_max_array = np.array([]) #The maximum values of V in single files 
V_min_array = np.array([]) #The minimum ---------------------------
for file in listdir(directory):
    if isNotValid(file,bad_files):
        continue
    filename = directory+file
    P,V,t = extractPVt(filename)
    P_new,V_new = leakage_correction(P,V,t)
    
    V_max_array = np.append(V_max_array,np.max(V_new))
    V_min_array = np.append(V_min_array,np.min(V_new))


V_lower = np.max(V_min_array)
V_upper = np.min(V_max_array)


no_of_points = 200
V_range = np.linspace(V_lower,V_upper,no_of_points)
T_vec,V_vec = np.meshgrid(T_array,V_range)

P_mesh = np.empty(T_vec.shape)

for file in listdir(directory):
    if isNotValid(file,bad_files):
        continue
    filename = directory+file
    P,V,t = extractPVt(filename)
    P_new,V_new = leakage_correction(P,V,t)    
    
    
    T = extractT(file)
    n = np.where(T_array==T)[0][0]
    assert np.max(V_range) <= np.max(V_new)
    assert np.min(V_range) >= np.min(V_new)

    sorted_indices = np.argsort(V_new)
    V_new = V_new[sorted_indices]
    P_new = P_new[sorted_indices]
    P_mesh[:,n] = np.interp(V_range,V_new,P_new)
    

no_of_T_points = 200

T_new = np.linspace(T_vec[0,0],T_vec[0,-1],no_of_T_points)
P_mesh_smooth = np.empty((P_mesh.shape[0],no_of_T_points))
T_vec_smooth,V_vec_smooth = np.meshgrid(T_new,V_range)

for k in np.arange(P_mesh.shape[0]):
    P = P_mesh[k]
    T = T_vec[k]    
    tck = scipy.interpolate.splrep(T,P,s=0.0029)
    P_new = scipy.interpolate.splev(T_new,tck)
    if np.any(np.isnan(P_new)):
        pdb.set_trace()
    P_mesh_smooth[k] = P_new





#P-T plots at different fields
def plotPT():
    no_of_lines_to_show = 5
    for n in np.arange(P_mesh.shape[0]):
        if n % (P_mesh.shape[0] // no_of_lines_to_show) != 0:
            continue
        my_color = (np.random.rand(),np.random.rand(),np.random.rand())
        plt.plot(T_vec[n],100*P_mesh[n], 'o',color=my_color)
        plt.plot(T_vec_smooth[n],100*P_mesh_smooth[n],'-',color=my_color)

    plt.title(directory_name+' Max V: '+str(V_upper*300e-6))
    plt.xlabel('T / K')
    plt.ylabel('P / $\mu$ C cm$^{-2}$')
    plt.xlim([370,530])
    plt.ylim([0,90])
    plt.savefig(save_dir+directory_name+'PT.png')
plotPT()
plt.show()



#Taking the derivative with respect to T (Confirmed)
dPdT = np.diff(P_mesh_smooth,axis=1) / np.diff(T_vec_smooth,axis=1)
T_vec_d = scipy.signal.convolve2d(T_vec_smooth,[np.ones(2)/2],mode='valid')
V_vec_d =  scipy.signal.convolve2d(V_vec_smooth,[np.ones(2)/2],mode='valid')



#Integrating dPdT wrt. E' (dummy) from  E_lower to E (NOT Confirmed)
assert np.all(np.diff(V_vec_d[:,0]) > 0) #Make sure E is always increasing
P_integrated = scipy.integrate.cumtrapz(dPdT,V_vec_d,axis=0)
V_vec_int = scipy.signal.convolve2d(V_vec_d,np.ones((2,1))/2,mode='valid')
T_vec_int = scipy.signal.convolve2d(T_vec_d,np.ones((2,1))/2,mode='valid')
rho = 8100 #Only for PMNPT!
DS = P_integrated / rho



no_of_lines_to_show = 10
plt.subplot(211)
plotPT()
plt.xlim([np.min(T_vec_int),np.max(T_vec_int)])
plt.subplot(212)
for n in np.arange(P_integrated.shape[0]):
    if n % (P_integrated.shape[0] // no_of_lines_to_show) != 0:
        continue
    plt.plot(T_vec_int[n],DS[n],'o-')

plt.xlabel('T/K')
plt.ylabel('$\Delta S$ / J K$^{-1}$ kg$^{-1}$')
#plt.ylim([-8,10])
plt.xlim([np.min(T_vec_int),np.max(T_vec_int)])

plt.show()
