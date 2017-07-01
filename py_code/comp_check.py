import numpy as np
import matplotlib.pyplot as plt
import pdb
from matplotlib import gridspec

#Using the default values
#Call the files
class_lin_data = np.loadtxt('/Users/penafiel/JPL/class/output/explanatory_mess02_z1_pk.dat', skiprows=4)
ccl_lin_data = np.loadtxt('/Users/penafiel/JPL/CCL-master/data_files/explanatory_mess.dat', skiprows=1)

#Get the values
k_lin = ccl_lin_data[:,0]
ccl_lin = ccl_lin_data[:,1]
#k_lin_h = ccl_lin_data[:,2]
#ccl_lin_h = ccl_lin_data[:,3]
class_k_lin = class_lin_data[:,0]
class_lin = class_lin_data[:,1]


#Might have to multiply by some factor of this thing
h = 0.67556 #Def h value for CLASS
n_s = 0.9619

#Calculate the error
ccl_lin# *= h**3
class_k_lin *= h
class_lin /= h**3
ccl_lin_err = (ccl_lin- class_lin ) / class_lin
gs = gridspec.GridSpec(2,1, height_ratios=[3,1])
fig = plt.figure
ax1 = plt.subplot(gs[0])
ax1.plot(k_lin, ccl_lin , label='CCL, P(k_class)')
#ax1.plot(k_lin_h, ccl_lin_h, label='CCL, P(k_class*h)')
ax1.plot(class_k_lin , class_lin , c='k',label='CLASS, no factor')
#ax1.plot(class_k_lin * h, class_lin, label='Class, k * h')
#ax1.plot(class_k_lin / h, class_lin, label='Class, k / h')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.tick_params(axis ='y', which='both',labeltop=False, labelright=True)

ax2 = plt.subplot(gs[1])
ax2.plot(k_lin,np.abs(ccl_lin_err))
plt.xscale('log')
plt.yscale('log')

plt.savefig('/Users/penafiel/JPL/plots/def_stats.png', format='png')

plt.show()
