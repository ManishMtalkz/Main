import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests
from datetime import datetime
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

  #-------------------- data preprocessing----------------------#
    
df1 =pd.read_csv("https://mtalkzplatformstorage.blob.core.windows.net/mtalkz-files-transfer/ynX1KNPiiyFRLwS.csv")
# df1.dtypes
#dataset2
df2 = pd.read_csv("https://mtalkzplatformstorage.blob.core.windows.net/mtalkz-files-transfer/Qxozys6Bpi66Cvt.csv")
df2.dtypes
df2.rename(columns = {'Campaign Name':'Campaign name'}, inplace = True)
merge_dff = pd.merge(df1, df2, on ='Number',how='outer')
merge_dff.head()
#null value present in each column.-----
merge_dff.isnull().sum()

#-----------------Rename column-------------------
merge_dff.rename(columns = {'Location_y':'Click Location','Location_x':'Provider Location','Campaign name_x':'Campaign name','Count':'Clicks'}, inplace = True)
merge_dff.head()
#remove extra column---------------



# ---------------------dealing with null values-------------------
merge_dff= merge_dff.fillna(value={'Provider Location':'unknown' , 'Provider':'unknown' , 'Browser':'unknown' , 'Platform':'unknown'   ,'Status':'No','Clicks':0,'Click Location':'unknown'})
merge_dff.drop(['Campaign name_y'], inplace = True,axis = 1)
merge_dff['Clicks'] = merge_dff['Clicks'].astype(int)
merge_dff['Status'] = merge_dff['Status'].replace(['Delivery','Other'], ['Delivered','Failed'])

#-----------------------calculate diffrence btwn sent-time and delivered time---------#
# convert send time and Delivered time into datetime datatype----
merge_dff["Send Time"] =  pd.to_datetime(merge_dff["Send Time"], infer_datetime_format=True)
merge_dff["Delivered Time"] =  pd.to_datetime(merge_dff["Delivered Time"], infer_datetime_format=True)
#Diffrence of send time and delivered time.-------
merge_dff["Diffrence Time"] = merge_dff["Delivered Time"] - merge_dff["Send Time"]
seconds = merge_dff["Diffrence Time"].astype('timedelta64[s]').astype(np.int32)
merge_dff["Diffrence Secs"] = seconds

    
#return delivered rate of caimpaign     

total_sent = merge_dff['Message'].count()
Delivered = (merge_dff['Status'] == 'Delivered').sum()
delivered_rate = (Delivered / total_sent) * 100

# undelivered rate-----------
total_sent = merge_dff['Status'].count()
Failed = (merge_dff['Status'] == 'Failed').sum()
undelivered_rate = (Failed / total_sent) * 100

#response rate-----------
total_sent = merge_dff['Status'].count()
Clicked = (merge_dff['Clicks'] > 0).sum()
response_rate = (Clicked / total_sent)*100

#now calculating the non-reaction rate ---
total_sent = merge_dff['Status'].count()
unclicked_msg = (merge_dff['Clicks'] == 0).sum()
notresponse_rate = (unclicked_msg  / total_sent)*100

#  frequeancy of status of the messages
df4 =  merge_dff.groupby('Status').size().sort_values(ascending=False).reset_index()
df4.rename(columns =  {0:'No_of_msges'},inplace = True)
j = df4.set_index('Status')['No_of_msges'].to_json()
df6 = merge_dff.groupby('Status').size().sort_values(ascending=False).reset_index()
df6.rename(columns =  {0:'No_of_msges'},inplace = True)

#----Provider and its frequency-----------
df5 =  merge_dff.groupby('Provider').size().sort_values(ascending=False).reset_index()
df5.rename(columns =  {0:'Frequency'},inplace = True)

# df_top10 = df5.nlargest(10, "df5")
top10_Provider = df5["Provider"].tolist()
top10_freq = df5["Frequency"].tolist()

#fetching info. of client with the help of ip address-----------
not_null_ip = merge_dff.dropna(axis=0, subset=['IP Address'])
IP_list = not_null_ip["IP Address"].tolist()

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
        "country": response.get("country")
    }
    return location_data
    

