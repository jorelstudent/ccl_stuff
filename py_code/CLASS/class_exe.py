from __future__ import print_function
import os
from subprocess import call
import subprocess
import pdb
import numpy as np
import glob

#This .py file runs ./class on the all .ini files
#Iterates over every file with that extension in this folder
for filename in glob.iglob('/Users/penafiel/JPL/class/ini_files/*.ini'):
	#Executes the ./class for each ini file
	
	#Skips it for files that cause an error
	"""
	if filename == '/Users/penafiel/JPL/class/ini_files/lhs_lin_00038.ini':
		continue
	if filename == '/Users/penafiel/JPL/class/ini_files/lhs_lin_00042.ini':
		continue
	
	if filename == '/Users/penafiel/JPL/class/ini_files/lhs_nonlin_00038.ini':
		continue
	if filename == '/Users/penafiel/JPL/class/ini_files/lhs_nonlin_00042.ini':
		continue
	"""
	subprocess.call(['./class', '%s' %filename])#, stdout = subprocess.PIPE)
	print('Performing', filename)
	#Get and save the output
	stdout = subprocess.check_output(['./class', '%s' %filename])
	basefile = os.path.splitext('%s' %filename)[0]
	file = open('%s.txt' %basefile, 'w')
	file.write(stdout)
	file.close()


