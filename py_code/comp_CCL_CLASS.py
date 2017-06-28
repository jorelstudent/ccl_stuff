import numpy as np
import matplotlib.pyplot as plt
import pdb
import glob
from matplotlib import gridspec

#This program is to get each trial, and plot the differences for each thing
#While also trying to show the different parameter values
#Also plots the statistics, i.e. how precise our these calculations

#Call the original par_var file, so we can get the trial # easier in the long run, trust
# (Unless there's a more efficient way of calling files)

data = np.genfromtxt('/Users/penafiel/JPL/py_code/par_var.txt', dtype='str', skip_header=1)

#Gets the trial number into an arr
trial_arr = data[:,0]

#Iterates over the trial #
for i in range(len(trial_arr)):
    trial = data[i,0]
    print 'Performing trial %s' %trial

    #Call the CCL data
    ccl_lin_data = np.loadtxt('/Users/penafiel/JPL/CCL-master/data_files/mpk_lin_%s.dat' %trial, skiprows=1)
    ccl_nl_data = np.loadtxt('/Users/penafiel/JPL/CCL-master/data_files/mpk_nl_%s.dat' %trial, skiprows=1)
    #Call the CLASS lin data
    class_lin_data = np.loadtxt('/Users/penafiel/JPL/class/output/lin/trial_lin_%sz1_pk.dat' %trial, skiprows=4)

    #Call the CLASS nl data
    class_nl_data = np.loadtxt('/Users/penafiel/JPL/class/output/nonlin/trial_nonlin_%sz1_pk.dat' %trial, skiprows=4)

    k_lin = ccl_lin_data[:,0]
    k_nl = ccl_nl_data[:,0]
    ccl_lin = ccl_lin_data[:,1]
    ccl_nl = ccl_nl_data[:,1]

    class_k_lin = class_lin_data[:,0]
    class_lin = class_lin_data[:,1]
    class_k_nl = class_nl_data[:,0]
    class_nl = class_nl_data[:,1]

    #Multiply by factors
    #multiply k by some factor of h, CLASS and CCL use different units, ugh
    h = float(data[i,1])

    class_k_lin *= h
    class_lin /= h**3
    class_k_nl *= h
    class_nl /= h**3
    #For lin case
    #Get the error
    ccl_lin_err = (ccl_lin - class_lin) / class_lin
    gs = gridspec.GridSpec(2,1, height_ratios=[3,1])
    fig = plt.figure()
    ax1 = plt.subplot(gs[0])#, rowspan = 2)
    ax1.plot(k_lin, ccl_lin, 'r')
    ax1.plot(class_k_lin ,class_lin, 'b')
    ax1.tick_params(labeltop=False, labelright=True)
    plt.xscale('log')
    plt.yscale('log')

    ax2 = plt.subplot(gs[1])
    ax2.plot(k_lin, np.abs(ccl_lin_err))
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig('/Users/penafiel/JPL/plots/stats_lin_%s.png' %trial, format='png')

    plt.clf()

    #For the nonlin case
    #Get the error
    ccl_nl_err = (ccl_nl - class_nl) / class_nl

    fig = plt.figure()
    gs = gridspec.GridSpec(2,1, height_ratios=[3,1])
    ax1 = plt.subplot(gs[0])#, rowspan=2)
    ax1.plot(k_nl, ccl_nl, 'r')
    ax1.plot(class_k_nl , class_nl , 'b')
    plt.xscale('log')
    plt.yscale('log')
    
    ax2 = plt.subplot(gs[1])
    ax2.plot(k_nl, np.abs(ccl_nl_err))


    plt.xscale('log')
    plt.yscale('log')

    plt.savefig('/Users/penafiel/JPL/plots/stats_nl_%s.png' %trial, format='png')
    plt.clf()

