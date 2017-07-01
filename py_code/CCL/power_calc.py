import numpy as np
import pyccl as ccl
import glob
import matplotlib.pyplot as plt
import pdb

#We are going to get the numbers generated from the gen_par.py file for CLASS
#They are the same variables, so all we need to do is rename them to the proper name

#Cal the files as string, make the rest floats later
data = np.genfromtxt('/Users/penafiel/JPL/data/par_stan.txt', dtype='str', skip_header=1)

#This gets the trial number into an arr
trial_arr = data[:,0]

#Perform the calculation for each set of parameters
#We will store both the linear and nonlinear cases

#Initialize variables that won't change

#k = np.logspace(-5., 1., 100) #Wavenumber
a = 1. #Scale factor
#k_list = k.tolist()
#k_list = ['k'] + k_list
"""
#Compare 00007 and 00008
h = float(data[7,1])
omega_b = float(data[7,2])
omega_cdm = float(data[7,3])
A_s = float(data[7,4])
n_s = float(data[7,5])
cosmo = ccl.Cosmology(Omega_c=omega_cdm, Omega_b=omega_b, h=h, A_s=A_s, n_s=n_s, transfer_function='boltzmann')
print cosmo
pk_lin = ccl.linear_matter_power(cosmo, k , a)
pk_nl = ccl.nonlin_matter_power(cosmo, k, a)

#Check if 00008 is working
h = float(data[8,1])
omega_b = float(data[8,2])
omega_cdm = float(data[8,3])
A_s = float(data[8,4])
n_s = float(data[8,5])
cosmo_1 = ccl.Cosmology(Omega_c=omega_cdm, Omega_b=omega_b, h=h, A_s=A_s, n_s=n_s, transfer_function='boltzmann')
print cosmo_1
#pk_lin = ccl.linear_matter_power(cosmo_1, k , a)
#pk_nl = ccl.nonlin_matter_power(cosmo_1, k, a)
"""
#pdb.set_trace()
for i in range(len(trial_arr)):
    trial = data[i,0]
    print 'Performing trial %s' %trial
    h = float(data[i,1])
    omega_b = float(data[i,2]) / h**2
    omega_cdm = float(data[i,3]) / h**2
    A_s = float(data[i,4])
    n_s = float(data[i,5])
    #Get the k values, directly from CLASS
    k_lin_data = np.loadtxt('/Users/penafiel/JPL/class/output/lin/lhs_lin_%sz1_pk.dat' %trial, skiprows=4)
    k_nl_data = np.loadtxt('/Users/penafiel/JPL/class/output/nonlin/lhs_nonlin_%sz1_pk.dat' %trial, skiprows=4)

    k_lin = k_lin_data[:,0]
    k_nl = k_nl_data[:,0]
    k_lin *= h
    k_nl *= h
    cosmo = ccl.Cosmology(Omega_c=omega_cdm, Omega_b=omega_b, h=h, A_s=A_s, n_s=n_s, transfer_function='boltzmann')
    print 'Check 1'
    #if h < 0.56:
    #    print 'Skipped trial %s' %trial, h
    #    continue
    #Matter power spectrum for lin and nonlin
    pk_lin = ccl.linear_matter_power(cosmo, k_lin, a)

    pk_nl = ccl.nonlin_matter_power(cosmo, k_nl, a)

    print 'Check 333'
    #Transform these into lists and add header lines
    k_lin_list = k_lin.tolist()
    k_lin_list = ['k'] + k_lin_list

    k_nl_list = k_nl.tolist()
    k_nl_list = ['k'] + k_nl_list
    pk_lin_list = pk_lin.tolist()
    pk_nl_list = pk_nl.tolist()
    pk_lin_list =['pk_lin'] + pk_lin_list
    pk_nl_list = ['pk_nl'] + pk_nl_list

    np.savetxt('/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_lin_%s.dat' %trial, np.transpose([k_lin_list, pk_lin_list]), fmt='%-25s')
    np.savetxt('/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_nl_%s.dat' %trial, np.transpose([k_nl_list, pk_nl_list]), fmt='%-25s')
    
    del pk_lin_list[:]
    del pk_nl_list[:]
    del pk_lin
    del pk_nl
    del cosmo


