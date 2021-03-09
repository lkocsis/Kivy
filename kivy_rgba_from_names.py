# https://www.w3schools.com/colors/colors_names.asp
# https://material.io/resources/color/#!/?view.left=0&view.right=0
#$ CWD
import os, sys, subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PyFilePath  = os.path.dirname(os.path.abspath(__file__))
PyPrgName   = os.path.basename(__file__).split('.')[0]
import webcolors
colors = ['aqua', 'black', 'blue', 'fuchsia', 'gray', 'grey', 'green', 'lime', 
            'maroon', 'navy', 'olive', 'purple', 'red', 'silver', 'teal','white','yellow']
colorsDict= {}
for cname in colors:
    r,g,b=webcolors.name_to_rgb_percent(cname)
    colorsDict[cname]=(r,g,b)

for k in colorsDict:
    print(f'{k}:{colorsDict[k]}')

import pandas as pd
htl = pd.read_html('https://www.w3schools.com/colors/colors_groups.asp')
print (type(htl))
print (len(htl))
df = htl[0]
df = df.iloc[:, : 1]
df.columns = ['ColorName']
ColorRanges = ['Pink Colors', 'Purple Colors', 'Red Colors', 'Orange Colors', 'Yellow Colors', 
                'Green Colors', 'Cyan Colors', 'Blue Colors', 'Brown Colors', 'White Colors', 'Grey Colors']

print(df.head())
print(df.index)
print(df.columns)
print(df.tail())

df = df.loc[~df.ColorName.isin(['Color Name','RebeccaPurple']+ColorRanges)]
print(df.head())
print(df.tail())

from pyIniLib import pandasExcel
xlsx = pandasExcel('./data/w3schools_colors.xlsx')
for cname in df.ColorName:
    r,g,b=webcolors.name_to_rgb_percent(cname)
    colorsDict[cname]=(r,g,b)
    print(f'{cname}:{colorsDict[cname]}')
    for col in ['R','G','B']:
        df.loc[df.ColorName== cname , col] = r.strip('%')
for col in ['R','G','B']:
        df[col]=df[col].astype(float) # df.B=pd.to_numeric(df.B)
        df[col]=df[col]/100
df['A'] = 1
# df.apply(pd.to_numeric, errors='ignore')
xlsx.sheet(df,'w3cnrgb')
xlsx.save()