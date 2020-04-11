# libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
 
# Data

# raw_data = {'greenBars': [20, 1.5, 7, 10, 5], 'orangeBars': [5, 15, 5, 10, 15],'blueBars': [2, 15, 18, 5, 10]}
# df = pd.DataFrame(raw_data)
df = pd.read_csv('log.csv')
print(df.head())
y_max = df['pixels'].max()
df = df[['ts','low','med','high']]
df.columns = ['ts','greenBars','orangeBars','blueBars']
# r = [0,1,2,3,4]
r = list(range(df.shape[0]))
# From raw value to percentage
totals = [i+j+k for i,j,k in zip(df['greenBars'], df['orangeBars'], df['blueBars'])]
totals = [max(totals)]*len(totals)
greenBars = [i / j * 100 for i,j in zip(df['greenBars'], totals)]
orangeBars = [i / j * 100 for i,j in zip(df['orangeBars'], totals)]
blueBars = [i / j * 100 for i,j in zip(df['blueBars'], totals)]
 
# plot
barWidth = 0.85
names = ('A','B','C','D','E')
names = tuple(df['ts'].values.tolist())
# Create green Bars
plt.bar(r, greenBars, color='#b5ffb9', edgecolor='white', width=barWidth, label="mild")
# Create orange Bars
plt.bar(r, orangeBars, bottom=greenBars, color='#f9bc86', edgecolor='white', width=barWidth, label="medium")
# Create blue Bars
plt.bar(r, blueBars, bottom=[i+j for i,j in zip(greenBars, orangeBars)], color='red', edgecolor='white', width=barWidth, label="high")
 
# Custom x axis
plt.xticks(r, names,rotation='vertical')
plt.xlabel("Birubari, Guwahati")

# Set limit on y-axis 
# plt.ylim(0,y_max)

# Add a legend
plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
 
# Show graphic
plt.show()