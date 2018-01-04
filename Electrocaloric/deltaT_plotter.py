import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import tkinter as tk
from tkinter import filedialog
import pdb

def colorpicker(n):
    r = np.modf(0.1*n+1.234*n**3+0.1*n**2+3.14159265+(n/10)**5)[0]
    g = np.modf(0.1*n+1.9*n**3+1.3*n**2+0.7+(2*n/10)**5)[0]
    b = np.modf(2.1*n+1.234*n**3+0.1*n**2+5.5*np.sqrt(n)+(n/10)**5)[0]
    return (r,g,b)


root = tk.Tk()
root.withdraw()
filenames = filedialog.askopenfilenames()

#colors = ['Blue','Red','Green','Purple','Grey','Turquoise','Pink','Black']
for n,filename in np.ndenumerate(filenames):
    df_temp = pd.read_csv(filename)
    
    filename = filename.split(r'/')[-1]
    filename = filename.split('.')[0]
    #print(filename)
    x = np.array(df_temp['T/K'])
    y1 = np.array(df_temp['DTP'])
    y2 = np.array(df_temp['DTM'])
    
    
    #REMOVE OUTLIERS FROM y1
    
    
    plt.plot(x,y1,'o-',color=colorpicker(n[0]),label=filename)
 

    
    x = np.array(df_temp['T/K']) #Must restore x
   
    
    #Remove outliers from y2:
    
    
    
    if 'leakage' not in filename:
        plt.plot(x,y2,'o-',color=colorpicker(n[0]),label=filename)

plt.xlabel('Temperature / K')
plt.ylabel('$\Delta$T / K')

handles, labels = plt.gca().get_legend_handles_labels()
i = 1

while i<len(labels):
    if labels[i] in labels[:i]:
        del(labels[i])
        del(handles[i])
    else:
        i +=1
plt.legend(handles, labels)
plt.show()

#while True:
#    dydx = np.diff(y)/np.diff(x)
#    avg_diff = np.mean(np.abs(dydx))
#    max_diff_idx = np.argmax(dydx)
#    if np.abs(dydx[max_diff_idx]) < 3*avg_diff:
#        break
#    y = np.delete(y,max_diff_idx+1)
#    x = np.delete(x,max_diff_idx+1)


