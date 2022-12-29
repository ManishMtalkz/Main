import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast
from datetime import datetime
from flask import Flask, jsonify
from flask import Flask, render_template
from flask import*

app = Flask(__name__)

@app.route('/')
def hello_world():
   return jsonify({"status":"welcome"})



# read dataset ,undeli,resp,nreac
def dataset():
    df1 = pd.read_csv("dataset.csv",low_memory=False)
    d = dict();
    
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
    i = df5.set_index('Provider')['Frequency'].to_json()
    pro = ast.literal_eval(i)
   
    
    #return delivered rate of caimpaign     APP1----
    
    total_sent = df4['Message'].count()
    # print("total messages sent",total_sent)
    num_delivered = (df4['Status'] == 'Delivered').sum()
    # print(f"number of messages delivered in APP1\t{num_delivered}")
    delivered_rate = (num_delivered / total_sent) * 100
    d['delivered_rate'] = delivered_rate
    
    
    # undelivered rate-----------
    
    
    total_sent = df4['Status'].count()
    num_undelivered = (df4['Status'] == 'No').sum()
    # print("number of undelivered msges\t",num_undelivered)
    undelivered_rate = (num_undelivered / total_sent) * 100
    d['undelivered_rate']=undelivered_rate
    
    #response rate-----------
        
    
    total_sent = df4['Click Status'].count()
    # print("total messages sent \n",total_sent)
    clicked_msg = (df4['Click Status'] == 'Yes').sum()
    # print("number of messages clicked\t",clicked_msg)
    response_rate = (clicked_msg  / total_sent)*100
    d['response_rate']=response_rate
    
    
    #now calculating the non-reaction rate of APP1---
    
    
    total_sent = df4['Click Status'].count()
    # print("total messages sent\n\t",total_sent)
    options = ['No']
    df6 = df4[(df4['Status'] == 'Delivered') & (df4['Click Status'].isin(options))]
    unclicked_msg = df6['Status'].count()
    # print("number of unclicked messages\t",unclicked_msg)
    nonreaction_rate = (unclicked_msg  / total_sent)*100
    d['nonreaction_rate']=nonreaction_rate
    
    
    
    # find the frequeancy of status of the messages of APP1
    df7 =  df4.groupby('Status').size().sort_values(ascending=False).reset_index()
    df7.rename(columns =  {0:'No_of_msges'},inplace = True)
   
    
    j = df7.set_index('Status')['No_of_msges'].to_json()
    sta = ast.literal_eval(j)
   
    dict1 = {"diff_rates":d,"provider_freq":pro,"status_msg":sta}
    # return dict1
    return d,pro,sta,dict1

d,pro,sta,dict1 = dataset()
@app.route('/all_analytics', methods=['GET'])
def all_data():
    return jsonify({"all analytics":dict1})
       
    
    
@app.route('/diff_rates', methods=['GET'])
def insights():
    return jsonify({"diffrent rates in APP1":d})

@app.route('/provider_freq',methods =['GET'])
def provider_freq():
    return jsonify({"provider in camp1 and their freq":pro})

@app.route('/status',methods =['GET'])
def status():
    return jsonify({"status of messages in APP1":sta})


if __name__ == '__main__':
    app.run(debug = True)
  