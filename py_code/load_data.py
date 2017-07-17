import numpy as np
import matplotlib.pyplot as plt
import pdb

#This code is designed so that the user can input a file ID, and it outputs the
#parameter values and possibly stats and power spectra values



#Call the original par_var file, so we can get the trail # (easier in the long run)

data = np.genfromtxt('/Users/penafiel/JPL/data/par_stan.txt', dtype='str', skip_header=1)


#Get the trial number into an arr
trial_arr = data[:,0]


#Let's define a couple of functions that will work out for us
def load_par(file_id):
	file_index = trial_arr.tolist().index(file_id)
	h = float(data[file_index,1])
	Omega_b = float(data[file_index,2])
	Omega_cdm = float(data[file_index,3])
	A_s = float(data[file_index, 4])
	n_s = float(data[file_index, 5])

	return file_id, h, Omega_b, Omega_cdm, A_s, n_s

def load_mpk_lin(file_id, z_index):
	#CLASS AND CCL use different units ugh, so we gotta multiply by some constants
	file_index = trial_arr.tolist().index(file_id)
	h = float(data[file_index,1])

	#Path where it's located
	ccl_lin_path = '/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_lin_%s' %file_id
	class_lin_path = '/Users/penafiel/JPL/class/output/lin/lhs_lin_%s' %file_id
	stats_lin_path = '/Users/penafiel/JPL/stats/lhs_mpk_err_lin_%s' %file_id

	#Adds the z-valued portion
	z_str = str(z_index)
	z_path = 'z%s_pk.dat' %z_str
	ccl_lin_path += z_path
	class_lin_path += z_path
	
	z_stats_path = '_z%s.dat' %z_str
	stats_lin_path += z_stats_path

	#Loads the data
	ccl_lin_data = np.loadtxt(ccl_lin_path, skiprows=1)
	class_lin_data = np.loadtxt(class_lin_path, skiprows=1)
	stats_lin_data = np.loadtxt(stats_lin_path, skiprows=1)

	#Creates the vectors
	ccl_k_lin = ccl_lin_data[:,0]
	ccl_pk_lin = ccl_lin_data[:,1]
	class_k_lin = class_lin_data[:,0]
	class_pk_lin = class_lin_data[:,1]
	stats_lin_err = stats_lin_data[:,1]

	#Multiply by the factors
	class_k_lin *= h
	class_pk_lin /= h**3

	return class_k_lin, class_pk_lin, ccl_k_lin, ccl_pk_lin, stats_lin_err

	
def load_mpk_nl(file_id, z_index):
	
	#CLASS AND CCL use different units ugh, so we gotta multiply by some constants
	file_index = trial_arr.tolist().index(file_id)
	h = float(data[file_index,1])

	#Path where it's located
	ccl_nl_path = '/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_nl_%s' %file_id
	class_nl_path = '/Users/penafiel/JPL/class/output/nonlin/lhs_nonlin_%s' %file_id
	stats_nl_path = '/Users/penafiel/JPL/stats/lhs_mpk_err_nl_%s' %file_id

	#Adds the z-valued portion
	z_str = str(z_index)
	z_path = 'z%s_pk.dat' %z_str
	ccl_nl_path += z_path
	class_nl_path += z_path
	
	z_stats_path = '_z%s.dat' %z_str
	stats_nl_path += z_stats_path

	#Loads the data
	ccl_nl_data = np.loadtxt(ccl_nl_path, skiprows=1)
	class_nl_data = np.loadtxt(class_nl_path, skiprows=1)
	stats_nl_data = np.loadtxt(stats_nl_path, skiprows=1)

	#Creates the vectors
	ccl_k_nl = ccl_nl_data[:,0]
	ccl_pk_nl = ccl_nl_data[:,1]
	class_k_nl = class_nl_data[:,0]
	class_pk_nl = class_nl_data[:,1]
	stats_nl_err = stats_nl_data[:,1]

	#Multiply by the factors
	class_k_nl *= h
	class_pk_nl /= h**3

	return class_k_nl, class_pk_nl, ccl_k_nl, ccl_pk_nl, stats_nl_err

