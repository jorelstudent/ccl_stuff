from flask import Flask, render_template, request
import pandas as pd
from bokeh.embed import components

from bokeh.layouts import column, widgetbox, WidgetBox, layout
from bokeh.models import CustomJS, Button, HoverTool, ColumnDataSource, LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar, OpenURL, TapTool#For the button and a hovertool
from bokeh.models.widgets import Slider, Dropdown, Select #For the sliders and dropdown
from bokeh.plotting import figure, curdoc, show
from bokeh.io import gridplot, output_file, show #allows you to make gridplots
from bokeh.charts import HeatMap, bins, output_file, show #Allows you to craete heatmaps

import numpy as np
import pdb
from random import random

app = Flask(__name__)
#creates hover tool
indices = range(100)
def create_lin(index):
    # load the data
    i = int(index)

    fname = "/Users/penafiel/JPL/git/ccl_stuff/for_daniel/CCL/lhs/lin/non_pre/lhs_mpk_lin_%05dz1_pk.dat" % (i)
    #ccl_data = pd.read_table(fname,
        #names=["k", "pk_lin"], skiprows = 1, delim_whitespace = True)
    cclData = np.loadtxt(fname, skiprows = 1)
    cclK = cclData[:, 0]
    cclPk = cclData[:, 1]
    data = np.loadtxt('/Users/penafiel/JPL/git/ccl_stuff/for_daniel/text_files/par_stan.txt', skiprows = 1)


    fname = "/Users/penafiel/JPL/git/ccl_stuff/for_daniel/class/lhs/lin/non_pre/lhs_lin_%05dz1_pk.dat" % (i)
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
    p.circle(cclK, cclPk, size = 10, legend = "ccl data", fill_color = "white")

    #p.circle(classData['k'].values, classData['P'].values, size = 5, color = "red", legend = "class data")
    p.line(classKLin, classPLin, line_width = 2)
    p.circle(classKLin, classPLin, size = 5, color = "red", legend = "class data", fill_color = "white")

    # Set the x axis label
    # Set the y axis label
    p.yaxis.axis_label = 'Count (log)'
    comparisonValue = abs(cclPk - classPLin)
    comparisonValue = abs(cclPk - classPLin) / classPLin
    p2.line(classKLin, comparisonValue, line_width = 2)
    p2.circle(classKLin, abs(cclPk - classPLin) / classPLin, size = 5, fill_color = "white")
    plot = gridplot([[p],[p2]])
    return plot

def create_nl(index):
    # load the data
    i = int(index)

    fname ="Users/penafiel/JPL/git/ccl_stuff/for_daniel/class/lhs/nl/non_pre/lhs_nl_%05dz1_pk.dat" % (i)
    #ccl_data = pd.read_table(fname,
        #names=["k", "pk_lin"], skiprows = 1, delim_whitespace = True)
    cclData = np.loadtxt(fname, skiprows = 1)
    cclK = cclData[:, 0]
    cclPk = cclData[:, 1]
    data = np.loadtxt('/Users/penafiel/JPL/git/ccl_stuff/for_daniel/text_files/par_stan.txt', skiprows = 1)



    fname = '/Users/penafiel/JPL/git/ccl_stuff/for_daniel/class/lhs/nl/non_pre/lhs_nonlin_%05dz1_pk.dat' % (i)
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
    p.circle(cclK, cclPk, size = 10, legend = "ccl data", fill_color = "white")

    #p.circle(classData['k'].values, classData['P'].values, size = 5, color = "red", legend = "class data")
    p.line(classKLin, classPLin, line_width = 2)
    p.circle(classKLin, classPLin, size = 5, color = "red", legend = "class data", fill_color = "white")

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

    fname = "/Users/penafiel/JPL/git/ccl_stuff/for_daniel/CCL/lhs/lin/pre/lhs_mpk_lin_pk_%05dz1_pk.dat" % (i)
    #ccl_data = pd.read_table(fname,
        #names=["k", "pk_lin"], skiprows = 1, delim_whitespace = True)
    cclData = np.loadtxt(fname, skiprows = 1)
    cclK = cclData[:, 0]
    cclPk = cclData[:, 1]
    data = np.loadtxt('/Users/penafiel/JPL/git/ccl_stuff/for_daniel/text_files/par_stan.txt', skiprows = 1)



    fname ="/Users/penafiel/JPL/git/ccl_stuff/for_daniel/class/lhs/lin/pre/lhs_lin_pk_%05dz1_pk.dat" % (i)
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
    p.circle(cclK, cclPk, size = 10, legend = "ccl data", fill_color = "white")

    #p.circle(classData['k'].values, classData['P'].values, size = 5, color = "red", legend = "class data")
    p.line(classKLin, classPLin, line_width = 2)
    p.circle(classKLin, classPLin, size = 5, color = "red", legend = "class data", fill_color = "white")

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

    fname = "/Users/penafiel/JPL/git/ccl_stuff/for_daniel/CCL/lhs/nl/pre/lhs_mpk_nl_pk_%05dz1_pk.dat" % (i)
    #ccl_data = pd.read_table(fname,
        #names=["k", "pk_lin"], skiprows = 1, delim_whitespace = True)
    cclData = np.loadtxt(fname, skiprows = 1)
    cclK = cclData[:, 0]
    cclPk = cclData[:, 1]
    data = np.loadtxt('/Users/penafiel/JPL/git/ccl_stuff/for_daniel/text_files/par_stan.txt', skiprows = 1)


    fname = '/Users/penafiel/JPL/git/ccl_stuff/for_daniel/class/lhs/nl/pre/lhs_nonlin_pk_%05dz1_pk.dat' % (i)

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
    p.circle(cclK, cclPk, size = 10, legend = "ccl data", fill_color = "white")

    #p.circle(classData['k'].values, classData['P'].values, size = 5, color = "red", legend = "class data")
    p.line(classKLin, classPLin, line_width = 2)
    p.circle(classKLin, classPLin, size = 5, color = "red", legend = "class data", fill_color = "white")

    # Set the x axis label
    # Set the y axis label
    p.yaxis.axis_label = 'Count (log)'
    comparisonValue = abs(cclPk - classPLin) / classPLin
    p2.line(classKLin, comparisonValue, line_width = 2)
    p2.circle(classKLin, abs(cclPk - classPLin) / classPLin, size = 5, fill_color = "white")
    plot = gridplot([[p],[p2]])
    return plot

#LETS IMPLEMENT A CLICK
@app.route('/')
def home():
    #load the data
    data = np.loadtxt('/Users/penafiel/JPL/git/ccl_stuff/for_daniel/text_files/par_stan.txt', skiprows = 1)
    tot_tot = np.loadtxt('/Users/penafiel/JPL/git/ccl_stuff/for_daniel/text_files/tot_tot.txt')

    #Load the parameter values and total failures, since it will be easier to load
    trial_arr = data[:,0]
    h_arr = data[:,1]
    Omega_b_arr = data[:,2]
    Omega_cdm_arr = data[:,3]
    A_s_arr = data[:,4]
    n_s_arr = data[:,5]
    #Gets the extension depending on which mode you choose
    tot_tot_lin = tot_tot[:,0]
    tot_tot_nl = tot_tot[:,1]
    tot_tot_lin_pre = tot_tot[:,2]
    tot_tot_nl_pre = tot_tot[:,3]
    #Creates a dictionary since that's what ColumnDataSource takes in
    data_lin = {'tot_tot_data':tot_tot_lin}
    data_nl = {'tot_tot_data':tot_tot_nl}
    data_lin_pre = {'tot_tot_data':tot_tot_lin_pre}
    data_nl_pre = {'tot_tot_data':tot_tot_nl_pre}

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
    s1.rect('h_arr', 'Omega_b_arr',width=0.05, height=0.0034, alpha=0.8, source=source_data,fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s1.yaxis.axis_label = '$\Omega_b$'
    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size='5pt',
                    ticker=BasicTicker(desired_num_ticks=len(colors)),
                    label_standoff=6, border_line_color=None, location=(0,0))
    s1.add_layout(color_bar, 'right')

    s2 = figure(plot_width=300, plot_height=300, tools=[hover2, TapTool()])
    s2.grid.grid_line_color=None
    s2.rect('h_arr', 'Omega_cdm_arr', width=0.05, height=0.035, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s2.yaxis.axis_label = '$\Omega_{cdm}$' 

    s3 = figure(plot_width=300, plot_height=300, tools=[hover3, TapTool()])
    s3.grid.grid_line_color = None
    #Plots the rectangles
    s3.rect('Omega_b_arr', 'Omega_cdm_arr',width=0.0034, height=0.035, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    
    s4 = figure(plot_width=300, plot_height=300, tools=[hover4, TapTool()])
    s4.grid.grid_line_color = None
    #Plots the rectangles
    s4.rect('h_arr', 'A_s_arr',width=0.05, height=0.09e-9, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s4.yaxis.axis_label = '$\A_s$' 

    s5 = figure(plot_width=300, plot_height=300, tools=[hover5, TapTool()])
    s5.grid.grid_line_color = None
    s5.rect('Omega_b_arr', 'A_s_arr',width=0.0034, height=0.09e-9, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)

    s6 = figure(plot_width=300, plot_height=300, tools=[hover6, TapTool()])
    s6.grid.grid_line_color = None
    s6.rect('Omega_cdm_arr', 'A_s_arr',width=0.035, height=0.09e-9, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)

    s7 = figure(plot_width=300, plot_height=300, tools=[hover7, TapTool()])
    s7.grid.grid_line_color = None
    s7.rect('h_arr', 'n_s_arr',width=0.05, height=0.0068, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s7.yaxis.axis_label = '$n_s$'
    s7.xaxis.axis_label = '$h$'
   
    s8 = figure(plot_width=300, plot_height=300, tools=[hover8,TapTool()])
    s8.grid.grid_line_color = None
    s8.rect('Omega_b_arr', 'n_s_arr', width=0.0034, height=0.0068, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s8.xaxis.axis_label = '$\Omega_b$'

    s9 = figure(plot_width=300, plot_height=300, tools=[hover9, TapTool()])
    s9.grid.grid_line_color = None
    s9.rect('Omega_cdm_arr', 'n_s_arr', width=0.035, height=0.0068, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s9.xaxis.axis_label = '$\Omega_{cdm}$'

    s10 = figure(plot_width=300, plot_height=300,tools=[hover10, TapTool()])
    s10.grid.grid_line_color = None
    s10.rect('A_s_arr', 'n_s_arr', width=0.09e-9, height=0.0068, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s10.xaxis.axis_label = '$A_s$'

        
    #Creates the gridplot to be reminscient of a corner plot
    plot = gridplot([[s1, None, None, None], [s2, s3, None, None], [s4,s5,s6, None], [s7,s8,s9,s10]])

    #Creates the selection menu for the select
    selection_men = ['Linear', 'Non-Linear', 'Linear, Precision', 'Non-Linear, Precision']
    dropdown = Select(title='Mode', value=selection_men[0], options=selection_men)
    #Callback file
    #This takes ihe value from the source file and changes it according to the value of the dropdown
    code_dropdown = """
    var f = cb_obj.value;
    var tot_data = source_data.data;
    var tot_lin = js_lin.data;
    var tot_nl = js_nl.data;
    var tot_lin_pre = js_lin_pre.data;
    var tot_nl_pre = js_nl_pre.data;
    console.log(f);
    console.log(tot_data);
    for (key in tot_data) {console.log(tot_data[key]);}
    if (f == "Linear") {
    delete tot_data['tot_tot_data'];
    tot_data['tot_tot_data'] = tot_lin['tot_tot_data'];
    }

    if (f == "Non-Linear") {
    delete tot_data['tot_tot_data'];
    tot_data['tot_tot_data'] = tot_nl['tot_tot_data'];
    }

    if (f == "Linear, Precision"){
    delete tot_data['tot_tot_data'];
    tot_data['tot_tot_data'] = tot_lin_pre['tot_tot_data'];
    }

    if (f == "Non-Linear, Precision"){
    delete tot_data['tot_tot_data'];
    tot_data['tot_tot_data'] = tot_nl_pre['tot_tot_data'];
    }
    console.log(tot_data);
    console.log(tot_data['tot_tot_data']);
    source_data.trigger('change');
    """

    #This will cause the change to occur
    callback = CustomJS(args=dict(source_data=source_data,js_lin=source_lin,js_nl=source_nl,js_lin_pre=source_lin_pre, js_nl_pre=source_nl_pre), code=code_dropdown)
    dropdown.js_on_change('value', callback) #Adds the callback onto our plot
    
    #Make it open a URL on tap, but it needs to be for the proper mode
    #Use dropdown.value
    mode = dropdown.value
    if mode == 'Linear':
        url = 'http://127.0.0.1:5000/lin/?index=@trial_arr'
    
    elif mode == 'Non-Linear':
        url = 'http://127.0.0.1:5000/nl/?index=@trial_arr'

    elif mode == 'Linear, Precision':
        url = 'http://127.0.0.1:5000/lin_pre/?index=@trial_arr'

    elif mode == 'Non-Linear, Precision':
        url = 'http://127.0.0.1:5000/nl_pre/?index=@trial_arr'
    else:
        url = 'http://127.0.0.1:5000/lin/?index=@trial_arr'


    #Make it open a new URL on tap
    #Bokeh is again a bitch, so we gotta initiate multiple instances
    taptool = s1.select(type=TapTool)
    taptool.callback=OpenURL(url=url)

    taptool = s2.select(type=TapTool)
    taptool.callback=OpenURL(url=url)

    taptool = s3.select(type=TapTool)
    taptool.callback=OpenURL(url=url)

    taptool = s4.select(type=TapTool)
    taptool.callback=OpenURL(url=url)

    taptool = s5.select(type=TapTool)
    taptool.callback=OpenURL(url=url)

    taptool = s6.select(type=TapTool)
    taptool.callback=OpenURL(url=url)

    taptool = s7.select(type=TapTool)
    taptool.callback=OpenURL(url=url)

    taptool = s8.select(type=TapTool)
    taptool.callback=OpenURL(url=url)

    taptool = s9.select(type=TapTool)
    taptool.callback=OpenURL(url=url)

    taptool = s10.select(type=TapTool)
    taptool.callback=OpenURL(url=url)

    

    #plot = create_corner(comp_ll, source_data.data['tot_tot_data'])
    #script, div_dict = components(plot)#components({'plot':plot, 'dropdown':dropdown})
    #script, div_dict = components({'plot':plot, 'dropdown':HBox(dropdown, height=50)})
    l = layout([[WidgetBox(dropdown),], [plot,]])
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






