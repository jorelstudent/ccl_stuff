import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import corner
from corner_source import * #Note: This version of corner is edited so that it does scatter
from pandas import *
import pdb
import glob

#This program's aim is to look at each trial and find the places where the validity fails
#These will be based on the condition for clustering
#Clustering values  only affect those in the range of [1.e-2,0.2]
#So we're going to bin our k values according to
#Ultra-large scales:[1e-4, 1e-2]
#Linear scales:[1e-2, 0.1]
#Quasi-linear:[0.1,1.0]
#Each bin we're going to assign a number for badly the points reach the 1e-4 threshold for each bin

#Also the number for failures can either include clustering regime only or not
thres = 1.e-4 #Threshold for number of failures
clustering_only = False #Only counts failures if inside the clustering regime

ultra_scale_min = 1e-4 #Minimum for the ultra-large scales
ultra_scale_max = 1e-2 #Maximum for the ultra-large scales
lin_scale_min = 1e-2 #Min for the linear scales
lin_scale_max = 1e-1 #Max for the linear scales
quasi_scale_min = 1e-1 #Min for the quasi-lin scales
quasi_scale_max = 1.0 #Max for the quasi-lin scales


cluster_reg_min = 1e-2 #Min for the cluster regime
cluster_reg_max = 0.2 # Max for the cluster regime

#Call the original par_stan file, so we can get the trial # (easier in the long run, trust)

data = np.loadtxt('/Users/penafiel/JPL/data/par_stan1.csv', skiprows=1)


#Get the trial number into an arr
trial_arr = data[:,0]

#Create arrays that will be filled in the loop over trials
#Total of the wights
tot_tot_lin = []
tot_tot_nl = []
tot_tot_lin_pre = []
tot_tot_nl_pre = []

#######################
#                     #
#PLOTTING SUMMARY STAT#
#                     #
#######################

#Iterates over the trial #:
for i in range(len(trial_arr)):
	trial = data[i,0]
	print 'Performing trial %05d' %trial

	z_vals = ['1', '2', '3', '4', '5', '6']

	#Gonna generate an array of arrays, with each row corresponding to a different z value
	#Each columns will correspond to a different bins of k_values
	tot_lin = []

	#For list of lists
	tot_lin_ll = []

	for j in range(len(z_vals)):
		z_val = z_vals[j]
		z_path ='_z%s.dat' %z_val
		print 'Performing z_val = ', z_val
		
		#For ease in iterating over different z values we use string manipulation
		stats_lin_path = '/Users/penafiel/JPL/stats/lhs_mpk_err_lin_%05d' %trial

		#Adds the z_path
		stats_lin_path += z_path

		#Calls the data 
		stats_lin_data = np.loadtxt(stats_lin_path, skiprows=1)

		stats_lin_k = stats_lin_data[:,0]
		stats_lin_err = stats_lin_data[:,1]

		#Create arrays that will be used to fill the complete summary arrays
		tot_lin_z = []

		#For list of lists
		tot_lin_z_ll = []

		#We perform a loop that looks into the bins for k
		#Doing this for lin
		#Much easier than doing a for loop because of list comprehension ALSO FASTER
		tot_ultrasc = 0 #initialize value for ultra large scales
		tot_linsc = 0 #initialize for lin scales
		tot_quasisc = 0 #initialize for quasi lin scales

		#k has to fall in the proper bins
		aux_k_ultra = (stats_lin_k >= ultra_scale_min) & (stats_lin_k < ultra_scale_max)
		aux_k_lin = (stats_lin_k >= lin_scale_min) & (stats_lin_k < lin_scale_max)
		aux_k_quasi = (stats_lin_k >= quasi_scale_min) & (stats_lin_k <= quasi_scale_max)

		#Looks at only the regime where clustering affects it
		if clustering_only == True:
			aux_cluster_ultra = (stats_lin_k[aux_k_ultra] > cluster_reg_min) & (stats_lin_k[aux_k_ultra] < cluster_reg_max)
			aux_cluster_lin = (stats_lin_k[aux_k_lin] > cluster_reg_min) & (stats_lin_k[aux_k_lin] < cluster_reg_max)
			aux_cluster_quasi = (stats_lin_k[aux_k_quasi] > cluster_reg_min) & (stats_lin_k[aux_k_quasi] < cluster_reg_max)
			
			#Calculate the weights i.e. how badly has this bin failed
			w_ultra = np.log10(np.abs((stats_lin_err[aux_k_ultra])[aux_cluster_ultra]) / thres)
			w_lin = np.log10(np.abs((stats_lin_err[aux_k_lin])[aux_cluster_lin]) / thres)
			w_quasi = np.log10(np.abs((stats_lin_err[aux_k_quasi])[aux_cluster_quasi]) / thres)

			#Make all the negative values = 0, since that means they didn't pass the threshold
			aux_ultra_neg = w_ultra < 0.
			aux_lin_neg = w_lin < 0.
			aux_quasi_neg = w_quasi < 0.

			w_ultra[aux_ultra_neg] = 0
			w_lin[aux_lin_neg] = 0
			w_quasi[aux_quasi_neg] = 0

			tot_ultrasc = np.sum(w_ultra)
			tot_linsc = np.sum(w_lin)
			tot_quasisc = np.sum(w_quasi)
		#calculates imprecision in any regime
		if clustering_only == False:
			#caluclate the weights i.e. how badly has this bin failed
			w_ultra = np.log10(np.abs(stats_lin_err[aux_k_ultra]) / thres)
			w_lin = np.log10(np.abs(stats_lin_err[aux_k_lin]) / thres)
			w_quasi = np.log10(np.abs(stats_lin_err[aux_k_quasi]) / thres)

			#Make all the negative values = 0, since that means they didn't pass the threshold
			aux_ultra_neg = w_ultra < 0.
			aux_lin_neg = w_lin < 0.
			aux_quasi_neg = w_quasi < 0.

			w_ultra[aux_ultra_neg] = 0
			w_lin[aux_lin_neg] = 0
			w_quasi[aux_quasi_neg] = 0

			#calculate the totals
			tot_ultrasc = np.sum(w_ultra)
			tot_linsc = np.sum(w_lin)
			tot_quasisc = np.sum(w_quasi)
		
		
		#Append these values to our z summary stat
		#For list only
		tot_lin_z = np.append(tot_lin_z, tot_ultrasc)
		tot_lin_z = np.append(tot_lin_z, tot_linsc)
		tot_lin_z = np.append(tot_lin_z, tot_quasisc)

		#For list of lists
		tot_lin_z_ll.append(tot_ultrasc)
		tot_lin_z_ll.append(tot_linsc)
		tot_lin_z_ll.append(tot_quasisc)

		#Append these values for the general z stat
		#For list only
		tot_lin = np.append(tot_lin, tot_lin_z)
		#For list of lists
		tot_lin_ll.append(tot_lin_z_ll)

	#Generate our z values for plotting
	z_actual = range(len(z_vals))
	z_arr = np.float_(np.asarray(z_actual))
	z_arr *= 0.5
	z = []
	z_ll = []

	for j in range(len(z_actual)):
		z_full = np.full(len(tot_lin_ll[0]), z_arr[j])
		z = np.append(z,z_full)
		z_ll.append(z_full)

	#Generate an array of the midpoints of the bins
	ultra_scale_bin = (ultra_scale_max + ultra_scale_min) / 2
	lin_scale_bin = (lin_scale_max + lin_scale_min) / 2
	quasi_scale_bin = (quasi_scale_max + quasi_scale_min) / 2

	k_bin = [ultra_scale_bin, lin_scale_bin, quasi_scale_bin]
	k_list = k_bin * len(z_vals)

	#Doing it the pandas way
	k_words = ['Ultra-large', 'Linear', 'Quasi Lin']

	#Generates the data frame
	df = DataFrame(tot_lin_ll, index=z_arr, columns=k_words)

	#Plots the colors
	pc = plt.pcolor(df)

	#Changes the ticks
	plt.yticks(np.arange(0.5, len(df.index),1), df.index)
	plt.xticks(np.arange(0.5, len(df.columns),1), df.columns)
	plt.xlabel('Scales')
	plt.ylabel('$z$')

	#Generate the color bar
	cb = plt.colorbar(pc)
	cb.set_label('How badly it failed')
	plt.title('Scales vs $z$, Threshold = %d' %thres)

	plt.savefig('/Users/penafiel/JPL/sum_stats/sum_stats_lin_%05d.png' %trial, format='png')
	plt.clf()

	tot_tot_lin = np.append(tot_tot_lin, np.sum(tot_lin))

	print 'Performing this for nonlin'
	#Gonna generate an array of arrays, with each row corresponding to a different z value
	#Each columns will correspond to a different bins of k_values
	tot_nl = []

	#For list of lists
	tot_nl_ll = []

	for j in range(len(z_vals)):
		z_val = z_vals[j]
		z_path ='_z%s.dat' %z_val
		print 'Performing z_val = ', z_val
		
		#For ease in iterating over different z values we use string manipulation
		stats_nl_path = '/Users/penafiel/JPL/stats/lhs_mpk_err_nl_%05d' %trial

		#Adds the z_path
		stats_nl_path += z_path

		#Calls the data 
		stats_nl_data = np.loadtxt(stats_nl_path, skiprows=1)

		stats_nl_k = stats_nl_data[:,0]
		stats_nl_err = stats_nl_data[:,1]

		#Create arrays that will be used to fill the complete summary arrays
		tot_nl_z = []

		#For list of lists
		tot_nl_z_ll = []

		#We perform a loop that looks into the bins for k
		#Doing this for lin
		#Much easier than doing a for loop because of list comprehension ALSO FASTER
		tot_ultra = 0 #initialize value for ultra large scales
		tot_lin = 0 #initialize for lin scales
		tot_quasi = 0 #initialize for quasi lin scales

		#k has to fall in the proper bins
		aux_k_ultra = (stats_nl_k >= ultra_scale_min) & (stats_nl_k < ultra_scale_max)
		aux_k_lin = (stats_nl_k >= lin_scale_min) & (stats_nl_k < lin_scale_max)
		aux_k_quasi = (stats_nl_k >= quasi_scale_min) & (stats_nl_k <= quasi_scale_max)

		#Looks at only the regime where clustering affects it
		if clustering_only == True:
			aux_cluster_ultra = (stats_nl_k[aux_k_ultra] > cluster_reg_min) & (stats_nl_k[aux_k_ultra] < cluster_reg_max)
			aux_cluster_lin = (stats_nl_k[aux_k_lin] > cluster_reg_min) & (stats_nl_k[aux_k_lin] < cluster_reg_max)
			aux_cluster_quasi = (stats_nl_k[aux_k_quasi] > cluster_reg_min) & (stats_nl_k[aux_k_quasi] < cluster_reg_max)
			
			#Calculate the weights i.e. how badly has this bin failed
			w_ultra = np.log10(np.abs((stats_nl_err[aux_k_ultra])[aux_cluster_ultra]) / thres)
			w_lin = np.log10(np.abs((stats_nl_err[aux_k_lin])[aux_cluster_lin]) / thres)
			w_quasi = np.log10(np.abs((stats_nl_err[aux_k_quasi])[aux_cluster_quasi]) / thres)

			#Make all the negative values = 0, since that means they didn't pass the threshold
			aux_ultra_neg = w_ultra < 0.
			aux_lin_neg = w_lin < 0.
			aux_quasi_neg = w_quasi < 0.

			w_ultra[aux_ultra_neg] = 0
			w_lin[aux_lin_neg] = 0
			w_quasi[aux_quasi_neg] = 0

			tot_ultra = np.sum(w_ultra)
			tot_lin = np.sum(w_lin)
			tot_quasi = np.sum(w_quasi)
		#calculates imprecision in any regime
		if clustering_only == False:
			#caluclate the weights i.e. how badly has this bin failed
			w_ultra = np.log10(np.abs(stats_nl_err[aux_k_ultra]) / thres)
			w_lin = np.log10(np.abs(stats_nl_err[aux_k_lin]) / thres)
			w_quasi = np.log10(np.abs(stats_nl_err[aux_k_quasi]) / thres)

			#Make all the negative values = 0, since that means they didn't pass the threshold
			aux_ultra_neg = w_ultra < 0.
			aux_lin_neg = w_lin < 0.
			aux_quasi_neg = w_quasi < 0.

			w_ultra[aux_ultra_neg] = 0
			w_lin[aux_lin_neg] = 0
			w_quasi[aux_quasi_neg] = 0

			#calculate the totals
			tot_ultra = np.sum(w_ultra)
			tot_lin = np.sum(w_lin)
			tot_quasi = np.sum(w_quasi)
		
		
		#Append these values to our z summary stat
		#For list only
		tot_nl_z = np.append(tot_nl_z, tot_ultra)
		tot_nl_z = np.append(tot_nl_z, tot_lin)
		tot_nl_z = np.append(tot_nl_z, tot_quasi)

		#For list of lists
		tot_nl_z_ll.append(tot_ultra)
		tot_nl_z_ll.append(tot_lin)
		tot_nl_z_ll.append(tot_quasi)

		#Append these values for the general z stat
		#For list only
		tot_nl = np.append(tot_nl, tot_nl_z)
		#For list of lists
		tot_nl_ll.append(tot_nl_z_ll)

	#Generate our z values for plotting
	z_actual = range(len(z_vals))
	z_arr = np.float_(np.asarray(z_actual))
	z_arr *= 0.5
	z = []
	z_ll = []

	for j in range(len(z_actual)):
		z_full = np.full(len(tot_nl_ll[0]), z_arr[j])
		z = np.append(z,z_full)
		z_ll.append(z_full)

	#Generate an array of the midpoints of the bins
	ultra_scale_bin = (ultra_scale_max + ultra_scale_min) / 2
	lin_scale_bin = (lin_scale_max + lin_scale_min) / 2
	quasi_scale_bin = (quasi_scale_max + quasi_scale_min) / 2

	k_bin = [ultra_scale_bin, lin_scale_bin, quasi_scale_bin]
	k_list = k_bin * len(z_vals)

	#Doing it the pandas way
	k_words = ['Ultra-large', 'Linear', 'Quasi Lin']

	#Generates the data frame
	df = DataFrame(tot_nl_ll, index=z_arr, columns=k_words)

	#Plots the colors
	pc = plt.pcolor(df)

	#Changes the ticks
	plt.yticks(np.arange(0.5, len(df.index),1), df.index)
	plt.xticks(np.arange(0.5, len(df.columns),1), df.columns)
	plt.xlabel('Scales')
	plt.ylabel('$z$')

	#Generate the color bar
	cb = plt.colorbar(pc)
	cb.set_label('How badly it failed')
	plt.title('Scales vs $z$, Threshold = %d' %thres)

	plt.savefig('/Users/penafiel/JPL/sum_stats/sum_stats_nl_%05d.png' %trial, format='png')
	plt.clf()

	tot_tot_nl = np.append(tot_tot_nl,np.sum(tot_nl))




	print 'Performing this for lin precise'
	#Gonna generate an array of arrays, with each row corresponding to a different z value
	#Each columns will correspond to a different bins of k_values
	tot_lin_pre = []

	#For list of lists
	tot_lin_pre_ll = []

	for j in range(len(z_vals)):
		z_val = z_vals[j]
		z_path ='_z%s.dat' %z_val
		print 'Performing z_val = ', z_val
		
		#For ease in iterating over different z values we use string manipulation
		stats_lin_pre_path = '/Users/penafiel/JPL/stats/lhs_mpk_err_lin_pk_%05d' %trial

		#Adds the z_path
		stats_lin_pre_path += z_path

		#Calls the data 
		stats_lin_pre_data = np.loadtxt(stats_lin_pre_path, skiprows=1)

		stats_lin_pre_k = stats_lin_pre_data[:,0]
		stats_lin_pre_err = stats_lin_pre_data[:,1]

		#Create arrays that will be used to fill the complete summary arrays
		tot_lin_pre_z = []

		#For list of lists
		tot_lin_pre_z_ll = []

		#We perform a loop that looks into the bins for k
		#Doing this for lin
		#Much easier than doing a for loop because of list comprehension ALSO FASTER
		tot_ultra = 0 #initialize value for ultra large scales
		tot_lin = 0 #initialize for lin scales
		tot_quasi = 0 #initialize for quasi lin scales

		#k has to fall in the proper bins
		aux_k_ultra = (stats_lin_pre_k >= ultra_scale_min) & (stats_lin_pre_k < ultra_scale_max)
		aux_k_lin = (stats_lin_pre_k >= lin_scale_min) & (stats_lin_pre_k < lin_scale_max)
		aux_k_quasi = (stats_lin_pre_k >= quasi_scale_min) & (stats_lin_pre_k <= quasi_scale_max)

		#Looks at only the regime where clustering affects it
		if clustering_only == True:
			aux_cluster_ultra = (stats_lin_pre_k[aux_k_ultra] > cluster_reg_min) & (stats_lin_pre_k[aux_k_ultra] < cluster_reg_max)
			aux_cluster_lin = (stats_lin_pre_k[aux_k_lin] > cluster_reg_min) & (stats_lin_pre_k[aux_k_lin] < cluster_reg_max)
			aux_cluster_quasi = (stats_lin_pre_k[aux_k_quasi] > cluster_reg_min) & (stats_lin_pre_k[aux_k_quasi] < cluster_reg_max)
			
			#Calculate the weights i.e. how badly has this bin failed
			w_ultra = np.log10(np.abs((stats_lin_pre_err[aux_k_ultra])[aux_cluster_ultra]) / thres)
			w_lin = np.log10(np.abs((stats_lin_pre_err[aux_k_lin])[aux_cluster_lin]) / thres)
			w_quasi = np.log10(np.abs((stats_lin_pre_err[aux_k_quasi])[aux_cluster_quasi]) / thres)

			#Make all the negative values = 0, since that means they didn't pass the threshold
			aux_ultra_neg = w_ultra < 0.
			aux_lin_neg = w_lin < 0.
			aux_quasi_neg = w_quasi < 0.

			w_ultra[aux_ultra_neg] = 0
			w_lin[aux_lin_neg] = 0
			w_quasi[aux_quasi_neg] = 0

			tot_ultra = np.sum(w_ultra)
			tot_lin = np.sum(w_lin)
			tot_quasi = np.sum(w_quasi)
		#calculates imprecision in any regime
		if clustering_only == False:
			#caluclate the weights i.e. how badly has this bin failed
			w_ultra = np.log10(np.abs(stats_lin_pre_err[aux_k_ultra]) / thres)
			w_lin = np.log10(np.abs(stats_lin_pre_err[aux_k_lin]) / thres)
			w_quasi = np.log10(np.abs(stats_lin_pre_err[aux_k_quasi]) / thres)

			#Make all the negative values = 0, since that means they didn't pass the threshold
			aux_ultra_neg = w_ultra < 0.
			aux_lin_neg = w_lin < 0.
			aux_quasi_neg = w_quasi < 0.

			w_ultra[aux_ultra_neg] = 0
			w_lin[aux_lin_neg] = 0
			w_quasi[aux_quasi_neg] = 0

			#calculate the totals
			tot_ultra = np.sum(w_ultra)
			tot_lin = np.sum(w_lin)
			tot_quasi = np.sum(w_quasi)
		
		
		#Append these values to our z summary stat
		#For list only
		tot_lin_pre_z = np.append(tot_lin_pre_z, tot_ultra)
		tot_lin_pre_z = np.append(tot_lin_pre_z, tot_lin)
		tot_lin_pre_z = np.append(tot_lin_pre_z, tot_quasi)

		#For list of lists
		tot_lin_pre_z_ll.append(tot_ultra)
		tot_lin_pre_z_ll.append(tot_lin)
		tot_lin_pre_z_ll.append(tot_quasi)

		#Append these values for the general z stat
		#For list only
		tot_lin_pre = np.append(tot_lin_pre, tot_lin_pre_z)
		#For list of lists
		tot_lin_pre_ll.append(tot_lin_pre_z_ll)

	#Generate our z values for plotting
	z_actual = range(len(z_vals))
	z_arr = np.float_(np.asarray(z_actual))
	z_arr *= 0.5
	z = []
	z_ll = []

	for j in range(len(z_actual)):
		z_full = np.full(len(tot_lin_pre_ll[0]), z_arr[j])
		z = np.append(z,z_full)
		z_ll.append(z_full)

	#Generate an array of the midpoints of the bins
	ultra_scale_bin = (ultra_scale_max + ultra_scale_min) / 2
	lin_scale_bin = (lin_scale_max + lin_scale_min) / 2
	quasi_scale_bin = (quasi_scale_max + quasi_scale_min) / 2

	k_bin = [ultra_scale_bin, lin_scale_bin, quasi_scale_bin]
	k_list = k_bin * len(z_vals)

	#Doing it the pandas way
	k_words = ['Ultra-large', 'Linear', 'Quasi Lin']

	#Generates the data frame
	df = DataFrame(tot_lin_pre_ll, index=z_arr, columns=k_words)

	#Plots the colors
	pc = plt.pcolor(df)

	#Changes the ticks
	plt.yticks(np.arange(0.5, len(df.index),1), df.index)
	plt.xticks(np.arange(0.5, len(df.columns),1), df.columns)
	plt.xlabel('Scales')
	plt.ylabel('$z$')

	#Generate the color bar
	cb = plt.colorbar(pc)
	cb.set_label('How badly it failed')
	plt.title('Scales vs $z$, Threshold = %d' %thres)

	plt.savefig('/Users/penafiel/JPL/sum_stats/sum_stats_lin_pre_%05d.png' %trial, format='png')
	plt.clf()
	
	tot_tot_lin_pre = np.append(tot_tot_lin_pre, np.sum(tot_lin_pre))



	print 'Performing this for nonlin precision'
	#Gonna generate an array of arrays, with each row corresponding to a different z value
	#Each columns will correspond to a different bins of k_values
	tot_nl_pre = []

	#For list of lists
	tot_nl_pre_ll = []

	for j in range(len(z_vals)):
		z_val = z_vals[j]
		z_path ='_z%s.dat' %z_val
		print 'Performing z_val = ', z_val
		
		#For ease in iterating over different z values we use string manipulation
		stats_nl_pre_path = '/Users/penafiel/JPL/stats/lhs_mpk_err_nl_pk_%05d' %trial

		#Adds the z_path
		stats_nl_pre_path += z_path

		#Calls the data 
		stats_nl_pre_data = np.loadtxt(stats_nl_pre_path, skiprows=1)

		stats_nl_pre_k = stats_nl_pre_data[:,0]
		stats_nl_pre_err = stats_nl_pre_data[:,1]

		#Create arrays that will be used to fill the complete summary arrays
		tot_nl_pre_z = []

		#For list of lists
		tot_nl_pre_z_ll = []

		#We perform a loop that looks into the bins for k
		#Doing this for lin
		#Much easier than doing a for loop because of list comprehension ALSO FASTER
		tot_ultra = 0 #initialize value for ultra large scales
		tot_lin = 0 #initialize for lin scales
		tot_quasi = 0 #initialize for quasi lin scales

		#k has to fall in the proper bins
		aux_k_ultra = (stats_nl_pre_k >= ultra_scale_min) & (stats_nl_pre_k < ultra_scale_max)
		aux_k_lin = (stats_nl_pre_k >= lin_scale_min) & (stats_nl_pre_k < lin_scale_max)
		aux_k_quasi = (stats_nl_pre_k >= quasi_scale_min) & (stats_nl_pre_k <= quasi_scale_max)

		#Looks at only the regime where clustering affects it
		if clustering_only == True:
			aux_cluster_ultra = (stats_nl_pre_k[aux_k_ultra] > cluster_reg_min) & (stats_nl_pre_k[aux_k_ultra] < cluster_reg_max)
			aux_cluster_lin = (stats_nl_pre_k[aux_k_lin] > cluster_reg_min) & (stats_nl_pre_k[aux_k_lin] < cluster_reg_max)
			aux_cluster_quasi = (stats_nl_pre_k[aux_k_quasi] > cluster_reg_min) & (stats_nl_pre_k[aux_k_quasi] < cluster_reg_max)
			
			#Calculate the weights i.e. how badly has this bin failed
			w_ultra = np.log10(np.abs((stats_nl_pre_err[aux_k_ultra])[aux_cluster_ultra]) / thres)
			w_lin = np.log10(np.abs((stats_nl_pre_err[aux_k_lin])[aux_cluster_lin]) / thres)
			w_quasi = np.log10(np.abs((stats_nl_pre_err[aux_k_quasi])[aux_cluster_quasi]) / thres)

			#Make all the negative values = 0, since that means they didn't pass the threshold
			aux_ultra_neg = w_ultra < 0.
			aux_lin_neg = w_lin < 0.
			aux_quasi_neg = w_quasi < 0.

			w_ultra[aux_ultra_neg] = 0
			w_lin[aux_lin_neg] = 0
			w_quasi[aux_quasi_neg] = 0

			tot_ultra = np.sum(w_ultra)
			tot_lin = np.sum(w_lin)
			tot_quasi = np.sum(w_quasi)
		#calculates imprecision in any regime
		if clustering_only == False:
			#caluclate the weights i.e. how badly has this bin failed
			w_ultra = np.log10(np.abs(stats_nl_pre_err[aux_k_ultra]) / thres)
			w_lin = np.log10(np.abs(stats_nl_pre_err[aux_k_lin]) / thres)
			w_quasi = np.log10(np.abs(stats_nl_pre_err[aux_k_quasi]) / thres)

			#Make all the negative values = 0, since that means they didn't pass the threshold
			aux_ultra_neg = w_ultra < 0.
			aux_lin_neg = w_lin < 0.
			aux_quasi_neg = w_quasi < 0.

			w_ultra[aux_ultra_neg] = 0
			w_lin[aux_lin_neg] = 0
			w_quasi[aux_quasi_neg] = 0

			#calculate the totals
			tot_ultra = np.sum(w_ultra)
			tot_lin = np.sum(w_lin)
			tot_quasi = np.sum(w_quasi)
		
		
		#Append these values to our z summary stat
		#For list only
		tot_nl_pre_z = np.append(tot_nl_pre_z, tot_ultra)
		tot_nl_pre_z = np.append(tot_nl_pre_z, tot_lin)
		tot_nl_pre_z = np.append(tot_nl_pre_z, tot_quasi)

		#For list of lists
		tot_nl_pre_z_ll.append(tot_ultra)
		tot_nl_pre_z_ll.append(tot_lin)
		tot_nl_pre_z_ll.append(tot_quasi)

		#Append these values for the general z stat
		#For list only
		tot_nl_pre = np.append(tot_nl_pre, tot_nl_pre_z)
		#For list of lists
		tot_nl_pre_ll.append(tot_nl_pre_z_ll)

	#Generate our z values for plotting
	z_actual = range(len(z_vals))
	z_arr = np.float_(np.asarray(z_actual))
	z_arr *= 0.5
	z = []
	z_ll = []

	for j in range(len(z_actual)):
		z_full = np.full(len(tot_nl_pre_ll[0]), z_arr[j])
		z = np.append(z,z_full)
		z_ll.append(z_full)

	#Generate an array of the midpoints of the bins
	ultra_scale_bin = (ultra_scale_max + ultra_scale_min) / 2
	lin_scale_bin = (lin_scale_max + lin_scale_min) / 2
	quasi_scale_bin = (quasi_scale_max + quasi_scale_min) / 2

	k_bin = [ultra_scale_bin, lin_scale_bin, quasi_scale_bin]
	k_list = k_bin * len(z_vals)

	#Doing it the pandas way
	k_words = ['Ultra-large', 'Linear', 'Quasi Lin']

	#Generates the data frame
	df = DataFrame(tot_nl_pre_ll, index=z_arr, columns=k_words)

	#Plots the colors
	pc = plt.pcolor(df)

	#Changes the ticks
	plt.yticks(np.arange(0.5, len(df.index),1), df.index)
	plt.xticks(np.arange(0.5, len(df.columns),1), df.columns)
	plt.xlabel('Scales')
	plt.ylabel('$z$')

	#Generate the color bar
	cb = plt.colorbar(pc)
	cb.set_label('How badly it failed')
	plt.title('Scales vs $z$, Threshold = %d' %thres)

	plt.savefig('/Users/penafiel/JPL/sum_stats/sum_stats_nl_pre_%05d.png' %trial, format='png')
	plt.clf()

	#Appends the complete sum f the totals
	tot_tot_nl_pre = np.append(tot_tot_nl_pre, np.sum(tot_nl_pre))


