import numpy as np
import pyccl as ccl
import matplotlib.pyplot as plt
import pdb

#Define Cosmological paramters as usual
#Omega_c = CDM fractional density
#Omega_b = baryon fractional density
#A_s = amplitude of the power spectrum
#n_s = tilt of the power spectrum
#h = Hubble Constant

cosmo = ccl.Cosmology(Omega_c=0.27, Omega_b=0.045, h=0.67, A_s=2.1e-9, n_s=0.96, transfer_function='boltzmann')

#Calculate the matter power spectrum

k = np.logspace(-4., 1., 100) #Wavenumber
a = 1. #Scale factor

#Matter power spectrum, lin and nonlin
pk_lin = np.asarray(ccl.linear_matter_power(cosmo, k, a))
pk_nl = np.asarray(ccl.nonlin_matter_power(cosmo, k, a))

plt.plot(k, pk_lin, 'b-')
plt.plot(k, pk_nl, 'r-')
plt.xscale('log')
plt.yscale('log')
plt.savefig('power_spectrum.png', format='png')

#Transforms these to lists
k = k.tolist()
pk_lin = pk_lin.tolist()
pk_nl = pk_nl.tolist()
#Adds a header line
k = ['k'] + k
pk_lin =['pk lin'] + pk_lin
pk_nl = ['pk_nl'] + pk_nl
np.savetxt('power_spec.dat', np.transpose([k, pk_lin, pk_nl]), fmt='%-20s')

#Get the power spectrum normalization, sigma_8
normal = ccl.sigma8(cosmo)

pdb.set_trace()
