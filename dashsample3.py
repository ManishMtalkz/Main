import pandas as pd
import numpy as np
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

app = dash.Dash()


df1 = pd.read_csv("dataset.csv",low_memory=False)    
# Drop the unwanted column.
df1.drop(['Unnamed: 15','Unnamed: 16'], inplace = True,axis = 1)
# total number of null values present in each column
# print("total number of null values present in each column\n\n",df1.isnull().sum())
# filling the null values using fillna function.
df2 = df1.fillna(value={'Provider':'unknown' , 'Click Count':0 , 'Click Status':'NA' , 'Click DateTime':'NA' , 'Browser':'NA' , 'Platform':'not define' , 'IP Address':'not define' ,'Status':'No'})
print("\n")

#After fill the null value check the null value in dataset.
# convert send time and Delivered time into datetime datatype
df2["Send Time"] =  pd.to_datetime(df2["Send Time"], infer_datetime_format=True)
df2["Delivered Time"] =  pd.to_datetime(df2["Delivered Time"], infer_datetime_format=True)

#find the difference between delivered time and send time,and convert in seconds.
df2["Diffrence Time"] = df2["Delivered Time"] - df2["Send Time"]
seconds = df2["Diffrence Time"].astype('timedelta64[s]').astype(np.int32)
df2["Diffrence Secs"] = seconds

#print("print the dataset which cointaining diffrence seconds column",df2.head())
# print("\n")
# Here we grouped the the df2 
df3 = df2.groupby("Campaign name")
df3

for x,y in df3:
    print(x)
    # print(y.head())
    # print()

df4 = df3.get_group("APP1")

# providers in APP1 and their frequency messages in APP1
df5 = df4.groupby('Provider').size().sort_values(ascending=False).reset_index()
df5.rename(columns =  {0:'Frequency'},inplace = True)
print(df5)


app.layout = html.Div([

    dcc.Dropdown(
        id = 'first_dropdown',
        options = df5.Provider,
        placeholder='Select a Provider'
    )
    html.Div(id='output-graph')

])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='first_dropdown', component_property='options')]
)


    return dcc.Graph(id = 'Bar_Plor', 
                  figure = {
                      'data' : [
                          {'x':df5.Provider, 'y':df5.Frequency, 'type':'bar', 'name':'First Chart'}
                          ]
                      })
    
    
if __name__ == '__main__':
   app.run_server(debug=True)