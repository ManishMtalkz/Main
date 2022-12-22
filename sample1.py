#import the library for Data preprocessing-----
import pandas as pd
import numpy as np
from datetime import datetime
# import requests
from flask import Flask
from flask import Flask, jsonify
from flask import*

app = Flask(__name__)


@app.route('/')
def hello_world():
   return jsonify({"status":"welcome"})



# read dataset 
def dataset():
    df1 = pd.read_csv("demo_dataset.csv",low_memory=False)
    
    print("first five rows of the dataset\n\n",df1.head())
    print("\n")
    
    # Drop the unwanted column.
    df1.drop(['Unnamed: 15','Unnamed: 16'], inplace = True,axis = 1)
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
    
    df4 = df3.get_group("APP2")

    # providers in APP1 and their frequency messages in APP1
    df9 = df4.groupby('Provider').size().sort_values(ascending=False).reset_index()
    df9.rename(columns =  {0:'Frequency'},inplace = True)
    # print(df9)
    data_dict = df9.to_dict()
    print(data_dict)
    return data_dict

@app.route("/showdata",methods=['GET','POST'])
def showdata():
    try:

        if(request.method == 'POST'):
            res = dataset()
            provider = {}
            freq = {}
            provider = res['Provider']
            freq = res['Frequency']
            ans = {}
            
            for i in provider:
               
                valuep = provider[i]
                valuef = freq[i]
                
               
                ans[valuep] = valuef
                
            print("This is ans dict = ",ans)
            return jsonify({"status":ans}) ,200
        else:
            return jsonify({"status":"Invalid request"}), 400
        
    except Exception as e:
        print(e)
        return jsonify({"error":e})
    
      
if __name__ == '__main__':
   app.run(debug = True)
 