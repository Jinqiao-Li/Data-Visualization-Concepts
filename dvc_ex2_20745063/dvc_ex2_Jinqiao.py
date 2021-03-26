#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
from math import pi
import numpy as np
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,FactorRange
import bokeh.palettes as bp
 
# Goal: Draw a line chart displaying averaged daily new cases for all cantons in Switzerland.
# Dataset: covid19_cases_switzerland_openzh-phase2.csv
# Interpretation: value on row i, column j is either the cumulative covid-19 case number of canton j on date i or null value

### Task 1: Data Preprocessing
## T1.1 Read data into a dataframe, set column "Date" to be the index 

url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/covid19_cases_switzerland_openzh-phase2.csv?raw=true'
raw = pd.read_csv(url,usecols=range(0,28))

# Initialize the first row with zeros, and remove the last column 'CH' from dataframe
raw.iloc[0,1:] = 0
raw.drop('CH',axis=1,inplace=True)

# Fill null with the value of previous date from same canton
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html
raw = raw.fillna(method='ffill')

#raw


# In[2]:


## T1.2 Calculate and smooth daily case changes

# Compute daily new cases (dnc) for each canton, e.g. new case on Tuesday = case on Tuesday - case on Monday;
# Fill null with zeros as well

dnc = raw.copy()
#dnc.reshape(raw.shape)
#print(dnc)
for i in range(1,raw.shape[0]):
    for j in range(1,raw.shape[1]):
        dnc.iloc[i,j]=raw.iloc[i,j]-raw.iloc[i-1,j]
#dnc.fillna(0)
#print(dnc['AI'])

# Smooth daily new case by the average value in a rolling window, and the window size is defined by step
# Why do we need smoothing? How does the window size affect the result?
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rolling.html
step = 3
dnc_avg = dnc.copy()
dnc_avg.iloc[:,1:] =dnc.iloc[:,1:].rolling(step, min_periods=1).mean()

#dnc_avg


# In[3]:


## T1.3 Build a ColumnDataSource 

# Extract all canton names and dates
# NOTE: be careful with the format of date when it is used as x input for a plot
cantons = dnc_avg.columns.values[1:].tolist()
#print(cantons)
date = pd.to_datetime(dnc_avg['Date'])
#print(date)

# Create a color list to represent different cantons in the plot, you can either construct your own color patette or use the Bokeh color pallete
import itertools

color_palette = itertools.cycle(bp.Spectral8)
#color_palette = bp.Spectral11
#print(color_palette)

# Build a dictionary with date and each canton name as a key, i.e., {'date':[], 'AG':[], ..., 'ZH':[]}
# For each canton, the value is a list containing the averaged daily new cases 
source_dict = {col:dnc_avg[col].tolist() for col in cantons}
source_dict.update({"date": date}) 
#print(source_dict)
source = ColumnDataSource(data=source_dict)


# In[4]:


### Task 2: Data Visualization

## T2.1: Draw a group of lines, each line represents a canton, using date, dnc_avg as x,y. Add proper legend.
# https://docs.bokeh.org/en/latest/docs/reference/models/glyphs/line.html?highlight=line#bokeh.models.glyphs.Line
# https://docs.bokeh.org/en/latest/docs/user_guide/interaction/legends.html

p = figure(plot_width=1000, plot_height=800, x_axis_type="datetime")
p.title.text = 'Daily New Cases in Switzerland'

lines = []
for canton,color in zip(cantons,color_palette): 
    renderer = p.line(x='date',y=canton,legend_label=canton,
                      source=source,color=color)
    
    hover = (HoverTool(
            tooltips=[( 'date', '@date{%F}'),
                      ( 'canton', canton), 
                      ( 'cases', '@'+canton )],
            formatters={'@date': 'datetime'},
            renderers = [renderer]))
    
    p.add_tools(hover)
                
#p.add_tools(hover)
# Make the legend of the plot clickable, and set the click_policy to be "hide"
p.legend.location = "top_left"
p.legend.click_policy="hide"


# In[5]:


## T2.2 Add hovering tooltips to display date, canton and averaged daily new case

# (Hovertip doc) https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#hovertool
# (Date hover)https://stackoverflow.com/questions/41380824/python-bokeh-hover-date-time

    
show(p)
output_file("dvc_ex2.html")
save(p)

