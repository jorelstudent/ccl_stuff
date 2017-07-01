import numpy as np
import pyccl as ccl
import matplotlib.pyplot as plt
import pdb

#Call the file from the default ini file from CLASS

h = 0.67556 #Default h value for CLASS
omega_b = 0.022032 / h**2 #Default omega_b value for CLASS
omega_cdm = 0.12038 / h**2 #Default omega_cdm value for CLASS
A_s = 2.215e-9 #Default A_s value for CLASS
n_s = 0.9619 # Default n_s value for CLASS

k_data = np.loadtxt('/Users/penafiel/JPL/class/output/explanatory_mess02_z1_pk.dat', skiprows=4)

k_lin = k_data[:,0]
a=1. #scale factor

cosmo = ccl.Cosmology(Omega_c=omega_cdm, Omega_b=omega_b, h=h, A_s=A_s, n_s=n_s, transfer_function='boltzmann')
#pk_lin_h = ccl.linear_matter_power(cosmo, k_lin * h, a)
pk_lin = ccl.linear_matter_power(cosmo, k_lin * h, a)

k_lin *= h
#k_lin_h = h * k_lin
#k_lin_h_list = k_lin_h.tolist()
#k_lin_h_list = ['k*h'] + k_lin_h_list
k_lin_list = k_lin.tolist()
k_lin_list = ['k'] + k_lin_list


pk_lin_list = pk_lin.tolist()
pk_lin_list = ['pk_lin'] + pk_lin_list
#pk_lin_h_list = pk_lin_h.tolist()
#pk_lin_h_list = ['pkh_lin'] + pk_lin_h_list

np.savetxt('/Users/penafiel/JPL/CCL-master/data_files/explanatory_mess.dat', np.transpose([k_lin_list, pk_lin_list]), fmt='%-25s')



