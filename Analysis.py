#!/usr/bin/env python
# coding: utf-8

# ### TASK1: Import panda libary
# 

# In[106]:


import pandas as pd
import os
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter


# ### Task2: Collate monthly sales
# 

# In[10]:


files=[file for file in os.listdir('./Sales_Data')]
allMonthsData= pd.DataFrame()

for file in files:
    df = pd.read_csv("./Sales_Data/"+ file)
    allMonthsData=pd.concat([allMonthsData,df])
allMonthsData.to_csv("collated_data.csv", index=False)    
    


# In[12]:


collated_data=pd.read_csv("collated_data.csv")
collated_data.head()


# ### Task3: Cleaning the data

# #### Drop NAN rows and Remove Or

# In[61]:


nan_df=collated_data[collated_data.isna().any(axis=1)]
nan_df.head()

collated_data=collated_data.dropna(how='all')
collated_data.head(5)

collated_data=collated_data[collated_data['Order Date'].str[0:2]!='Or']
collated_data.head(20)


# ### Add Months column
# 
# 

# In[39]:


collated_data['Month']=collated_data['Order Date'].str[0:2]

collated_data['Month']=collated_data['Month'].astype('int32')
#collated_data['Month']=pd.to_numeric(collated_data['Order Date'])#converted to int


# # To find the Best sales month and amount
# 

# In[69]:


collated_data['Quantity Ordered']=pd.to_numeric(collated_data['Quantity Ordered'])#make as int
collated_data['Price Each']=pd.to_numeric(collated_data['Price Each'])#make as float

collated_data['Sales']=collated_data['Quantity Ordered']*collated_data['Price Each']#sales per day in a month
#collated_data.head(25)
results=collated_data.groupby('Month').sum()
results


# ### Plot montly sales using plotlib

# In[62]:


months=range(1,13)
plt.bar(months,results['Sales'])

plt.xticks(months)
plt.ylabel('Sales in $')
plt.xlabel('Month in number')
plt.show()


# # To find the city with the maximum sales

# ### Add City column and state to remove duplicacy

# In[66]:


def get_city(address):
    return address.split(',')[1]
def get_state(address):
    return address.split(',')[2].split(' ')[1]


collated_data['City']=collated_data['Purchase Address'].apply(lambda x:f"{get_city(x)},({get_state(x)})")
collated_data.head(20)


# #### To find city with highest number of sales and plot

# In[76]:


results=collated_data.groupby('City').sum()
results
#plotting the graph

cities=[city for city, df in collated_data.groupby('City')]

plt.bar(cities,results['Sales'])
plt.xticks(cities, rotation='vertical', size=10)
plt.ylabel('Sales in $')
plt.xlabel('City Name')
plt.show()


# ### Best time of the day to advertise
# 

# #### Seperating the hour of the day from the order time and date and putting a count

# In[81]:


collated_data['Order Date']=pd.to_datetime(collated_data['Order Date'])
collated_data['Hour']=collated_data['Order Date'].dt.hour
collated_data['CountHour']=1
collated_data.head()


# #### Plotting a graph to find the peak hours

# In[91]:


#Plotting graph to find the best time of the day for advertisement

hours=[hour for hour, df in collated_data.groupby('Hour')]

plt.plot(hours, collated_data.groupby(['Hour']).count())
plt.grid()
plt.xticks(hours)
plt.ylabel('Count of Order')
plt.xlabel('Hour of the Day')
plt.show()

#Peak at 11am and 7pm


# # To find the products sold together most often

# In[103]:


#find the duplicate order Id to know which orders were made together

df=collated_data[collated_data['Order ID'].duplicated(keep=False)]
#df.head(50)
df['Grouped']=df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))

df=df[['Order ID','Grouped']].drop_duplicates()
df.head(20)


# In[107]:


#counting the total number of products ordered together

count=Counter()

for row in df['Grouped']:
    row_list=row.split(',')
    count.update(Counter(combinations(row_list,2)))
    
for key, value in count.most_common(10):
    print(key, value)


# # What product sold the most and why?

# In[121]:


product_group=collated_data.groupby('Product')
quantity_ordered=product_group.sum()['Quantity Ordered']


#plotting the graph
products=[product for product, df in product_group]
plt.bar(products, quantity_ordered)
plt.xticks(products, rotation='vertical', size=10)
plt.ylabel('Quantity Ordered')
plt.xlabel('Products')
plt.show()


# # Overlaying the graphs to get better insights

# In[123]:


#mean of prices of each product sold

prices=collated_data.groupby('Product').mean()['Price Each']
print (prices)


# In[138]:


#graph to plot pricevs product vs quantity ordered

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color='g')
ax2.plot(products,prices,)

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price($)', color='b')
ax1.set_xticklabels(products,rotation='vertical',size=10)
plt.show()