def load_mpk_lin_pre(file_id, z_index):
	#CLASS AND CCL use different units ugh, so we gotta multiply by some constants
	file_index = trial_arr.tolist().index(file_id)
	h = float(data[file_index,1])

	#Path where it's located
	ccl_lin_pre_path = '/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_lin_pk_%s' %file_id
	class_lin_pre_path = '/Users/penafiel/JPL/class/output/lin/lhs_lin_pk_%s' %file_id
	stats_lin_pre_path = '/Users/penafiel/JPL/stats/lhs_mpk_err_lin_pk_%s' %file_id

	#Adds the z-valued portion
	z_str = str(z_index)
	z_path = 'z%s_pk.dat' %z_str
	ccl_lin_pre_path += z_path
	class_lin_pre_path += z_path
	
	z_stats_path = '_z%s.dat' %z_str
	stats_lin_pre_path += z_stats_path

	#Loads the data
	ccl_lin_pre_data = np.loadtxt(ccl_lin_pre_path, skiprows=1)
	class_lin_pre_data = np.loadtxt(class_lin_pre_path, skiprows=1)
	stats_lin_pre_data = np.loadtxt(stats_lin_pre_path, skiprows=1)

	#Creates the vectors
	ccl_k_lin_pre = ccl_lin_pre_data[:,0]
	ccl_pk_lin_pre = ccl_lin_pre_data[:,1]
	class_k_lin_pre = class_lin_pre_data[:,0]
	class_pk_lin_pre = class_lin_pre_data[:,1]
	stats_lin_pre_err = stats_lin_pre_data[:,1]

	#Multiply by the factors
	class_k_lin_pre *= h
	class_pk_lin_pre /= h**3

	return class_k_lin_pre, class_pk_lin_pre, ccl_k_lin_pre, ccl_pk_lin_pre, stats_lin_pre_err

def load_mpk_nl_pre(file_id, z_index):
	#CLASS AND CCL use different units ugh, so we gotta multiply by some constants
	file_index = trial_arr.tolist().index(file_id)
	h = float(data[file_index,1])

	#Path where it's located
	ccl_nl_pre_path = '/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_nl_pk_%s' %file_id
	class_nl_pre_path = '/Users/penafiel/JPL/class/output/nonlin/lhs_nonlin_pk_%s' %file_id
	stats_nl_pre_path = '/Users/penafiel/JPL/stats/lhs_mpk_err_nl_pk_%s' %file_id

	#Adds the z-valued portion
	z_str = str(z_index)
	z_path = 'z%s_pk.dat' %z_str
	ccl_nl_pre_path += z_path
	class_nl_pre_path += z_path
	
	z_stats_path = '_z%s.dat' %z_str
	stats_nl_pre_path += z_stats_path

	#Loads the data
	ccl_nl_pre_data = np.loadtxt(ccl_nl_pre_path, skiprows=1)
	class_nl_pre_data = np.loadtxt(class_nl_pre_path, skiprows=1)
	stats_nl_pre_data = np.loadtxt(stats_nl_pre_path, skiprows=1)

	#Creates the vectors
	ccl_k_nl_pre = ccl_nl_pre_data[:,0]
	ccl_pk_nl_pre = ccl_nl_pre_data[:,1]
	class_k_nl_pre = class_nl_pre_data[:,0]
	class_pk_nl_pre = class_nl_pre_data[:,1]
	stats_nl_pre_err = stats_nl_pre_data[:,1]

	#Multiply by the factors
	class_k_nl_pre *= h
	class_pk_nl_pre /= h**3

	return class_k_nl_pre, class_pk_nl_pre, ccl_k_nl_pre, ccl_pk_nl_pre, stats_nl_pre_err

print 'Welcome to Data Loading Land (name pending)!'
id_pass = False
#Stays in this loop until it properly passes
while id_pass == False:
	#From there have the user input something
	print 'If you need help on what will be loaded, type help'
	file_id_raw = raw_input('Enter a file ID: ')

	#if input == help:

	if file_id_raw == 'help':
		print 'This program will laod the parameter values and data of the ID you want.'
		print 'Try it out by inputting a valid ID number'

	if file_id_raw != 'help':
		file_id = int(file_id_raw)
		answer = isinstance(file_id, (int,long))
		if answer == True:
			#First since we have strings conver to string
			file_id_str = '%05d' %file_id

			#Check to see if this thing is inside the data file
			id_check = file_id_str in trial_arr

			if id_check == False:
				print 'ID not found. Please input a different file ID.'
			if id_check == True:
				id_pass = True
	
		else:
			print 'Please enter a valid ID number or if you\'re always lost like Zoro, type help'

