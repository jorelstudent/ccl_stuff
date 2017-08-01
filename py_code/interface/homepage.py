from flask import Flask, render_template, request
import pandas as pd
from bokeh.embed import components

from bokeh.layouts import column, widgetbox, WidgetBox, layout
from bokeh.models import CustomJS, Button, HoverTool, ColumnDataSource, LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar, OpenURL, TapTool#For the button and a hovertool
from bokeh.models.widgets import Slider, Dropdown, Select, RangeSlider #For the sliders and dropdown
from bokeh.plotting import figure, curdoc, show
from bokeh.io import gridplot, output_file, show #allows you to make gridplots
from bokeh.charts import HeatMap, bins, output_file, show #Allows you to craete heatmaps
from bokeh.models import Rect

import numpy as np
import pdb
from random import random

app = Flask(__name__)
#creates hover tool
indices = range(100)
def create_lin(index):
    # load the data
    i = int(index)

    fname = "/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_lin_%05dz1_pk.dat" % (i)
    #ccl_data = pd.read_table(fname,
        #names=["k", "pk_lin"], skiprows = 1, delim_whitespace = True)
    cclData = np.loadtxt(fname, skiprows = 1)
    cclK = cclData[:, 0]
    cclPk = cclData[:, 1]
    data = np.loadtxt('/Users/penafiel/JPL/data/par_stan1.csv', skiprows = 1)


    fname = "/Users/penafiel/JPL/class/output/lin/lhs_lin_%05dz1_pk.dat" % (i)
    #classData = pd.read_table(fname,
        #names=["k", "P"], skiprows = 4, delim_whitespace = True)
    classData = np.loadtxt(fname, skiprows = 4);
    classKLin = classData[:, 0]
    classPLin = classData[:, 1]

    #Multiply by factors
    #multiply k by some factor of h, CLASS and CCL use different units, ugh
    h = float(data[i,1])

    classKLin *= h
    classPLin /= h**3

    # create a plot and style its properties
    p = figure(toolbar_location="right", title = "CCL Validation", x_axis_type = "log", y_axis_type = "log",
        tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")


    p2 = figure(toolbar_location="right", title = "CCL Validation", x_axis_type = "log", y_axis_type = "log",
        tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")

    p.outline_line_color = None
    p.grid.grid_line_color = None

    p2.outline_line_color = None
    p2.grid.grid_line_color = None

    # plot the data
    #p.circle(ccl_data['k'].values, ccl_data['pk_lin'].values, size = 5, legend = "ccl data")
    p.line(cclK, cclPk, line_width = 2)
    p.circle(cclK, cclPk, size = 5,fill_alpha=0.8, legend = "ccl data")

    #p.circle(classData['k'].values, classData['P'].values, size = 5, color = "red", legend = "class data")
    p.line(classKLin, classPLin, line_width = 2)
    p.circle(classKLin, classPLin, size = 5,fill_alpha=0.8,color = "red", legend = "class data")

    # Set the x axis label
    # Set the y axis label
    p.yaxis.axis_label = 'Count (log)'
    comparisonValue = abs(cclPk - classPLin) / classPLin
    p2.line(classKLin, comparisonValue, line_width = 2)
    p2.circle(classKLin, abs(cclPk - classPLin) / classPLin, size = 5, fill_color = "white")
    plot = gridplot([[p],[p2]])
    return plot


def create_nl(index):
    # load the data
    i = int(index)

    fname = "/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_nl_%05dz1_pk.dat" % (i)
    #ccl_data = pd.read_table(fname,
        #names=["k", "pk_lin"], skiprows = 1, delim_whitespace = True)
    cclData = np.loadtxt(fname, skiprows = 1)
    cclK = cclData[:, 0]
    cclPk = cclData[:, 1]
    data = np.loadtxt('/Users/penafiel/JPL/data/par_stan1.csv', skiprows = 1)


    fname = "/Users/penafiel/JPL/class/output/nonlin/lhs_nonlin_%05dz1_pk_nl.dat" % (i)
    #classData = pd.read_table(fname,
        #names=["k", "P"], skiprows = 4, delim_whitespace = True)
    classData = np.loadtxt(fname, skiprows = 4);
    classKLin = classData[:, 0]
    classPLin = classData[:, 1]

    #Multiply by factors
    #multiply k by some factor of h, CLASS and CCL use different units, ugh
    h = float(data[i,1])

    classKLin *= h
    classPLin /= h**3

    # create a plot and style its properties
    p = figure(toolbar_location="right", title = "CCL Validation", x_axis_type = "log", y_axis_type = "log",
        tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")

    p2 = figure(toolbar_location="right", title = "CCL Validation", x_axis_type = "log", y_axis_type = "log",
        tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")

    p.outline_line_color = None
    p.grid.grid_line_color = None

    p2.outline_line_color = None
    p2.grid.grid_line_color = None

    # plot the data
    #p.circle(ccl_data['k'].values, ccl_data['pk_lin'].values, size = 5, legend = "ccl data")
    p.line(cclK, cclPk, line_width = 2)
    p.circle(cclK, cclPk, size = 5,fill_alpha=0.8, legend = "ccl data")

    #p.circle(classData['k'].values, classData['P'].values, size = 5, color = "red", legend = "class data")
    p.line(classKLin, classPLin, line_width = 2)
    p.circle(classKLin, classPLin, size = 5, fill_alpha=0.8, color = "red", legend = "class data")

    # Set the x axis label
    # Set the y axis label
    p.yaxis.axis_label = 'Count (log)'
    comparisonValue = abs(cclPk - classPLin) / classPLin
    p2.line(classKLin, comparisonValue, line_width = 2)
    p2.circle(classKLin, abs(cclPk - classPLin) / classPLin, size = 5, fill_color = "white")
    plot = gridplot([[p],[p2]])
    return plot

def create_lin_pre(index):
    # load the data
    i = int(index)

    fname = "/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_lin_pk_%05dz1_pk.dat" % (i)
    #ccl_data = pd.read_table(fname,
        #names=["k", "pk_lin"], skiprows = 1, delim_whitespace = True)
    cclData = np.loadtxt(fname, skiprows = 1)
    cclK = cclData[:, 0]
    cclPk = cclData[:, 1]
    data = np.loadtxt('/Users/penafiel/JPL/data/par_stan1.csv', skiprows = 1)


    fname = "/Users/penafiel/JPL/class/output/lin/lhs_lin_pk_%05dz1_pk.dat" % (i)
    #classData = pd.read_table(fname,
        #names=["k", "P"], skiprows = 4, delim_whitespace = True)
    classData = np.loadtxt(fname, skiprows = 4);
    classKLin = classData[:, 0]
    classPLin = classData[:, 1]

    #Multiply by factors
    #multiply k by some factor of h, CLASS and CCL use different units, ugh
    h = float(data[i,1])

    classKLin *= h
    classPLin /= h**3

    # create a plot and style its properties
    p = figure(toolbar_location="right", title = "CCL Validation", x_axis_type = "log", y_axis_type = "log",
        tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")

    p2 = figure(toolbar_location="right", title = "CCL Validation", x_axis_type = "log", y_axis_type = "log",
        tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")

    p.outline_line_color = None
    p.grid.grid_line_color = None

    p2.outline_line_color = None
    p2.grid.grid_line_color = None

    # plot the data
    #p.circle(ccl_data['k'].values, ccl_data['pk_lin'].values, size = 5, legend = "ccl data")
    p.line(cclK, cclPk, line_width = 2)
    p.circle(cclK, cclPk, size = 6, fill_alpha=0.8,legend = "ccl data")

    #p.circle(classData['k'].values, classData['P'].values, size = 5, color = "red", legend = "class data")
    p.line(classKLin, classPLin, line_width = 2)
    p.circle(classKLin, classPLin, size = 5, fill_alpha=0.8, color = "red", legend = "class data")

    # Set the x axis label
    # Set the y axis label
    p.yaxis.axis_label = 'Count (log)'
    comparisonValue = abs(cclPk - classPLin) / classPLin
    p2.line(classKLin, comparisonValue, line_width = 2)
    p2.circle(classKLin, abs(cclPk - classPLin) / classPLin, size = 5, fill_color = "white")
    plot = gridplot([[p],[p2]])
    return plot

def create_nl_pre(index):
    # load the data
    i = int(index)

    fname = "/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_nl_pk_%05dz1_pk.dat" % (i)
    #ccl_data = pd.read_table(fname,
        #names=["k", "pk_lin"], skiprows = 1, delim_whitespace = True)
    cclData = np.loadtxt(fname, skiprows = 1)
    cclK = cclData[:, 0]
    cclPk = cclData[:, 1]
    data = np.loadtxt('/Users/penafiel/JPL/data/par_stan1.csv', skiprows = 1)


    fname = "/Users/penafiel/JPL/class/output/nonlin/lhs_nonlin_pk_%05dz1_pk_nl.dat" % (i)
    #classData = pd.read_table(fname,
        #names=["k", "P"], skiprows = 4, delim_whitespace = True)
    classData = np.loadtxt(fname, skiprows = 4);
    classKLin = classData[:, 0]
    classPLin = classData[:, 1]

    #Multiply by factors
    #multiply k by some factor of h, CLASS and CCL use different units, ugh
    h = float(data[i,1])

    classKLin *= h
    classPLin /= h**3

    # create a plot and style its properties
    p = figure(toolbar_location="right", title = "CCL Validation", x_axis_type = "log", y_axis_type = "log",
        tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")

    p2 = figure(toolbar_location="right", title = "CCL Validation", x_axis_type = "log", y_axis_type = "log",
        tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")

    p.outline_line_color = None
    p.grid.grid_line_color = None

    p2.outline_line_color = None
    p2.grid.grid_line_color = None

    # plot the data
    #p.circle(ccl_data['k'].values, ccl_data['pk_lin'].values, size = 5, legend = "ccl data")
    p.line(cclK, cclPk, line_width = 2)
    p.circle(cclK, cclPk, size = 5,legend = "ccl data")

    #p.circle(classData['k'].values, classData['P'].values, size = 5, color = "red", legend = "class data")
    p.line(classKLin, classPLin, line_width = 2)
    p.circle(classKLin, classPLin, size = 5, fill_alpha=0.8, color = "red", legend = "class data")

    # Set the x axis label
    # Set the y axis label
    p.yaxis.axis_label = 'Count (log)'
    comparisonValue = abs(cclPk - classPLin) / classPLin
    p2.line(classKLin, comparisonValue, line_width = 2)
    p2.circle(classKLin, abs(cclPk - classPLin) / classPLin, fill_alpha=0.8,size = 5, fill_color = "white")
    plot = gridplot([[p],[p2]])
    return plot

#LETS IMPLEMENT A CLICK
@app.route('/')
def home():
    #load the data
    data = np.loadtxt('/Users/penafiel/JPL/data/par_stan1.csv', skiprows=1)
    tot_tot = np.loadtxt('/Users/penafiel/JPL/data/tot_tot.txt')

    #Load the parameter values and total failures, since it will be easier to load
    trial_arr = data[:,0]
    h_arr = data[:,1]
    Omega_b_arr = data[:,2]
    Omega_cdm_arr = data[:,3]
    A_s_arr = data[:,4]
    n_s_arr = data[:,5]
    #Gets the extension depending on which mode you choose
    #tot_tot_lin = tot_tot[:,0]
    #tot_tot_nl = tot_tot[:,1]
    #tot_tot_lin_pre = tot_tot[:,2]
    #tot_tot_nl_pre = tot_tot[:,3]

    ####################################################
    #CALCULATE THE VALUES FOR HOW BADLY SOMETHING FAILS#
    ####################################################

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

    #load the data
    tot_tot = np.loadtxt('/Users/penafiel/JPL/data/tot_tot.txt')


    #Create arrays that will be filled in the loop over trials
    #Total of the wights
    tot_tot_lin = []
    tot_tot_nl = []
    tot_tot_lin_pre = []
    tot_tot_nl_pre = []

    #Get the totals for different k_ranges
    #We have 3 k_ranges, denote by 1,2,3
    #1 = Ultra Large Scales
    #2 = Linear scales
    #3 = Nonlinear scales

    #But we have to do this for different z_values as well
    #Probably a more efficient way of writing this, but I think this will suffice
    tot_lin_k1_z1 = []
    tot_lin_k2_z1 = []
    tot_lin_k3_z1 = []
    
    tot_lin_k1_z2 = []
    tot_lin_k2_z2 = []
    tot_lin_k3_z2 = []
    
    tot_lin_k1_z3 = []
    tot_lin_k2_z3 = []
    tot_lin_k3_z3 = []
    
    tot_lin_k1_z4 = []
    tot_lin_k2_z4 = []
    tot_lin_k3_z4 = []
    
    tot_lin_k1_z5 = []
    tot_lin_k2_z5 = []
    tot_lin_k3_z5 = []
    
    tot_lin_k1_z6 = []
    tot_lin_k2_z6 = []
    tot_lin_k3_z6 = []
    
    tot_nl_k1_z1 = []
    tot_nl_k2_z1 = []
    tot_nl_k3_z1 = []

    tot_nl_k1_z2 = []
    tot_nl_k2_z2 = []
    tot_nl_k3_z2 = []

    tot_nl_k1_z3 = []
    tot_nl_k2_z3 = []
    tot_nl_k3_z3 = []

    tot_nl_k1_z4 = []
    tot_nl_k2_z4 = []
    tot_nl_k3_z4 = []

    tot_nl_k1_z5 = []
    tot_nl_k2_z5 = []
    tot_nl_k3_z5 = []

    tot_nl_k1_z6 = []
    tot_nl_k2_z6 = []
    tot_nl_k3_z6 = []

    tot_lin_pre_k1_z1 = []
    tot_lin_pre_k2_z1 = []
    tot_lin_pre_k3_z1 = []

    tot_lin_pre_k1_z2 = []
    tot_lin_pre_k2_z2 = []
    tot_lin_pre_k3_z2 = []

    tot_lin_pre_k1_z3 = []
    tot_lin_pre_k2_z3 = []
    tot_lin_pre_k3_z3 = []

    tot_lin_pre_k1_z4 = []
    tot_lin_pre_k2_z4 = []
    tot_lin_pre_k3_z4 = []

    tot_lin_pre_k1_z5 = []
    tot_lin_pre_k2_z5 = []
    tot_lin_pre_k3_z5 = []

    tot_lin_pre_k1_z6 = []
    tot_lin_pre_k2_z6 = []
    tot_lin_pre_k3_z6 = []

    tot_nl_pre_k1_z1 = []
    tot_nl_pre_k2_z1 = []
    tot_nl_pre_k3_z1 = []

    tot_nl_pre_k1_z2 = []
    tot_nl_pre_k2_z2 = []
    tot_nl_pre_k3_z2 = []

    tot_nl_pre_k1_z3 = []
    tot_nl_pre_k2_z3 = []
    tot_nl_pre_k3_z3 = []

    tot_nl_pre_k1_z4 = []
    tot_nl_pre_k2_z4 = []
    tot_nl_pre_k3_z4 = []

    tot_nl_pre_k1_z5 = []
    tot_nl_pre_k2_z5 = []
    tot_nl_pre_k3_z5 = []

    tot_nl_pre_k1_z6 = []
    tot_nl_pre_k2_z6 = []
    tot_nl_pre_k3_z6 = []

    ###########################
    #                         #
    #GETTING THE SUMMARY STATS#
    #                         #
    ###########################
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

        #Appending the values for the k ranges
        tot_lin_k1_z1 = np.append(tot_lin_k1_z1, tot_lin_ll[0][0])
        tot_lin_k2_z1 = np.append(tot_lin_k2_z1, tot_lin_ll[0][1])
        tot_lin_k3_z1 = np.append(tot_lin_k3_z1, tot_lin_ll[0][2])

        tot_lin_k1_z2 = np.append(tot_lin_k1_z2, tot_lin_ll[1][0])
        tot_lin_k2_z2 = np.append(tot_lin_k2_z2, tot_lin_ll[1][1])
        tot_lin_k3_z2 = np.append(tot_lin_k3_z2, tot_lin_ll[1][2])

        tot_lin_k1_z3 = np.append(tot_lin_k1_z3, tot_lin_ll[2][0])
        tot_lin_k2_z3 = np.append(tot_lin_k2_z3, tot_lin_ll[2][1])
        tot_lin_k3_z3 = np.append(tot_lin_k3_z3, tot_lin_ll[2][2])

        tot_lin_k1_z4 = np.append(tot_lin_k1_z4, tot_lin_ll[3][0])
        tot_lin_k2_z4 = np.append(tot_lin_k2_z4, tot_lin_ll[3][1])
        tot_lin_k3_z4 = np.append(tot_lin_k3_z4, tot_lin_ll[3][2])

        tot_lin_k1_z5 = np.append(tot_lin_k1_z5, tot_lin_ll[4][0])
        tot_lin_k2_z5 = np.append(tot_lin_k2_z5, tot_lin_ll[4][1])
        tot_lin_k3_z5 = np.append(tot_lin_k3_z5, tot_lin_ll[4][2])

        tot_lin_k1_z6 = np.append(tot_lin_k1_z6, tot_lin_ll[5][0])
        tot_lin_k2_z6 = np.append(tot_lin_k2_z6, tot_lin_ll[5][1])
        tot_lin_k3_z6 = np.append(tot_lin_k3_z6, tot_lin_ll[5][2])

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

        #Appending the values for the k ranges
        tot_nl_k1_z1 = np.append(tot_nl_k1_z1, tot_nl_ll[0][0])
        tot_nl_k2_z1 = np.append(tot_nl_k2_z1, tot_nl_ll[0][1])
        tot_nl_k3_z1 = np.append(tot_nl_k3_z1, tot_nl_ll[0][2])

        tot_nl_k1_z2 = np.append(tot_nl_k1_z2, tot_nl_ll[1][0])
        tot_nl_k2_z2 = np.append(tot_nl_k2_z2, tot_nl_ll[1][1])
        tot_nl_k3_z2 = np.append(tot_nl_k3_z2, tot_nl_ll[1][2])

        tot_nl_k1_z3 = np.append(tot_nl_k1_z3, tot_nl_ll[2][0])
        tot_nl_k2_z3 = np.append(tot_nl_k2_z3, tot_nl_ll[2][1])
        tot_nl_k3_z3 = np.append(tot_nl_k3_z3, tot_nl_ll[2][2])

        tot_nl_k1_z4 = np.append(tot_nl_k1_z4, tot_nl_ll[3][0])
        tot_nl_k2_z4 = np.append(tot_nl_k2_z4, tot_nl_ll[3][1])
        tot_nl_k3_z4 = np.append(tot_nl_k3_z4, tot_nl_ll[3][2])

        tot_nl_k1_z5 = np.append(tot_nl_k1_z5, tot_nl_ll[4][0])
        tot_nl_k2_z5 = np.append(tot_nl_k2_z5, tot_nl_ll[4][1])
        tot_nl_k3_z5 = np.append(tot_nl_k3_z5, tot_nl_ll[4][2])

        tot_nl_k1_z6 = np.append(tot_nl_k1_z6, tot_nl_ll[5][0])
        tot_nl_k2_z6 = np.append(tot_nl_k2_z6, tot_nl_ll[5][1])
        tot_nl_k3_z6 = np.append(tot_nl_k3_z6, tot_nl_ll[5][2])

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

        #Appending the values for the k ranges
        tot_lin_pre_k1_z1 = np.append(tot_lin_pre_k1_z1, tot_lin_pre_ll[0][0])
        tot_lin_pre_k2_z1 = np.append(tot_lin_pre_k2_z1, tot_lin_pre_ll[0][1])
        tot_lin_pre_k3_z1 = np.append(tot_lin_pre_k3_z1, tot_lin_pre_ll[0][2])

        tot_lin_pre_k1_z2 = np.append(tot_lin_pre_k1_z2, tot_lin_pre_ll[1][0])
        tot_lin_pre_k2_z2 = np.append(tot_lin_pre_k2_z2, tot_lin_pre_ll[1][1])
        tot_lin_pre_k3_z2 = np.append(tot_lin_pre_k3_z2, tot_lin_pre_ll[1][2])

        tot_lin_pre_k1_z3 = np.append(tot_lin_pre_k1_z3, tot_lin_pre_ll[2][0])
        tot_lin_pre_k2_z3 = np.append(tot_lin_pre_k2_z3, tot_lin_pre_ll[2][1])
        tot_lin_pre_k3_z3 = np.append(tot_lin_pre_k3_z3, tot_lin_pre_ll[2][2])

        tot_lin_pre_k1_z4 = np.append(tot_lin_pre_k1_z4, tot_lin_pre_ll[3][0])
        tot_lin_pre_k2_z4 = np.append(tot_lin_pre_k2_z4, tot_lin_pre_ll[3][1])
        tot_lin_pre_k3_z4 = np.append(tot_lin_pre_k3_z4, tot_lin_pre_ll[3][2])

        tot_lin_pre_k1_z5 = np.append(tot_lin_pre_k1_z5, tot_lin_pre_ll[4][0])
        tot_lin_pre_k2_z5 = np.append(tot_lin_pre_k2_z5, tot_lin_pre_ll[4][1])
        tot_lin_pre_k3_z5 = np.append(tot_lin_pre_k3_z5, tot_lin_pre_ll[4][2])

        tot_lin_pre_k1_z6 = np.append(tot_lin_pre_k1_z6, tot_lin_pre_ll[5][0])
        tot_lin_pre_k2_z6 = np.append(tot_lin_pre_k2_z6, tot_lin_pre_ll[5][1])
        tot_lin_pre_k3_z6 = np.append(tot_lin_pre_k3_z6, tot_lin_pre_ll[5][2])

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

        #Appending the values for the k ranges
        tot_nl_pre_k1_z1 = np.append(tot_nl_pre_k1_z1, tot_nl_pre_ll[0][0])
        tot_nl_pre_k2_z1 = np.append(tot_nl_pre_k2_z1, tot_nl_pre_ll[0][1])
        tot_nl_pre_k3_z1 = np.append(tot_nl_pre_k3_z1, tot_nl_pre_ll[0][2])

        tot_nl_pre_k1_z2 = np.append(tot_nl_pre_k1_z2, tot_nl_pre_ll[1][0])
        tot_nl_pre_k2_z2 = np.append(tot_nl_pre_k2_z2, tot_nl_pre_ll[1][1])
        tot_nl_pre_k3_z2 = np.append(tot_nl_pre_k3_z2, tot_nl_pre_ll[1][2])

        tot_nl_pre_k1_z3 = np.append(tot_nl_pre_k1_z3, tot_nl_pre_ll[2][0])
        tot_nl_pre_k2_z3 = np.append(tot_nl_pre_k2_z3, tot_nl_pre_ll[2][1])
        tot_nl_pre_k3_z3 = np.append(tot_nl_pre_k3_z3, tot_nl_pre_ll[2][2])

        tot_nl_pre_k1_z4 = np.append(tot_nl_pre_k1_z4, tot_nl_pre_ll[3][0])
        tot_nl_pre_k2_z4 = np.append(tot_nl_pre_k2_z4, tot_nl_pre_ll[3][1])
        tot_nl_pre_k3_z4 = np.append(tot_nl_pre_k3_z4, tot_nl_pre_ll[3][2])

        tot_nl_pre_k1_z5 = np.append(tot_nl_pre_k1_z5, tot_nl_pre_ll[4][0])
        tot_nl_pre_k2_z5 = np.append(tot_nl_pre_k2_z5, tot_nl_pre_ll[4][1])
        tot_nl_pre_k3_z5 = np.append(tot_nl_pre_k3_z5, tot_nl_pre_ll[4][2])

        tot_nl_pre_k1_z6 = np.append(tot_nl_pre_k1_z6, tot_nl_pre_ll[5][0])
        tot_nl_pre_k2_z6 = np.append(tot_nl_pre_k2_z6, tot_nl_pre_ll[5][1])
        tot_nl_pre_k3_z6 = np.append(tot_nl_pre_k3_z6, tot_nl_pre_ll[5][2])

        tot_tot_nl_pre = np.append(tot_tot_nl_pre, np.sum(tot_nl_pre))

    #Creates a dictionary since that's what ColumnDataSource takes in
    data_lin = {'tot_tot_lin':tot_tot_lin,
                'tot_lin_k1_z1':tot_lin_k1_z1,
                'tot_lin_k2_z1':tot_lin_k2_z1,
                'tot_lin_k3_z1':tot_lin_k3_z1,
                'tot_lin_k1_z2':tot_lin_k1_z2,
                'tot_lin_k2_z2':tot_lin_k2_z2,
                'tot_lin_k3_z2':tot_lin_k3_z2,
                'tot_lin_k1_z3':tot_lin_k1_z3,
                'tot_lin_k2_z3':tot_lin_k2_z3,
                'tot_lin_k3_z3':tot_lin_k3_z3,
                'tot_lin_k1_z4':tot_lin_k1_z4,
                'tot_lin_k2_z4':tot_lin_k2_z4,
                'tot_lin_k3_z4':tot_lin_k3_z4,
                'tot_lin_k1_z5':tot_lin_k1_z5,
                'tot_lin_k2_z5':tot_lin_k2_z5,
                'tot_lin_k3_z5':tot_lin_k3_z5,
                'tot_lin_k1_z6':tot_lin_k1_z6,
                'tot_lin_k2_z6':tot_lin_k2_z6,
                'tot_lin_k3_z6':tot_lin_k3_z6}
    data_nl = {'tot_tot_nl':tot_tot_nl,
                'tot_nl_k1_z1':tot_nl_k1_z1,
                'tot_nl_k2_z1':tot_nl_k2_z1,
                'tot_nl_k3_z1':tot_nl_k3_z1,
                'tot_nl_k1_z2':tot_nl_k1_z2,
                'tot_nl_k2_z2':tot_nl_k2_z2,
                'tot_nl_k3_z2':tot_nl_k3_z2,
                'tot_nl_k1_z3':tot_nl_k1_z3,
                'tot_nl_k2_z3':tot_nl_k2_z3,
                'tot_nl_k3_z3':tot_nl_k3_z3,
                'tot_nl_k1_z4':tot_nl_k1_z4,
                'tot_nl_k2_z4':tot_nl_k2_z4,
                'tot_nl_k3_z4':tot_nl_k3_z4,
                'tot_nl_k1_z5':tot_nl_k1_z5,
                'tot_nl_k2_z5':tot_nl_k2_z5,
                'tot_nl_k3_z5':tot_nl_k3_z5,
                'tot_nl_k1_z6':tot_nl_k1_z6,
                'tot_nl_k2_z6':tot_nl_k2_z6,
                'tot_nl_k3_z6':tot_nl_k3_z6}
    data_lin_pre = {'tot_tot_lin_pre':tot_tot_lin_pre,
                'tot_lin_pre_k1_z1':tot_lin_pre_k1_z1,
                'tot_lin_pre_k2_z1':tot_lin_pre_k2_z1,
                'tot_lin_pre_k3_z1':tot_lin_pre_k3_z1,
                'tot_lin_pre_k1_z2':tot_lin_pre_k1_z2,
                'tot_lin_pre_k2_z2':tot_lin_pre_k2_z2,
                'tot_lin_pre_k3_z2':tot_lin_pre_k3_z2,
                'tot_lin_pre_k1_z3':tot_lin_pre_k1_z3,
                'tot_lin_pre_k2_z3':tot_lin_pre_k2_z3,
                'tot_lin_pre_k3_z3':tot_lin_pre_k3_z3,
                'tot_lin_pre_k1_z4':tot_lin_pre_k1_z4,
                'tot_lin_pre_k2_z4':tot_lin_pre_k2_z4,
                'tot_lin_pre_k3_z4':tot_lin_pre_k3_z4,
                'tot_lin_pre_k1_z5':tot_lin_pre_k1_z5,
                'tot_lin_pre_k2_z5':tot_lin_pre_k2_z5,
                'tot_lin_pre_k3_z5':tot_lin_pre_k3_z5,
                'tot_lin_pre_k1_z6':tot_lin_pre_k1_z6,
                'tot_lin_pre_k2_z6':tot_lin_pre_k2_z6,
                'tot_lin_pre_k3_z6':tot_lin_pre_k3_z6}
    data_nl_pre = {'tot_tot_nl_pre':tot_tot_nl_pre,
                'tot_nl_pre_k1_z1':tot_nl_pre_k1_z1,
                'tot_nl_pre_k2_z1':tot_nl_pre_k2_z1,
                'tot_nl_pre_k3_z1':tot_nl_pre_k3_z1,
                'tot_nl_pre_k1_z2':tot_nl_pre_k1_z2,
                'tot_nl_pre_k2_z2':tot_nl_pre_k2_z2,
                'tot_nl_pre_k3_z2':tot_nl_pre_k3_z2,
                'tot_nl_pre_k1_z3':tot_nl_pre_k1_z3,
                'tot_nl_pre_k2_z3':tot_nl_pre_k2_z3,
                'tot_nl_pre_k3_z3':tot_nl_pre_k3_z3,
                'tot_nl_pre_k1_z4':tot_nl_pre_k1_z4,
                'tot_nl_pre_k2_z4':tot_nl_pre_k2_z4,
                'tot_nl_pre_k3_z4':tot_nl_pre_k3_z4,
                'tot_nl_pre_k1_z5':tot_nl_pre_k1_z5,
                'tot_nl_pre_k2_z5':tot_nl_pre_k2_z5,
                'tot_nl_pre_k3_z5':tot_nl_pre_k3_z5,
                'tot_nl_pre_k1_z6':tot_nl_pre_k1_z6,
                'tot_nl_pre_k2_z6':tot_nl_pre_k2_z6,
                'tot_nl_pre_k3_z6':tot_nl_pre_k3_z6}

    source_lin = ColumnDataSource(data=data_lin)
    source_nl = ColumnDataSource(data=data_nl)
    source_lin_pre = ColumnDataSource(data=data_lin_pre)
    source_nl_pre = ColumnDataSource(data=data_nl_pre)

    #Uses this dictionary, since if using x,y for fig.rect
    #That will lead to x, and y values changing all the time
    #So calling the dictionary value is better and won't fuck up your plots
    source_data = ColumnDataSource(data={'tot_tot_data':tot_tot_lin, 'h_arr':h_arr, 
                               'Omega_b_arr':Omega_b_arr, 'Omega_cdm_arr':Omega_cdm_arr,
                               'A_s_arr':A_s_arr, 'n_s_arr':n_s_arr, 'trial_arr':trial_arr})
    #Bokeh's a bitch, so I have to individually plot each one first

    #initialize the color values, this is Gn To Red
    colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
    #Mapper corresponding to the tot_tot_data
    mapper = LinearColorMapper(palette=colors, low=0, high=1000)

    #Create hover tool, Fuck Bokeh, I have to declare multiple instances of this shit
    hover1 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])

    hover2 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])
    
    hover3 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])
    
    hover4 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])
    
    hover5 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])
    
    hover6 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])
    
    hover7 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])
    
    hover8 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])
    
    hover9 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])
    
    hover10 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])

    #What tools do I want
    TOOLS = 'hover, pan, wheel_zoom, box_zoom, save, resize, reset'
    #Makes the plot
    s1 = figure(plot_width=300, plot_height=300,tools=[hover1, TapTool()])

    s1.grid.grid_line_color = None
    #Plots the rectangles
    s1_rect = s1.rect('h_arr', 'Omega_b_arr',width=0.05, height=0.0034, alpha=0.8, source=source_data,fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s1.yaxis.axis_label = '$\Omega_b$'
    
    s2 = figure(plot_width=300, plot_height=300, tools=[hover2, TapTool()])
    s2.grid.grid_line_color=None
    s2_rect = s2.rect('h_arr', 'Omega_cdm_arr', width=0.05, height=0.035, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s2.yaxis.axis_label = '$\Omega_{cdm}$' 

    s3 = figure(plot_width=300, plot_height=300, tools=[hover3, TapTool()])
    s3.grid.grid_line_color = None
    #Plots the rectangles
    s3_rect = s3.rect('Omega_b_arr', 'Omega_cdm_arr',width=0.0034, height=0.035, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    
    s4 = figure(plot_width=300, plot_height=300, tools=[hover4, TapTool()])
    s4.grid.grid_line_color = None
    #Plots the rectangles
    s4_rect = s4.rect('h_arr', 'A_s_arr',width=0.05, height=0.09e-9, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s4.yaxis.axis_label = '$\A_s$' 

    s5 = figure(plot_width=300, plot_height=300, tools=[hover5, TapTool()])
    s5.grid.grid_line_color = None
    s5_rect = s5.rect('Omega_b_arr', 'A_s_arr',width=0.0034, height=0.09e-9, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)

    s6 = figure(plot_width=300, plot_height=300, tools=[hover6, TapTool()])
    s6.grid.grid_line_color = None
    s6_rect = s6.rect('Omega_cdm_arr', 'A_s_arr',width=0.035, height=0.09e-9, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)

    s7 = figure(plot_width=300, plot_height=300, tools=[hover7, TapTool()])
    s7.grid.grid_line_color = None
    s7_rect = s7.rect('h_arr', 'n_s_arr',width=0.05, height=0.0068, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s7.yaxis.axis_label = '$n_s$'
    s7.xaxis.axis_label = '$h$'
   
    s8 = figure(plot_width=300, plot_height=300, tools=[hover8,TapTool()])
    s8.grid.grid_line_color = None
    s8_rect = s8.rect('Omega_b_arr', 'n_s_arr', width=0.0034, height=0.0068, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s8.xaxis.axis_label = '$\Omega_b$'

    s9 = figure(plot_width=300, plot_height=300, tools=[hover9, TapTool()])
    s9.grid.grid_line_color = None
    s9_rect = s9.rect('Omega_cdm_arr', 'n_s_arr', width=0.035, height=0.0068, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s9.xaxis.axis_label = '$\Omega_{cdm}$'

    s10 = figure(plot_width=300, plot_height=300,tools=[hover10, TapTool()])
    s10.grid.grid_line_color = None
    s10_rect = s10.rect('A_s_arr', 'n_s_arr', width=0.09e-9, height=0.0068, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s10.xaxis.axis_label = '$A_s$'
   
    #Create glyphs for the highlighting portion, so that when it is tapped
    #the colors don't change

    selected = Rect(fill_color={'field':'tot_tot_data', 'transform':mapper}, fill_alpha=0.8, line_color=None)
    nonselected = Rect(fill_color={'field':'tot_tot_data', 'transform':mapper}, fill_alpha=0.8, line_color=None)

    s1_rect.selection_glyph = selected
    s1_rect.nonselection_glyph = nonselected

    s2_rect.selection_glyph = selected
    s2_rect.nonselection_glyph = nonselected

    s3_rect.selection_glyph = selected
    s3_rect.nonselection_glyph = nonselected

    s4_rect.selection_glyph = selected
    s4_rect.nonselection_glyph = nonselected

    s5_rect.selection_glyph = selected
    s5_rect.nonselection_glyph = nonselected
    
    s6_rect.selection_glyph = selected
    s6_rect.nonselection_glyph = nonselected

    s7_rect.selection_glyph = selected
    s7_rect.nonselection_glyph = nonselected

    s8_rect.selection_glyph = selected
    s8_rect.nonselection_glyph = nonselected

    s9_rect.selection_glyph = selected
    s9_rect.nonselection_glyph = nonselected

    s10_rect.selection_glyph = selected
    s10_rect.nonselection_glyph = nonselected
    #Creates the color bar and adds it to the right side of the big plot
    
    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size='5pt',
                    ticker=BasicTicker(desired_num_ticks=len(colors)),
                    label_standoff=6, border_line_color=None, location=(0,0))

    s_color = figure()
    #Since this basically creates another plot, we want to remove it
    #That's what the next couple of lines does
    s_color.grid.grid_line_color = None
    s_color.axis.axis_line_color = None
    s_color.add_layout(color_bar, 'left')
    s_color.toolbar.logo = None
    s_color.toolbar_location = None


    #Creates the gridplot to be reminscient of a corner plot
    plot = gridplot([[s1, None, None, None], [s2, s3, None, None], [s4,s5,s6, None], [s7,s8,s9,s10]])

    #Code to be utilized by the JavaScript in the interface
    code_sliders="""
    //Get the range of our k_Slider
    var k = k_slider.range;
    var k_start = k_slider.range[0];
    var k_end = k_slider.range[1];


    //Get the range of our z_Slider
    var z = z_slider.range;
    var start = z_slider.range[0];
    var end = z_slider.range[1];
    console.log(start);
    console.log(end);

    //Get the mode in the dropdown
    var mode_selected = dropdown.value;

    //All of our data
    var tot_data = source_data.data;
    var tot_lin = js_lin.data;
    var tot_nl = js_nl.data;
    var tot_lin_pre = js_lin_pre.data;
    var tot_nl_pre = js_nl_pre.data;
    var sum = 0;
    console.log(mode_selected);
    if (mode_selected == "Linear") {
        //Create a loop for the ranges
        for (var i = 0; i <tot_data['tot_tot_data'].length; i++) {
            sum = 0;
            for(var j = start; j<=end; j=j+0.5){
                z_string = String((j*2)+1);
                for (var l = k_start; l<= k_end; l++) {
                    k_string = String(l);
                    sum += tot_lin['tot_lin_k' + k_string + '_z' + z_string][i];
                } // k_range

            } // z_value

            tot_data['tot_tot_data'][i] = sum;
        } // sum
    }

    if (mode_selected == "Non-Linear") {
        //Create a loop for the ranges
        for (var i = 0; i <tot_data['tot_tot_data'].length; i++) {
            sum = 0;
            for(var j = start; j<=end; j=j+0.5){
                z_string = String((j * 2)+1);
                for (var l = k_start; l<=k_end; l++) {
                    k_string = String(l);
                    sum += tot_nl['tot_nl_k' + k_string + '_z' + z_string][i];
                } // k_range
            } // z_value

            tot_data['tot_tot_data'][i] = sum;
            
        } // sum
    }

    if (mode_selected == "Linear, Precision"){
        
        //Create a loop for the ranges
        for (var i = 0; i <tot_data['tot_tot_data'].length; i++) {
            sum = 0;
            for(var j = start; j<=end; j=j+0.5){
                z_string = String((j * 2)+1);
                for (var l = k_start; l<=k_end; l++) {
                    k_string = String(l);
                    sum += tot_lin_pre['tot_lin_pre_k' + k_string + '_z' + z_string][i];

                } // k_range
            
            } // z_value

            tot_data['tot_tot_data'][i] = sum;
        } // sum
    }

    if (mode_selected == "Non-Linear, Precision"){
       
        //Create a loop for the ranges
        for (var i = 0; i <tot_data['tot_tot_data'].length; i++) {
            sum = 0;
            for(var j = start; j<=end; j=j+0.5){
                z_string = String((j * 2)+1);
                for (var l = k_start; l<=k_end; l++) {
                    k_string = String(l);
                    sum += tot_nl_pre['tot_nl_pre_k' + k_string + '_z' + z_string][i];
                } // k_range
            
            } // z_value
            tot_data['tot_tot_data'][i] = sum;
        } // sum
    }
    console.log(tot_data['tot_tot_data']);
    source_data.trigger('change');

    """

    callback_sliders = CustomJS(args=dict(source_data=source_data, js_lin=source_lin, js_nl=source_nl, js_lin_pre=source_lin_pre, js_nl_pre=source_nl_pre), code=code_sliders)
    
    #Creates the selection menu for the select
    selection_men = ['Linear', 'Non-Linear', 'Linear, Precision', 'Non-Linear, Precision']
    dropdown = Select(title='Mode', value=selection_men[0], options=selection_men, callback=callback_sliders)

    #Create the RangeSlider for the z values
    z_slider = RangeSlider(start=0, end=2.5, range=(0,2.5), step=0.5, title='Range of z values', callback=callback_sliders)
    
    #Create the RangeSlider for the k values
    k_slider = RangeSlider(start=1, end=3, range=(1,3), step=1, title='Range of k values', callback=callback_sliders)

    callback_sliders.args['k_slider'] = k_slider
    callback_sliders.args['z_slider'] = z_slider
    callback_sliders.args['dropdown'] = dropdown
    
    #Make it open a new URL on tap
    #Bokeh is again a bitch, so we gotta initiate multiple instances
    taptool = s1.select(type=TapTool)
    code_tap="""
        //Get the value 'Tapped'
        var index_selected=source.selected['1d'].indices[0];
        console.log(index_selected);
        //Get the mode in the dropdown
        var mode_selected = dropdown.value;
        console.log(mode_selected);
        //Initialize the starting URL
        var url = 'http://127.0.0.1:5000/'

        if (mode_selected == "Linear") {
        var url_mode = 'lin/'
        var url_index = '?index=' + String(index_selected)
        url_use = url + url_mode + url_index
        window.open(url_use)
        }

        if (mode_selected == "Non-Linear") {
        var url_mode = 'nl/'
        var url_index = '?index=' + String(index_selected)
        url_use = url + url_mode + url_index
        window.open(url_use)
        }

        if (mode_selected == "Linear, Precision"){
        var url_mode = 'lin_pre/'
        var url_index = '?index=' + String(index_selected)
        url_use = url + url_mode + url_index
        window.open(url_use)
        }

        if (mode_selected == "Non-Linear, Precision"){
        var url_mode = 'nl_pre/'
        var url_index = '?index=' + String(index_selected)
        url_use = url + url_mode + url_index
        window.open(url_use)
        }
    """


        
    taptool.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))
    
    taptool2 = s2.select(type=TapTool)
    taptool2.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool3 = s3.select(type=TapTool)
    taptool3.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool4 = s4.select(type=TapTool)
    taptool4.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool5 = s5.select(type=TapTool)
    taptool5.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool6 = s6.select(type=TapTool)
    taptool6.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool7 = s7.select(type=TapTool)
    taptool7.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool8 = s8.select(type=TapTool)
    taptool8.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool9 = s9.select(type=TapTool)
    taptool9.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool10 = s10.select(type=TapTool)
    taptool10.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    

    #plot = create_corner(comp_ll, source_data.data['tot_tot_data'])
    #script, div_dict = components(plot)#components({'plot':plot, 'dropdown':dropdown})
    #script, div_dict = components({'plot':plot, 'dropdown':HBox(dropdown, height=50)})
    l = layout([[WidgetBox(dropdown),],[WidgetBox(z_slider),], [WidgetBox(k_slider),], [plot,s_color]])
    script, div_dict = components(l)
    print div_dict
    #print div_dict
    return render_template('homepage.html', script=script, div=div_dict)
                           #feature_names=feature_names, current_feature_name=current_feature_name)


#Index page 
@app.route('/lin/')
def lin():
    index = request.args.get('index')
    if index == None:
        index = '0'
    # Create the plot
    plot = create_lin(index)
    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    #print (script)
    #print(div)

    return render_template("lin.html", script=script, div=div)

@app.route('/nl/')
def nl():
    index = request.args.get('index')
    if index == None:
        index = '0'
    # Create the plot
    plot = create_nl(index)
    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    #print (script)
    #print(div)

    return render_template("nl.html", script=script, div=div)
@app.route('/lin_pre/')
def lin_pre():
    index = request.args.get('index')
    if index == None:
        index = '0'
    # Create the plot
    plot = create_lin_pre(index)
    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    #print (script)
    #print(div)

    return render_template("lin_pre.html", script=script, div=div)
@app.route('/nl_pre/')
def nl_pre():
    index = request.args.get('index')
    if index == None:
        index = '0'
    # Create the plot
    plot = create_nl_pre(index)
    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    #print (script)
    #print(div)

    return render_template("nl_pre.html", script=script, div=div)

#With debug=True, Flask Render will auto-reload when there are code changes
if __name__ == '__main__':
    #set debug to False in a production environment
    app.run(port=5000, debug=True)