for i in range(0,5):
    response = get_location(IP_list[i])
    # print(response)
    ip.append(IP_list[i])
    city.append(response.get("city"))
    region.append(response.get("region"))
    country.append(response.get("country"))
    
    
df8 = pd.DataFrame(list(zip(ip, city, region, country)),columns =["ip", "city", "region","country"])
# print(df8)


# declare an empty list to store
# latitude and longitude of values
# of city column
longitude = []
latitude = []

# function to find the coordinate
# of a given city
def findGeocode(city):
	
	# try and catch is used to overcome
	# the exception thrown by geolocator
	# using geocodertimedout
	try:
		
		# Specify the user_agent as your
		# app name it should not be none
		geolocator = Nominatim(user_agent="your_app_name")
		
		return geolocator.geocode(city)
	
	except GeocoderTimedOut:
		
		return findGeocode(city)	

# each value from city column
# will be fetched and sent to
# function find_geocode
for i in (df8["city"]):
	
	if findGeocode(i) != None:
		
		loc = findGeocode(i)
		
		# coordinates returned from
		# function is stored into
		# two separate list
		latitude.append(loc.latitude)
		longitude.append(loc.longitude)
	
	# if coordinate for a city not
	# found, insert "NaN" indicating
	# missing value
	else:
		latitude.append(np.nan)
		longitude.append(np.nan)

# now add this column to dataframe
df8["Longitude"] = longitude
df8["Latitude"] = latitude
  
# print(df8)


fig = make_subplots(
    rows = 4, cols = 6,
    specs=[
            [{"type": "scattergeo", "rowspan": 4, "colspan": 3}, None, None, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"} ],
            [    None, None, None,               {"type": "bar", "colspan":3}, None, None],
            [    None, None, None,              {"type": "bar", "colspan":3}, None, None],
            [    None, None, None,               {"type": "bar", "colspan":3}, None, None],
          ]
)

#Create annotation text--------------
message = df8["country"] + "<br>"
message += "City: " + df8["city"] + "<br>"
message += "Region " + df8["region"] + "<br>"
df8["text"] = message


# Create subplot — Scattergeo map----------------
fig.add_trace(
    go.Scattergeo(
        
        locationmode = "country names",
        lon = df8["Longitude"],
        lat = df8["Latitude"],
        hovertext = df8["text"],
        showlegend=False,
        marker = dict(
            size = 10,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = True,
            symbol = 'square',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            cmin = 0,
            # color = df8['city'],
            # cmax = df8['region'],
            colorbar_title="usercity<br>user region",  
            colorbar_x = -0.05
        )

    ),
    
    row=1, col=1
)

#--------------------indicators-------------
fig.add_trace(
    go.Indicator(
        mode="number",
        value= Clicked,
        title="Clicked",
    ),
    row=1, col=4
)

fig.add_trace(
    go.Indicator(
        mode="number",
        value= Delivered,
        title="Delivered",
    ),
    row=1, col=5
)

fig.add_trace(
    go.Indicator(
        mode="number",
        value=Failed,
        title="Failed",
    ),
    row=1, col=6
)

fig.add_trace(
    go.Bar(
        x=top10_Provider,
        y=top10_freq, 
        marker=dict(color="crimson"), 
        name= "Provider and its frequency",

        showlegend=True),
    row=4, col=4
)

# ----------------------Finalize layout setting------------------
fig.update_layout(
    template="plotly_dark",
    title = "SMS CAIMPAIGN REPORT",
    showlegend=True,
    legend_orientation="h",
    legend=dict(x=0.65, y=0.8),
    geo = dict(
            projection_type="orthographic",
            showcoastlines=True,
            landcolor="white", 
            showland= True,
            showocean = True,
            lakecolor="LightBlue"
    ),
    
    annotations=[
        dict(
            
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.35,
            y=0)
    ]

   
)

fig.write_html('index.html', auto_open=True)