z_pass = False
#First have them input a z_value, since we have multiple sets of values
z_vals = np.linspace(0,2.5, 6)
#Stay in a loop if the user did not put a valid z_value
while z_pass == False:

	z_input_raw = raw_input('Enter a z value in [0, 2.5] in increments of 0.5: ')
	z_input = float(z_input_raw)
	z_check = z_input in z_vals
	print z_check
	if z_check == True:
		z_pass = True
		z_index = z_vals.tolist().index(z_input) + 1
	
	else:
		print 'Invalid z value. Bruh!'


done = 'no'
#Make a print statement to see if they\'re done loading the data
while done == 'no':

	#Have the user input what type of data they would like to load
	print 'If you need help on what will be loaded from which inputs, type help'
	load_raw = raw_input('Which data would you like to load? ')


	if load_raw == 'help':
		print 'So a function I will define multiple functions that will return values in this order.'
		print 'Inputting load_par will load trial, h, Omega_b, Omega_cdm, A_s, n_s'
		print 'Inputting load_mpk_lin will load k_CLASS, mPk_CLASS, k_CCL, mPk_CCL, mPk_err for the linear case'
		print 'Inputting load_mpk_nl will load k_CLASS, mPk_CLASS, k_CCL, mPk_CCL, mPk_err for the nonlin case'
		print 'Inputting load_mpk_pre_lin will load the more precise version \n k_CLASS_pre, mPk_CLASS_pre, k_CCL_pre, mPk_CCL_pre, mPk_err_pre for the lin case'
		print 'Inputting load_mpk_pre_nl will load the more precise version \n k_CLASS_pre, mPk_CLASS_pre, k_CCL_pre, mPk_CCL_pre, mPk_err_pre for the nonlin case'

	#h calls a different value, so we save it as h0
	elif load_raw == 'load_par':
		trial, h0, Omega_b, Omega_cdm, A_s, n_s = load_par(file_id_str)
		print 'Loaded the parameters under: trial, h0, Omega_b, Omega_cdm, A_s, n_s'
		continue_raw = raw_input('Would you like to load more data? [y/n]')
		if continue_raw == 'y':
			done = 'no'
		if continue_raw == 'n':
			done = 'yes'
	
	elif load_raw == 'load_mpk_lin':
		class_k_lin, class_pk_lin, ccl_k_lin, ccl_pk_lin, stas_lin_err = load_mpk_lin(file_id_str, z_index)
		print 'Loaded the data set as: class_k_lin, class_pk_lin, ccl_k_lin, ccl_pk_lin, stas_lin_err'
		continue_raw = raw_input('Would you like to load more data? [y/n]')

		if continue_raw == 'y':
			done = 'no'
		if continue_raw == 'n':
			done = 'yes'

	elif load_raw == 'load_mpk_nl':
		class_k_nl, class_pk_nl, ccl_k_nl, ccl_pk_nl, stats_nl_err = load_mpk_nl(file_id_str, z_index)
		print 'Loaded the data set as: class_k_nl, class_pk_nl, ccl_k_nl, ccl_pk_nl, stats_nl_err'

		continue_raw = raw_input('Would you like to load more data? [y/n]')

		if continue_raw == 'y':
			done = 'no'
		if continue_raw == 'n':
			done = 'yes'

	elif load_raw == 'load_mpk_lin_pre':
		class_k_lin_pre, class_pk_lin_pre, ccl_k_lin_pre, ccl_pk_lin_pre, stats_lin_pre_err = load_mpk_lin_pre(file_id_str, z_index)
		print 'Loaded the data set as: class_k_lin_pre, class_pk_lin_pre, ccl_k_lin_pre, ccl_pk_lin_pre, stats_lin_pre_err'

		continue_raw = raw_input('Would you like to load more data? [y/n]')

		if continue_raw == 'y':
			done = 'no'
		if continue_raw == 'n':
			done = 'yes'

	elif load_raw == 'load_mpk_nl_pre':
		class_k_nl_pre, class_pk_nl_pre, ccl_k_nl_pre, ccl_pk_nl_pre, stats_nl_pre_err = load_mpk_nl_pre(file_id_str, z_index)
		print 'Loaded the data set as: class_k_nl_pre, class_pk_nl_pre, ccl_k_nl_pre, ccl_pk_nl_pre, stats_nl_pre_err'

		continue_raw = raw_input('Would you like to load more data? [y/n]')

		if continue_raw == 'y':
			done = 'no'
		if continue_raw == 'n':
			done = 'yes'

	else:
		print 'Invalid input. USE help, damn it!'

print 'Now you can play/save your data. WOOOOOOOH Please come again!'
pdb.set_trace()
