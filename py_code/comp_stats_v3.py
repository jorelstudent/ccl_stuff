import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pandas import *
import pdb
import glob


#This program's aim is to look at each trial and find the places where the validity fails
#We are going to have 3 colors, corresponding to how badly it failed
#These will be based on the condition for clustering
#Clustering values  only affect those in the range of [1.e-2,0.2]
#So we're going to bin our k values according to
#Ultra-large scales:[1e-4, 1e-2]
#Linear scales:[1e-2, 0.1]
#Quasi-linear:[0.1,1.0]
#Each bin we're going to assign a number for how many points failed to reach 1e-4 threshold for each bin
#Then we will have a number as a threshold, accounting for how many times we will allow it to fail
#RED = it failed to reach 1e-4 more than the threshold
#ORANGE = it failed to reach 1e-4 less than the threshold
#GREEN = it reaches 1e-4 everywhere

#Also the number for failures can either include clustering regime only or not
thres = 10 #Threshold for number of failures
clustering_only = False #Only counts failures if inside the clustering regime

ultra_scale_min = 1e-4 #Minimum for the ultra-large scales
ultra_scale_max = 1e-2 #Maximum for the ultra-large scales
lin_scale_min = 1e-2 #Min for the linear scales
lin_scale_max = 1e-1 #Max for the linear scales
quasi_scale_min = 1e-1 #Min for the quasi-lin scales
quasi_scale_max = 1.0 #Max for the quasi-lin scales


cluster_reg_min = 1e-2 #Min for the cluster regime
cluster_reg_max = 0.2 # Max for the cluster regime


#Call the original par_var file, so we can get the trial # (easier in the long run, trust)

data = np.genfromtxt('/Users/penafiel/JPL/data/par_stan.txt', dtype='str', skip_header=1)

#Gets the trial number into an arr
trial_arr = data[:,0]

