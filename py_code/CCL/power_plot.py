import numpy as np
import matplotlib.pyplot as plt
import pdb
import glob

#Plots the power spectrum of these things
fig, ax = plt.subplots()
#linear, z = 0
for filename in glob.iglob('/Users/penafiel/JPL/CCL-master/data_files/*.dat'):
    data = np.loadtxt('%s' %filename, skiprows=1)
    k = data[:,0]
    P_lin = data[:,1]
    ax.plot(k,P_lin)

ax.set_xlabel('$k$')
ax.set_ylabel('$P(k)$')
ax.set_title('Matter power spectrum P(k) at redshift z = 0, linear, CCL')
plt.xscale('log')
plt.yscale('log')
fig.savefig('ccl_Pk_z0_lin.png', format='png')
print 'Done with 1'
plt.clf()

fig,ax = plt.subplots()
#nonlin, z = 0
for filename in glob.iglob('/Users/penafiel/JPL/CCL-master/data_files/*.dat'):
    data = np.loadtxt('%s' %filename, skiprows=1)
    k = data[:,0]
    P_nl = data[:,2]
    ax.plot(k,P_nl)

ax.set_xlabel('$k$')
ax.set_ylabel('$P(k)$')
ax.set_title('Matter power spectrum P(k) at redshift z = 0, non linear, CCL')
plt.xscale('log')
plt.yscale('log')
fig.savefig('ccl_Pk_z0_nl.png', format='png')
print 'Done with 1'
plt.clf()

