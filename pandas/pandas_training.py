import sys; print('Python %s on %s' % (sys.version, sys.platform))
import pandas as pd
import os
from pandas_profiling import ProfileReport
import dask.dataframe as dd

# set float options in pd
pd.options.display.float_format = '{:,.2f}'.format

# get wd
os.getcwd()

# read data
iris = pd.read_csv('pandas/iris.csv')
planets = pd.read_csv('pandas/planets.csv')

# subsetting data loc and iloc
# loc subset by position or names

cols = iris.columns
iris.loc[0:10, cols]
iris.iloc[1,1:len(iris.columns)]

# change data types float, int, str, datetime

planets['number'] = planets['number'].astype(float)
planets['year_dt'] = planets['year_dt'] - pd.Timedelta['30 d']
planets.isna()planets['year_dt'] = planets['year_dt'] - pd.Timedelta['30 d']
planets.isna()
# working with strings

iris['species'].str.len()
iris['species'].str.lower()
iris['species'].str.len()

# datetime objects

planets['year_dt'].diff(periods=1)
planets['year_dt'] = pd.to_datetime(planets['year'], format='%Y')

# map/apply/applymap

planets.apply(lambda x: 'far' if x['distance'] > 50 else 'short', axis = 1)
group = iris.drop('new names',axis=1).groupby(['species'])
group.apply(lambda x: x.sum())

dict = {'setosa':'first'}
iris['new names'] = iris['species'].map(dict)

# group by
# group by series, select agg method

iris.groupby(['species']).sum('sepal_length')
iris.groupby(['species']).max()

# pivot - pivots table (Can unstack for multiple levels)
# pivot_table applies and aggregation function

# merge - can merge, right join, left join, inner join, using on/how and change suffixes
# drop_duplicates

# can encode dummies using get_dummies

pd.get_dummies(iris['species'])


# basic plotting with pandas

planets.plot();
planets.boxplot()
planets.corr()

# profile report:

profile = ProfileReport(planets,title = 'Planets Report')
profile.to_notebook_iframe()
profile.to_file("iris-profile.html")

# dask dataframes

df = dd.read_csv("pandas/planets.csv")