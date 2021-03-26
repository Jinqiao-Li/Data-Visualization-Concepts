#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd 
from math import pi
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,FactorRange,CustomJS
# import bokeh.palettes as bp # uncomment it if you need special colors that are pre-defined

### Task 1: Data Preprocessing
 

## T1.1 Read online .csv file into a dataframe using pandas
# Reference links: 
# https://pandas.pydata.org/pandas-docs/stable/reference/frame.html
# https://stackoverflow.com/questions/55240330/how-to-read-csv-file-from-github-using-pandas 

original_url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/demographics_switzerland_bag.csv?raw=true'
df = pd.read_csv(original_url, index_col=0)
#print(df.head())

## T1.2 Prepare data for a grouped vbar_stack plot
# Reference link, read first before starting: 
# https://docs.bokeh.org/en/latest/docs/user_guide/categorical.html#stacked-and-grouped

# Filter out rows containing 'CH' 
df = df[~df['canton'].isin(["CH"])]
#print(df)

# Extract unique value lists of canton, age_group and sex
canton = df['canton'].drop_duplicates().values
canton_less = canton[5:18]
#print(canton_less) 

age_group = df['age_group'].drop_duplicates().values
#print(age_group) 

sex = df['sex'].drop_duplicates().values
#print(sex)

# Create a list of categories in the form of [(canton1,age_group1), (canton2,age_group2), ...]

factors = []
#print(type(m))
for i in range(len(canton)):
    for j in range(len(age_group)):
        m=(canton[i],age_group[j])
        factors.append(m)
#print(factors)
    
# Use genders as stack names
stacks = ['female','male']

# Calculate total population size as the value for each stack identified by canton,age_group and sex
stack_val = [[],[]]      #[female_val,male_val]
df_male = df[df.sex.isin([sex[0]])]
df_female = df[df.sex.isin([sex[1]])]

for i in range(len(canton)):
    for j in range(len(age_group)):
        #population size as the value for female
        pop_a=0
        aa = df_female[df_female.canton.isin([canton[i]])]
        ab = aa[aa.age_group.isin([age_group[j]])]
        pop_a = (ab['pop_size'].sum())
        stack_val[0].append(pop_a)
        
        #population size as the value for male
        ba = df_male[df_male.canton.isin([canton[i]])]
        bb = ba[ba.age_group.isin([age_group[j]])]
        pop_b=0
        pop_b = (bb['pop_size'].sum())
        stack_val[1].append(pop_b)
               
# Build a ColumnDataSource using above information
source = ColumnDataSource(data=dict(
    x = factors,
    female = stack_val[0],
    male = stack_val[1],
))
#print(stack_val)



# In[6]:


### Task 2: Data Visualization

## T2.1: Visualize the data using bokeh plot functions
p=figure(x_range=FactorRange(*factors), plot_height=500, plot_width=800, 
         title='Canton Population Visualization')
p.yaxis.axis_label = "Population Size"
p.xaxis.axis_label = "Canton"
p.sizing_mode = "stretch_both"
p.xgrid.grid_line_color = None

#p.vbar_stack(...)
p.vbar_stack(stacks, x='x', width=0.9, alpha=0.5, color=["blue", "red"], 
             source=source,legend_label=stacks)

p.y_range.start = 0
p.y_range.end = 200000
p.x_range.range_padding =0.05
p.xaxis.major_label_text_font_size='0.6em'
p.xaxis.major_label_orientation="vertical"
p.legend.location = "top_left"
p.legend.orientation = "vertical"

## T2.2 Add the hovering tooltips to the plot using HoverTool
# To be specific, the hover tooltips should display “gender”, canton, age group”, and “population” when hovering.
# https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#hovertool
# read more if you want to create fancy hover text: https://stackoverflow.com/questions/58716812/conditional-tooltip-bokeh-stacked-chart

TOOLTIPS = [
    ("gender", "$name"),
    ("canton,age_group", "@x"),
    ("population", "@$name"),
]
hover = HoverTool(tooltips=TOOLTIPS)
p.add_tools(hover)
show(p)

## T2.3 Save the plot as "dvc_ex1.html" using output_file
output_file("dvc_ex1.html")


# In[ ]:




