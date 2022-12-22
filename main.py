#import the library for Data preprocessing-----
import pandas as pd
import numpy as np
from datetime import datetime
import requests
from matplotlib import pyplot as plt

# read dataset 
df1 = pd.read_csv("https://mtalkzplatformstorage.blob.core.windows.net/mtalkz-files-transfer/ig138I5Ecgez1TL.csv",low_memory=False)
print("first five rows of the dataset\n\n",df1.head())
print("\n")
# Drop the unwanted column.
df1.drop(['Unnamed: 15','Unnamed: 16'], inplace = True,axis = 1)
#syntax----------------------------------------------------------------------------------------df1.drop(['C', 'D'], axis=1)
print("shape of the dataset",df1.shape)
# checking the null values in the dataset.
df1.isnull()
print("\n")
# total number of null values present in each column
print("total number of null values present in each column\n\n",df1.isnull().sum())
# filling the null values using fillna function.
df2 = df1.fillna(value={'Provider':'unknown' , 'Click Count':0 , 'Click Status':'NA' , 'Click DateTime':'NA' , 'Browser':'NA' , 'Platform':'not define' , 'IP Address':'not define' ,'Status':'No'})
print("\n")
#After fill the null value check the null value in dataset.
print("After fill the null value total null value in dataset",df2.isnull().sum().sum())
print("\n")
# convert send time and Delivered time into datetime datatype
df2["Send Time"] =  pd.to_datetime(df2["Send Time"], infer_datetime_format=True)
df2["Delivered Time"] =  pd.to_datetime(df2["Delivered Time"], infer_datetime_format=True)

#find the difference between delivered time and send time,and convert in seconds.
df2["Diffrence Time"] = df2["Delivered Time"] - df2["Send Time"]
seconds = df2["Diffrence Time"].astype('timedelta64[s]').astype(np.int32)
df2["Diffrence Secs"] = seconds
print("data types of column present in the dataset\n\n",df2.dtypes)
print("\n")
print("rows and column of the dataset\t",df2.shape)
#print("print the dataset which cointaining diffrence seconds column",df2.head())
print("\n")
# Here we grouped the the df2 
df3 = df2.groupby("Campaign name")
df3

for x,y in df3:
    print(x)
    print(y.head())
    print()
    
    
#accessing individual caimpaign and find the delivered rate
df4 = df3.get_group("APP1")
# df4 dataframe contain records related to APP1 campaign
print("number of rows and column of APP1 caimpaign",df4.shape)
print("\n")
total_sent = df4['Status'].count()
print("total messages sent\t",total_sent)
num_delivered = (df4['Status'] == 'Delivered').sum()
print("\n")
print("total messages delivered in APP1\t",num_delivered)
delivered_rate = (num_delivered / total_sent) * 100
print("\n")
print("delivered rate of APP1\t",delivered_rate)


#accessing  APP2 campaign and find the delivered rate
df5 = df3.get_group("APP2")
# print("shape of dataframe  APP1\t",df5.shape)
print("\n")
total_sent = df5['Status'].count()
print("total messages sent",total_sent)
print("\n")
num_delivered = (df5['Status'] == 'Delivered').sum()
print("total messages delivered in APP2\t",num_delivered)
print("\n")
delivered_rate = (num_delivered / total_sent) * 100
print("delivered rate of APP2\t",delivered_rate)
print("\n")


# now finding the undelivered rate --------
df6 = df3.get_group("APP1")
#print(df6.shape)
total_sent = df4['Status'].count()
#print("total messages sent",total_sent)
num_undelivered = (df4['Status'] == 'No').sum()
print("number of undelivered msges\t",num_undelivered)
print("\n")
undelivered_rate = (num_undelivered / total_sent) * 100
print("undelivered rate of APP1\t",undelivered_rate)
print("\n")

# now calculating the response rate of APP1 --------
df7 = df3.get_group("APP1")
total_sent = df4['Click Status'].count()
#print("total messages sent \n",total_sent)
clicked_msg = (df4['Click Status'] == 'Yes').sum()
print("number of messages clicked\t",clicked_msg)
print("\n")
response_rate = (clicked_msg  / total_sent)*100
print("response rate of APP1\t",response_rate)
print("\n")

#now calculating the failure rate of APP1---
df8 = df3.get_group("APP1")
total_sent = df4['Click Status'].count()
print("total messages sent\t",total_sent)
print("\n")
options = ['No']
# unclicked_msg = df4[(df4['Status'] == 'Delivered') & (df4['Click Status']=='No')].sum()
df9 = df4[(df4['Status'] == 'Delivered') & (df4['Click Status'].isin(options))]
unclicked_msg =df9['Status'].count()
print("number of unclicked messages\t",unclicked_msg)
nonreaction_rate = (unclicked_msg  / total_sent)*100
print("nonreaction_rate  of APP1\t",nonreaction_rate)
print("\n")

# providers in APP1 and their frequency messages in APP1
df9 = df4.groupby('Provider').size().sort_values(ascending=False).reset_index()
df9.rename(columns =  {0:'Frequency'},inplace = True)
print(df9.head())


