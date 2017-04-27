
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.2** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 2 - Pandas Introduction
# All questions are weighted the same in this assignment.
# ## Part 1
# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. 
# 
# The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.

# In[86]:

import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')


# ### Question 0 (Example)
# 
# What is the first country in df?
# 
# *This function should return a Series.*

# In[87]:

# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs


# ### Question 1
# Which country has won the most gold medals in summer games?
# 
# *This function should return a single string value.*

# In[88]:

def answer_one():
    return df.index[df['Gold'] == df['Gold'].max()][0]


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
# 
# *This function should return a single string value.*

# In[89]:

def answer_two():
    s = pd.Series(df['Gold'] - df['Gold.1'])
    s.sort(ascending=False)
    return s.index[0]


# ### Question 3
# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count? 
# 
# $$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$
# 
# Only include countries that have won at least 1 gold in both summer and winter.
# 
# *This function should return a single string value.*

# In[90]:

def answer_three():
    df_ = df[(df["Gold"] > 0) & (df['Gold.1'] > 0)]
    
    summer_gold = df_['Gold']
    winter_gold = df_['Gold.1']
    total_gold  = df_['Gold.2'] + summer_gold + winter_gold
    
    s = pd.Series((summer_gold.astype(float) - winter_gold.astype(float))/total_gold.astype(float))
    s.sort(ascending=False)
    
    return s.index[0]


# ### Question 4
# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created.
# 
# *This function should return a Series named `Points` of length 146*

# In[91]:

def answer_four():
    
    Points = pd.Series(df['Gold.2']  * 3 + 
                       df['Silver.2']* 2 + 
                       df['Bronze.2'])
    return Points


# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov/popest/data/counties/totals/2015/CO-EST2015-alldata.html). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](http://www.census.gov/popest/data/counties/totals/2015/files/CO-EST2015-alldata.pdf) for a description of the variable names.
# 
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
# 
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
# 
# *This function should return a single string value.*

# In[92]:

census_df = pd.read_csv('census.csv')


# In[93]:

def answer_five():
    STATE = 40
    COUNTY = 50
    COUNTY_SUBDIVISION = 60
    TRACT = 140
    BLOCK_GROUP = 150
    PLACE = 160
    
    """ Need to count all counties for each state and get the max???? """
    states = census_df.loc[census_df["SUMLEV"] == STATE,'STNAME'] # this will only get me all the states
    count = {}
    for state in states.values:
        count[state] = len(census_df.loc[(state == census_df['STNAME']) & 
                          (census_df['SUMLEV'] == COUNTY)])
    
    s = pd.Series(count)
    s.sort(ascending=False)
    return s.index[0] 


# ### Question 6
# Only looking at the three most populous counties for each state, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.
# 
# *This function should return a list of string values.*

# In[94]:

def answer_six():
    STATE              = 40
    COUNTY             = 50
    COUNTY_SUBDIVISION = 60
    TRACT              = 140
    BLOCK_GROUP        = 150
    PLACE              = 160
    
    df = census_df[census_df['SUMLEV'] == COUNTY].sort(['STNAME','CENSUS2010POP'],
                                                        ascending=False,
                                                        inplace=False)
    # Get the population of the top three counties for each state
    population = {}
    for state in census_df['STNAME'].unique():
        
        population[state] = df.loc[df['STNAME'] == state,'CENSUS2010POP'].iloc[:3].sum()   
        
    return list(pd.Series(population,index=population.keys()).sort(ascending=False,inplace=False).iloc[:3].index)


# ### Question 7
# Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
# 
# e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
# 
# *This function should return a single string value.*

# In[95]:

def answer_seven():
    STATE              = 40
    COUNTY             = 50
    COUNTY_SUBDIVISION = 60
    TRACT              = 140
    BLOCK_GROUP        = 150
    PLACE              = 160
    df = census_df.loc[census_df['SUMLEV'] == COUNTY,
                      ["POPESTIMATE201" + str(val) for val in range(6)] + 
                      ["CTYNAME","STNAME"]].set_index(['CTYNAME','STNAME'])
    diff = {}
    for county,state in df.index:
        diff[county,state] = df.loc[county,state].max() - df.loc[county,state].min()
    return pd.Series(diff).sort(inplace=False,ascending=False).index[0][0]


# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column. 
# 
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# 
# *This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

# In[96]:

def answer_eight():
    STATE              = 40
    COUNTY             = 50
    COUNTY_SUBDIVISION = 60
    TRACT              = 140
    BLOCK_GROUP        = 150
    PLACE              = 160
    
    df = census_df[((census_df['REGION'] == 1) | 
                   (census_df['REGION'] == 2)) &
                   (census_df['CTYNAME'].str.contains('Washington')) & 
                   (census_df['POPESTIMATE2015'] > census_df['POPESTIMATE2014'])].loc[:,["STNAME",'CTYNAME']]    
    return df


# In[ ]:




# 
