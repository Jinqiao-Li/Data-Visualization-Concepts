#!/usr/bin/env python
# coding: utf-8

# In[54]:


import pandas as pd 
import numpy as np
import bokeh.palettes as bp
from bokeh.plotting import figure
from bokeh.io import output_file, show, save
from bokeh.models import ColumnDataSource, HoverTool, ColorBar, RangeTool
from bokeh.transform import linear_cmap
from bokeh.layouts import gridplot


# ==========================================================================
# Goal: Visualize Covid-19 Tests statistics in Switzerland with linked plots
# Dataset: covid19_tests_switzerland_bag.csv
# Data Interpretation: 
# 		n_negative: number of negative cases in tests
# 		n_positive: number of positive cases in tests
# 		n_tests: number of total tests
# 		frac_negative: fraction of POSITIVE cases in tests
# ==========================================================================



### Task1: Data Preprocessing


## T1.1 Read the data to the dataframe "raw"
# You can read the latest data from the url, or use the data provided in the folder (update Nov.3, 2020)

url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/covid19_tests_switzerland_bag.csv?raw=true'
raw =  pd.read_csv(url)
#raw


# In[55]:


## T1.2 Create a ColumnDataSource containing: date, positive number, positive rate, total tests
# All the data can be extracted from the raw dataframe.

date = pd.to_datetime(raw["date"],format='%Y-%m-%d')
#print(date)
pos_num = raw["n_positive"].tolist()
pos_rate = raw["frac_negative"].tolist()     #positive rate
test_num = raw["n_tests"].tolist()

source = ColumnDataSource(data=dict(
    date = date,
    positive_number = pos_num,
    positive_rate = pos_rate,
    total_tests = test_num,
))
#print(date)


# In[56]:


## T1.3 Map the range of positive rate to a colormap using module "linear_cmap"
# "low" should be the minimum value of positive rates, and "high" should be the maximum value

mapper = linear_cmap(field_name='positive_rate', palette=bp.Spectral6,low=min(pos_rate) ,high=max(pos_rate))




# In[57]:



### Task2: Data Visualization
# Reference link:
# (range tool example) https://docs.bokeh.org/en/latest/docs/gallery/range_tool.html?highlight=rangetool


## T2.1 Covid-19 Total Tests Scatter Plot
# x axis is the time, and y axis is the total test number. 
# Set the initial x_range to be the first 30 days.

TOOLS = "box_select,lasso_select,wheel_zoom,pan,reset,help"
p = figure(plot_width=800, plot_height=300, x_axis_type="datetime",x_range=(date[0], date[30]))
p.scatter(x="date",y="total_tests",source=source,color=mapper,size=10)

p.title.text = 'Covid-19 Tests in Switzerland'
p.yaxis.axis_label = "Total Tests"
p.xaxis.axis_label = "Date"
p.sizing_mode = "stretch_both"

# Add a hovertool to display date, total test number
hover = (HoverTool(
            tooltips=[( 'date', '@date{%F}'),
                      ( 'total test number', '@total_tests')],
             formatters={'@date': 'datetime'}
        ))
p.add_tools(hover)



# In[58]:


## T2.2 Add a colorbar to the above scatter plot, and encode positve rate values with colors; please use the color mapper defined in T1.3 

#color_bar = ColorBar(...)
color_bar = ColorBar(color_mapper=mapper['transform'], width=8,  location=(0,0),title="Points")
p.add_layout(color_bar, 'right')
#show(p)


# In[59]:


## T2.3 Covid-19 Positive Number Plot using RangeTool
# In this range plot, x axis is the time, and y axis is the positive test number.

#select = figure(...)
select = figure(title="Drag the middle and edges of the selection box to change the range above",
                plot_height=250, plot_width=800, x_axis_type="datetime", 
                tools="", toolbar_location=None)

# Define a RangeTool to link with x_range in the scatter plot
#range_tool = RangeTool(...)
range_tool = RangeTool(x_range=p.x_range)


# Draw a line plot and add the RangeTool to the plot
#select ...
select.line(x='date',y='positive_number', source=source)
select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool

select.yaxis.axis_label = "Positive Cases"
select.xaxis.axis_label = "Date"


# Add a hovertool to the range plot and display date, positive test number
#hover2 = HoverTool(...)
hover2 = (HoverTool(
            tooltips=[( 'date', '@date{%F}'),
                      ( 'positive test number', '@positive_number')],
             formatters={'@date': 'datetime'}
        ))
select.add_tools(hover2)


# In[60]:



#T3 Represent positive rate values by the point sizes.

from bokeh.models import LinearInterpolator

size_mapper=LinearInterpolator(
    x=[min(pos_rate), max(pos_rate)],
    y=[5,50]
)

p2 = figure(plot_width=800, plot_height=300, x_axis_type="datetime",x_range=(date[0], date[30]))
p2.scatter(x="date",y="total_tests",source=source,fill_alpha=0.6, fill_color="red",
          size={'field':'positive_rate','transform': size_mapper})
p2.add_tools(hover)


p2.title.text = 'Covid-19 Tests in Switzerland'
p2.yaxis.axis_label = "Total Tests"
p2.xaxis.axis_label = "Date"
p2.sizing_mode = "stretch_both"


select2 = figure(title="Drag the middle and edges of the selection box to change the range above",
                plot_height=250, plot_width=800, x_axis_type="datetime", 
                tools="", toolbar_location=None)

# Define a RangeTool to link with x_range in the scatter plot
#range_tool = RangeTool(...)
range_tool2 = RangeTool(x_range=p2.x_range)


# Draw a line plot and add the RangeTool to the plot
#select ...
select2.line(x='date',y='positive_number', source=source)
select2.ygrid.grid_line_color = None
select2.add_tools(range_tool2)
select2.toolbar.active_multi = range_tool2

select2.yaxis.axis_label = "Positive Cases"
select2.xaxis.axis_label = "Date"
select.add_tools(hover2)


# In[61]:




## T2.4 Layout arrangement and display
linked_p = gridplot([p, select],ncols=1, plot_width=1000, plot_height=300)#Task2 color
linked_p2 = gridplot([p2, select2],ncols=1, plot_width=1000, plot_height=300)#Task3 size
show(linked_p)
save(linked_p)

output_file("dvc_ex3.html")

#show(linked_p2)
#save(linked_p2)