# Bar chart shows the providers in APP1 and their frequency messages in APP1.
name = df9['Provider'].head(12)
count = df9['Frequency'].head(12)

# Figure Size
fig, ax = plt.subplots(figsize =(16, 9))

# Horizontal Bar Plot
ax.barh(name, count)

# Remove axes splines
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)

# Remove x, y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')

# Add padding between axes and labels
ax.xaxis.set_tick_params(pad = 5)
ax.yaxis.set_tick_params(pad = 10)

# # Add x, y gridlines
# ax.grid(b = True, color ='grey',
# linestyle ='-.', linewidth = 0.5,
# alpha = 0.2)

# Show top values
ax.invert_yaxis()

# Add annotation to bars
for i in ax.patches:
    plt.text(i.get_width()+0.2, i.get_y()+0.5,
    str(round((i.get_width()), 2)),
    fontsize = 10, fontweight ='bold',
    color ='grey')

# Add Plot Title
ax.set_title('providers in campaign 1 and their frequency messages in campaign1',loc ='left', )

# Add Text watermark
fig.text(0.9, 0.15, 'Jeeteshgavande30', fontsize = 12,
color ='grey', ha ='right', va ='bottom',
alpha = 0.7)

# Show Plot
print(plt.show())


# find the frequeancy of status of the messages of APP1
df11 =  df4.groupby('Status').size().sort_values(ascending=False).reset_index()
df11.rename(columns =  {0:'No_of_msges'},inplace = True)
print("status of  messages sent\n\n",df11)

# pie chart between Delivered,No and Failed Messages.

STATUS = ['Delivered', ' No', 'Failed']
 
data = [6667,1667,1666]
explode = (0.1, 0.0, 0.2)
 
# Creating color parameters
colors = ( "green", "blue", "red")
 
# Wedge properties
wp = { 'linewidth' : 1, 'edgecolor' : "green" }
 
# Creating autocpt arguments
def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n({:d} g)".format(pct, absolute)
 
# Creating plot
fig, ax = plt.subplots(figsize =(10, 4))
wedges, texts, autotexts = ax.pie(data,
                                  autopct = lambda pct: func(pct, data),
                                  explode = explode,
                                  labels = STATUS,
                                  shadow = True,
                                  colors = colors,
                                  startangle = 90,
                                  wedgeprops = wp,
                                  textprops = dict(color ="black"))
 
 
plt.setp(autotexts, size = 8, weight ="bold")
ax.set_title("pie chart shows status of messages in campaign 1")
 
# show plot
print(plt.show())

# total messages sent in APP1 and number of messages delivered in APP1
total_sent = df4['Status'].count()
print("total messages sent in APP1\t",total_sent)
print("\n")
num_delivered = (df4['Status'] == 'Delivered').sum()
print("number of messages delivered in APP1\t",num_delivered)
# messages is Delivered with in 60 seconds in APP1.
msg_within60 = df4[(df4['Status']=='Delivered') & (df4['Diffrence Secs'] < 60)]
count = msg_within60['Diffrence Secs'].count()
print("number of messages in APP1 which sent with in 60 sec\t",count)
print("\n")

#total_sent = df5['Status'].count()
#print("total messages sent",total_sent)
num_delivered = (df5['Status'] == 'Delivered').sum()
print("number of messages is Delivered with in 60 seconds in APP1\t",num_delivered)
print("\n")

# messages is Delivered with in 60 seconds in APP2.
msg_within60 = df5[(df5['Status']=='Delivered') & (df5['Diffrence Secs'] < 60)]
time =msg_within60['Diffrence Secs'].count()
print("number of messages is Delivered with in 60 seconds in APP2\t", time)
print("\n")

# messages frequeancy sent by the diffrent provider.
provider = msg_within60.groupby('Provider').size().sort_values(ascending=False)
print("messages frequeancy sent by the diffrent provider in APP1\n\n",provider)

# Number of late messages delivered in APP1 which is Delivered more than 120 seconds.
late_messages = df4[df4['Diffrence Secs'] > 120]
print("Number of late messages delivered in APP1 which is Delivered more than 120 seconds\t",late_messages['Diffrence Secs'].count())
print("\n")
print(f" The shortest delivered time of msg in APP1 in seconds is\t {df4['Diffrence Secs'].min()}")
print("\n")
print(f" The longest delivered time of msg in APP1 in seconds is\t {df4['Diffrence Secs'].max()}")

# fetch the IP address column from the dataframe and extract information using ip address.
# fetching IP address column from df2
not_null_ip = df1.dropna(axis=0, subset=['IP Address'])
#convert ip address column to list
IP_list = not_null_ip["IP Address"].tolist()
IP_list[0:10]

# get the data using api
ip = []
city = []
region = []
country = []
def get_location(ip_address):
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data

#store information in list and then converted into dataframe.
print("store information in list and then converted into dataframe")
for i in range(0,5):
    response = get_location(IP_list[i])
    print(response)
    
    ip.append(IP_list[i])
    city.append(response.get("city"))
    region.append(response.get("region"))
    country.append(response.get("country"))
    
df13 = pd.DataFrame(list(zip(ip, city, region, country)),columns =["ip", "city", "region", "country"])

print(df13)