##########################
#                        #
#PLOTTING THE CORNER PLOT#
#                        #
##########################
#Call the other parameter values
h_arr = data[:,1]
Omega_b_arr = data[:,2]
Omega_cdm_arr = data[:,3]
A_s_arr = data[:,4]
n_s_arr = data[:,5]

#Puts all the arrays into an array of arrays
comp_ll = []
comp_ll.append(h_arr)
comp_ll.append(Omega_b_arr)
comp_ll.append(Omega_cdm_arr)
comp_ll.append(A_s_arr)
comp_ll.append(n_s_arr)
comp_tran = zip(*comp_ll)

#corner.corner(comp_tran,bins=len(comp_tran),plot_contours=False,weights=tot_tot_lin)
#Using a bastardized version of corner, we plot
corner(comp_tran,labels=[r'$h$', r'$\Omega_b$', r'$\Omega_{cdm}$', r'$A_s$', r'$n_s$'],bins=len(comp_tran),top_ticks=True,plot_density=False,plot_contours=False,data_kwargs={'s':5.0,'c':tot_tot_lin,'marker':'s'})
plt.savefig('/Users/penafiel/JPL/corner_plots/corner_lin.png', format='png')

plt.clf()

corner(comp_tran,labels=[r'$h$', r'$\Omega_b$', r'$\Omega_{cdm}$', r'$A_s$', r'$n_s$'],bins=len(comp_tran),top_ticks=True,plot_density=False,plot_contours=False,data_kwargs={'s':5.0,'c':tot_tot_nl,'marker':'s'})
plt.savefig('/Users/penafiel/JPL/corner_plots/corner_nl.png', format='png')
plt.clf()

corner(comp_tran,labels=[r'$h$', r'$\Omega_b$', r'$\Omega_{cdm}$', r'$A_s$', r'$n_s$'],bins=len(comp_tran),top_ticks=True,plot_density=False,plot_contours=False,data_kwargs={'s':5.0,'c':tot_tot_lin_pre,'marker':'s'})
plt.savefig('/Users/penafiel/JPL/corner_plots/corner_lin_pre.png', format='png')
plt.clf()

corner(comp_tran,labels=[r'$h$', r'$\Omega_b$', r'$\Omega_{cdm}$', r'$A_s$', r'$n_s$'],bins=len(comp_tran),top_ticks=True,plot_density=False,plot_contours=False,data_kwargs={'s':5.0,'c':tot_tot_nl_pre,'marker':'s'})
plt.savefig('/Users/penafiel/JPL/corner_plots/corner_nl_pre.png', format='png')
plt.clf()

np.savetxt('/Users/penafiel/JPL/data/tot_tot.txt', np.transpose([tot_tot_lin, tot_tot_nl, tot_tot_lin_pre, tot_tot_nl_pre]))

pdb.set_trace()
	