#Iterates over the trial #
for i in range(len(trial_arr)):
	trial = data[i,0]
	print 'Performing trial %s' %trial

	z_vals = ['1','2','3','4','5','6']
	
	#Gonna generate an array of arrays, with each row corresponding to a different z value
	#Each column will correspond to a different bin of k_values
	sum_lin = []
	sum_nl = []
	sum_lin_pre = []
	sum_nl_pre = []

	#For list of lists
	sum_lin_ll = []
	sum_nl_ll = []
	sum_lin_pre_ll = []
	sum_nl_pre_ll = []


	for j in range(len(z_vals)):
		z_val = z_vals[j]
		z_path = '_z%s.dat' %z_val
		print 'Performing z_val = ', z_val
		#For ease in iterating over different z valus we use string manipulation
		stats_lin_path = '/Users/penafiel/JPL/stats/lhs_mpk_err_lin_%s' %trial
		stats_nl_path = '/Users/penafiel/JPL/stats/lhs_mpk_err_nl_%s' %trial
		stats_lin_pre_path = '/Users/penafiel/JPL/stats/lhs_mpk_err_lin_pk_%s' %trial
		stats_nl_pre_path = '/Users/penafiel/JPL/stats/lhs_mpk_err_nl_pk_%s' %trial

		#Adds the z_path
		stats_lin_path += z_path
		stats_nl_path += z_path
		stats_lin_pre_path += z_path
		stats_nl_pre_path += z_path

		#calls the data
		stats_lin_data = np.loadtxt(stats_lin_path, skiprows=1)
		stats_nl_data = np.loadtxt(stats_nl_path, skiprows=1)
		stats_lin_pre_data = np.loadtxt(stats_lin_pre_path, skiprows=1)
		stats_nl_pre_data = np.loadtxt(stats_nl_pre_path, skiprows=1)

		stats_lin_k = stats_lin_data[:,0]
		stats_lin_err = stats_lin_data[:,1]
		stats_nl_k = stats_nl_data[:,0]
		stats_nl_err = stats_nl_data[:,1]
		stats_lin_pre_k = stats_lin_pre_data[:,0]
		stats_lin_pre_err = stats_lin_pre_data[:,1]
		stats_nl_pre_k = stats_nl_pre_data[:,0]
		stats_nl_pre_err = stats_nl_pre_data[:,1]

		#Create arrays that will be used to fill the complete summary arrays
		sum_lin_z = []
		sum_nl_z = []
		sum_lin_pre_z = []
		sum_nl_pre_z = []

		#For list of lists
		sum_lin_z_ll = []
		sum_nl_z_ll = []
		sum_lin_pre_z_ll = []
		sum_nl_pre_z_ll = []

		#We perform a loop that looks into the bins for k
		#Doing this for lin
		#Much easier than doing a for loop because of list comprehension ALSO FASTER
		fail_ultra = 0 #initial value for ultra large scales
		fail_lin = 0 #initialize for lin scales
		fail_quasi = 0 #initialize for quasi lin scales

		#k has to fall in the proper bins
		aux_k_ultra = (stats_lin_k > ultra_scale_min) & (stats_lin_k < ultra_scale_max)
		aux_k_lin = (stats_lin_k > lin_scale_min) & (stats_lin_k < lin_scale_max)
		aux_k_quasi = (stats_lin_k > quasi_scale_min) & (stats_lin_k < quasi_scale_max)

		#Looks at only the regime where clustering affects it
		if clustering_only == True:
			aux_cluster_ultra = (stats_lin_k[aux_k_ultra] > cluster_reg_min) & (stats_lin_k[aux_k_ultra] < cluster_reg_max)
			aux_cluster_lin = (stats_lin_k[aux_k_lin] > cluster_reg_min) & (stats_lin_k[aux_k_lin] < cluster_reg_max)
			aux_cluster_quasi = (stats_lin_k[aux_k_quasi] > cluster_reg_min) & (stats_lin_k[aux_k_quasi] < cluster_reg_max)
			aux_err_ultra = (stats_lin_err[aux_k_ultra])[aux_cluster_ultra] > 1e-4
			aux_err_lin = (stats_lin_err[aux_k_lin])[aux_cluster_lin] > 1e-4
			aux_err_quasi = (stats_lin_err[aux_k_quasi])[aux_cluster_quasi] > 1e-4
			
		#calculates imprecision in any regime
		if clustering_only == False:
			aux_err_ultra = stats_lin_err[aux_k_ultra] > 1e-4
			aux_err_lin = stats_lin_err[aux_k_lin] > 1e-4
			aux_err_quasi = stats_lin_err[aux_k_quasi] > 1e-4

		#Adds the number of times it fails and appends it to our summary statistic
		#If you want list of lists
		sum_lin_z_ll.append(np.sum(aux_err_ultra))
		sum_lin_z_ll.append(np.sum(aux_err_lin))
		sum_lin_z_ll.append(np.sum(aux_err_quasi))
		
		#Only interested in list
		sum_lin_z = np.append(sum_lin_z, np.sum(aux_err_ultra))
		sum_lin_z = np.append(sum_lin_z, np.sum(aux_err_lin))
		sum_lin_z = np.append(sum_lin_z, np.sum(aux_err_quasi))

		#We perform the calculation similarly for nl case
		fail_ultra = 0 #initial value for ultra large scales
		fail_lin = 0 #initialize for lin scales
		fail_quasi = 0 #initialize for quasi lin scales

		#k has to fall in the proper bins
		aux_k_ultra = (stats_nl_k > ultra_scale_min) & (stats_nl_k < ultra_scale_max)
		aux_k_lin = (stats_nl_k > lin_scale_min) & (stats_nl_k < lin_scale_max)
		aux_k_quasi = (stats_nl_k > quasi_scale_min) & (stats_nl_k < quasi_scale_max)

		#Looks at only the regime where clustering affects it
		if clustering_only == True:
			aux_cluster_ultra = (stats_nl_k[aux_k_ultra] > cluster_reg_min) & (stats_nl_k[aux_k_ultra] < cluster_reg_max)
			aux_cluster_lin = (stats_nl_k[aux_k_lin] > cluster_reg_min) & (stats_nl_k[aux_k_lin] < cluster_reg_max)
			aux_cluster_quasi = (stats_nl_k[aux_k_quasi] > cluster_reg_min) & (stats_nl_k[aux_k_quasi] < cluster_reg_max)
			aux_err_ultra = (stats_nl_err[aux_k_ultra])[aux_cluster_ultra] > 1e-4
			aux_err_lin = (stats_nl_err[aux_k_lin])[aux_cluster_lin] > 1e-4
			aux_err_quasi = (stats_nl_err[aux_k_quasi])[aux_cluster_quasi] > 1e-4
			
		#calculates imprecision in any regime
		if clustering_only == False:
			aux_err_ultra = stats_nl_err[aux_k_ultra] > 1e-4
			aux_err_lin = stats_nl_err[aux_k_lin] > 1e-4
			aux_err_quasi = stats_nl_err[aux_k_quasi] > 1e-4

		#Adds the number of times it fails and appends it to our summary statistic
		#if you want list of lists
		sum_nl_z_ll.append(np.sum(aux_err_ultra))
		sum_nl_z_ll.append(np.sum(aux_err_lin))
		sum_nl_z_ll.append(np.sum(aux_err_quasi))

		#Only interested in list
		sum_nl_z = np.append(sum_nl_z, np.sum(aux_err_ultra))
		sum_nl_z = np.append(sum_nl_z, np.sum(aux_err_lin))
		sum_nl_z = np.append(sum_nl_z, np.sum(aux_err_quasi))

		#Perform this similarly for lin precise

		fail_ultra = 0 #initial value for ultra large scales
		fail_lin = 0 #initialize for lin scales
		fail_quasi = 0 #initialize for quasi lin scales

		#k has to fall in the proper bins
		aux_k_ultra = (stats_lin_pre_k > ultra_scale_min) & (stats_lin_pre_k < ultra_scale_max)
		aux_k_lin = (stats_lin_pre_k > lin_scale_min) & (stats_lin_pre_k < lin_scale_max)
		aux_k_quasi = (stats_lin_pre_k > quasi_scale_min) & (stats_lin_pre_k < quasi_scale_max)

		#Looks at only the regime where clustering affects it
		if clustering_only == True:
			aux_cluster_ultra = (stats_lin_pre_k[aux_k_ultra] > cluster_reg_min) & (stats_lin_pre_k[aux_k_ultra] < cluster_reg_max)
			aux_cluster_lin = (stats_lin_pre_k[aux_k_lin] > cluster_reg_min) & (stats_lin_pre_k[aux_k_lin] < cluster_reg_max)
			aux_cluster_quasi = (stats_lin_pre_k[aux_k_quasi] > cluster_reg_min) & (stats_lin_pre_k[aux_k_quasi] < cluster_reg_max)
			aux_err_ultra = (stats_lin_pre_err[aux_k_ultra])[aux_cluster_ultra] > 1e-4
			aux_err_lin = (stats_lin_pre_err[aux_k_lin])[aux_cluster_lin] > 1e-4
			aux_err_quasi = (stats_lin_pre_err[aux_k_quasi])[aux_cluster_quasi] > 1e-4
			
		#calculates imprecision in any regime
		if clustering_only == False:
			aux_err_ultra = stats_lin_pre_err[aux_k_ultra] > 1e-4
			aux_err_lin = stats_lin_pre_err[aux_k_lin] > 1e-4
			aux_err_quasi = stats_lin_pre_err[aux_k_quasi] > 1e-4

		#Adds the number of times it fails and appends it to our summary statistic
		#If you want a list of lists
		sum_lin_pre_z_ll.append(np.sum(aux_err_ultra))
		sum_lin_pre_z_ll.append(np.sum(aux_err_lin))
		sum_lin_pre_z_ll.append(np.sum(aux_err_quasi))

		#Only interested in the list
		sum_lin_pre_z = np.append(sum_lin_pre_z, np.sum(aux_err_ultra))
		sum_lin_pre_z = np.append(sum_lin_pre_z, np.sum(aux_err_lin))
		sum_lin_pre_z = np.append(sum_lin_pre_z, np.sum(aux_err_quasi))


		#Lastly, we perform this for nl precise


		fail_ultra = 0 #initial value for ultra large scales
		fail_lin = 0 #initialize for lin scales
		fail_quasi = 0 #initialize for quasi lin scales

		#k has to fall in the proper bins
		aux_k_ultra = (stats_nl_pre_k > ultra_scale_min) & (stats_nl_pre_k < ultra_scale_max)
		aux_k_lin = (stats_nl_pre_k > lin_scale_min) & (stats_nl_pre_k < lin_scale_max)
		aux_k_quasi = (stats_nl_pre_k > quasi_scale_min) & (stats_nl_pre_k < quasi_scale_max)

		#Looks at only the regime where clustering affects it
		if clustering_only == True:
			aux_cluster_ultra = (stats_nl_pre_k[aux_k_ultra] > cluster_reg_min) & (stats_nl_pre_k[aux_k_ultra] < cluster_reg_max)
			aux_cluster_lin = (stats_nl_pre_k[aux_k_lin] > cluster_reg_min) & (stats_nl_pre_k[aux_k_lin] < cluster_reg_max)
			aux_cluster_quasi = (stats_nl_pre_k[aux_k_quasi] > cluster_reg_min) & (stats_nl_pre_k[aux_k_quasi] < cluster_reg_max)
			aux_err_ultra = (stats_nl_pre_err[aux_k_ultra])[aux_cluster_ultra] > 1e-4
			aux_err_lin = (stats_nl_pre_err[aux_k_lin])[aux_cluster_lin] > 1e-4
			aux_err_quasi = (stats_nl_pre_err[aux_k_quasi])[aux_cluster_quasi] > 1e-4
			
		#calculates imprecision in any regime
		if clustering_only == False:
			aux_err_ultra = stats_nl_pre_err[aux_k_ultra] > 1e-4
			aux_err_lin = stats_nl_pre_err[aux_k_lin] > 1e-4
			aux_err_quasi = stats_nl_pre_err[aux_k_quasi] > 1e-4

		#Adds the number of times it fails and appends it to our summary statistic
		#If you want list of lists
		sum_nl_pre_z_ll.append(np.sum(aux_err_ultra))
		sum_nl_pre_z_ll.append(np.sum(aux_err_lin))
		sum_nl_pre_z_ll.append(np.sum(aux_err_quasi))

		#only if you want lists
		sum_nl_pre_z = np.append(sum_nl_pre_z, np.sum(aux_err_ultra))
		sum_nl_pre_z = np.append(sum_nl_pre_z, np.sum(aux_err_lin))
		sum_nl_pre_z = np.append(sum_nl_pre_z, np.sum(aux_err_quasi))


		#If you want list of lists
		sum_lin_ll.append(sum_lin_z_ll)
		sum_nl_ll.append(sum_nl_z_ll)
		sum_lin_pre_ll.append(sum_lin_pre_z_ll)
		sum_nl_pre_ll.append(sum_nl_pre_z_ll)

		#Only if you want big list
		sum_lin = np.append(sum_lin, sum_lin_z)
		sum_nl = np.append(sum_nl, sum_nl_z)
		sum_lin_pre = np.append(sum_lin_pre, sum_lin_pre_z)
		sum_nl_pre = np.append(sum_nl_pre, sum_nl_pre_z)


	z_actual = range(len(z_vals))
	z_arr = np.float_(np.asarray(z_actual))
	z_arr *= 0.5
	z = []
	z_ll = []
	#Create a heat map, but makes it red, right now we just mark threshold on the heat map
	for j in range(len(z_actual)):
		z_full = np.full(len(sum_lin_ll[0]), z_arr[j])
		z = np.append(z,z_full)
		z_ll.append(z_full)
	#Generate an array of the midpoints of the bins
	ultra_scale_bin = (ultra_scale_max + ultra_scale_min)/2
	lin_scale_bin = (lin_scale_max + lin_scale_min)/2
	quasi_scale_bin = (quasi_scale_max + quasi_scale_min)/2

	k_bin = [ultra_scale_bin, lin_scale_bin, quasi_scale_bin]
	k_list = k_bin * len(z_vals)
	"""
	#Plot the k_values and z_values with an intensity map of the number of failures
	pl = plt.scatter(np.log10(k_list), z, c=sum_nl, marker='s', s=1500)
	plt.xlabel('$Log_{10}k$')
	plt.ylabel('$z$')
	cb = plt.colorbar(pl)
	cb.set_label('Num of Failures')
	plt.title('$Log_{10}k$ vs $z$')

	#Want to create lines to demarcate the different bins
	lines = np.linspace(-0.25, 2.75, 10)
	ultra_scale_max_lin = np.full(len(lines), ultra_scale_max)
	ultra_scale_min_lin = np.full(len(lines), ultra_scale_min)
	lin_scale_max_lin = np.full(len(lines),lin_scale_max)
	quasi_scale_max_lin = np.full(len(lines), quasi_scale_max)

	plt.plot(np.log10(ultra_scale_max_lin), lines, c='black')
	plt.plot(np.log10(lin_scale_max_lin), lines, c='black')
	plt.plot(np.log10(ultra_scale_min_lin), lines, c='black')
	plt.plot(np.log10(quasi_scale_max_lin), lines, c = 'black')
	"""
	#Gonna try to plot it the pandas way
	#WORKS!!!! AND it fills the whole space. FUCKING LIT
	k_words = ['Ultra-large', 'Linear', 'Quasi Lin']
	#Use pandas to generate a data frame
	df = DataFrame(sum_lin_ll, index=z_arr, columns=k_words)

	#Values greater than threshold will be red, values at 0 will be green
	#and values in between will be gradient of orange
	
	#Failed here
	#cmap, norm = mcolors.from_levels_and_colors([thres,100], ['red'])

	#Trying to brute force colors for me
	cmap = mcolors.ListedColormap(['limegreen', 'greenyellow', 'yellow', 'gold', 'orange','red'])
	bounds = [0,int(thres / 4.), int(thres / 3.), int(thres / 2.), int(thres), int(len(stats_lin_k))]
	norm = mcolors.BoundaryNorm(bounds, cmap.N)

	#Plots the colors
	pc = plt.pcolor(df, cmap = cmap, norm=norm)

	#Changes the ticks
	plt.yticks(np.arange(0.5, len(df.index),1), df.index)
	plt.xticks(np.arange(0.5, len(df.columns),1), df.columns)
	plt.xlabel('Scales')
	plt.ylabel('$z$')

	#Generate the color bar
	cb = plt.colorbar(pc)
	cb.set_label('Num of Failures')
	plt.title('Scales vs $z$, Threshold = %d' %thres)

	plt.savefig('/Users/penafiel/JPL/sum_stats/sum_stats_lin_%s.png' %trial, format='png')
	plt.clf()

	#Do this similarly for nonlin
	#Use pandas to generate a data frame
	df = DataFrame(sum_nl_ll, index=z_arr, columns=k_words)

	#Values greater than threshold will be red, values at 0 will be green
	#and values in between will be gradient of orange
	
	#Trying to brute force colors for me
	cmap = mcolors.ListedColormap(['limegreen', 'greenyellow', 'yellow', 'gold', 'orange','red'])
	bounds = [0,int(thres / 4.), int(thres / 3.), int(thres / 2.), int(thres), int(len(stats_nl_k))]
	norm = mcolors.BoundaryNorm(bounds, cmap.N)

	#Plots the colors
	pc = plt.pcolor(df, cmap = cmap, norm=norm)

	#Changes the ticks
	plt.yticks(np.arange(0.5, len(df.index),1), df.index)
	plt.xticks(np.arange(0.5, len(df.columns),1), df.columns)
	plt.xlabel('Scales')
	plt.ylabel('$z$')

	#Generate the color bar
	cb = plt.colorbar(pc)
	cb.set_label('Num of Failures')
	plt.title('Scales vs $z$, Threshold = %d' %thres)

	plt.savefig('/Users/penafiel/JPL/sum_stats/sum_stats_nl_%s.png' %trial, format='png')
	plt.clf()

	#Do this similarly for lin+precision
	#Use pandas to generate a data frame
	df = DataFrame(sum_lin_pre_ll, index=z_arr, columns=k_words)

	#Values greater than threshold will be red, values at 0 will be green
	#and values in between will be gradient of orange
	
	#Trying to brute force colors for me
	cmap = mcolors.ListedColormap(['limegreen', 'greenyellow', 'yellow', 'gold', 'orange','red'])
	bounds = [0,int(thres / 4.), int(thres / 3.), int(thres / 2.), int(thres), int(len(stats_lin_pre_k))]
	norm = mcolors.BoundaryNorm(bounds, cmap.N)

	#Plots the colors
	pc = plt.pcolor(df, cmap = cmap, norm=norm)

	#Changes the ticks
	plt.yticks(np.arange(0.5, len(df.index),1), df.index)
	plt.xticks(np.arange(0.5, len(df.columns),1), df.columns)
	plt.xlabel('Scales')
	plt.ylabel('$z$')

	#Generate the color bar
	cb = plt.colorbar(pc)
	cb.set_label('Num of Failures')
	plt.title('Scales vs $z$, Threshold = %d' %thres)

	plt.savefig('/Users/penafiel/JPL/sum_stats/sum_stats_lin_pre_%s.png' %trial, format='png')
	plt.clf()

	#Do this similarly for nonlin+precision
	#Use pandas to generate a data frame
	df = DataFrame(sum_nl_pre_ll, index=z_arr, columns=k_words)

	#Values greater than threshold will be red, values at 0 will be green
	#and values in between will be gradient of orange
	
	#Trying to brute force colors for me
	cmap = mcolors.ListedColormap(['limegreen', 'greenyellow', 'yellow', 'gold', 'orange','red'])
	bounds = [0,int(thres / 4.), int(thres / 3.), int(thres / 2.), int(thres), int(len(stats_nl_pre_k))]
	norm = mcolors.BoundaryNorm(bounds, cmap.N)

	#Plots the colors
	pc = plt.pcolor(df, cmap = cmap, norm=norm)

	#Changes the ticks
	plt.yticks(np.arange(0.5, len(df.index),1), df.index)
	plt.xticks(np.arange(0.5, len(df.columns),1), df.columns)
	plt.xlabel('Scales')
	plt.ylabel('$z$')

	#Generate the color bar
	cb = plt.colorbar(pc)
	cb.set_label('Num of Failures')
	plt.title('Scales vs $z$, Threshold = %d' %thres)

	plt.savefig('/Users/penafiel/JPL/sum_stats/sum_stats_nl_pre_%s.png' %trial, format='png')
	plt.clf()

pdb.set_trace()
