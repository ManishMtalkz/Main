import pandas as pd
import numpy as np
from datetime import datetime
from flask import Flask, jsonify
from flask import*
# analysis = Blueprint("analysis", __name__, static_folder="static", template_folder="templates")

app = Flask(__name__)

@app.route('/')
def hello_world():
   return jsonify({"status":"welcome to anlysis part"})
# read dataset
# def dataset(deli,undeli,resp,nreac):
def dataset(ansString):
    df1 = pd.read_csv('dataset.csv',low_memory=False)
    # print("first five rows of the dataset\n\n",df1.head())
    # print("\n")
    # Drop the unwanted column.
    df1.drop(['Unnamed: 15','Unnamed: 16'], inplace = True,axis = 1)
    # print("shape of the dataset",df1.shape)
    # checking the null values in the dataset.
    # df1.isnull()
    # print("\n")
    # total number of null values present in each column
    # print("total number of null values present in each column\n\n",df1.isnull().sum())
    # filling the null values using fillna function.
    df2 = df1.fillna(value={'Provider':'unknown' , 'Click Count':0 , 'Click Status':'NA' , 'Click DateTime':'NA' , 'Browser':'NA' , 'Platform':'not define' , 'IP Address':'not define' ,'Status':'No'})
   
    #After fill the null value check the null value in dataset.
    # print("After fill the null value total null value in dataset",df2.isnull().sum().sum())
    # print("\n")
    # convert send time and Delivered time into datetime datatype
    df2["Send Time"] =  pd.to_datetime(df2["Send Time"], infer_datetime_format=True)
    df2["Delivered Time"] =  pd.to_datetime(df2["Delivered Time"], infer_datetime_format=True)
    #find the difference between delivered time and send time,and convert in seconds.
    df2["Diffrence Time"] = df2["Delivered Time"] - df2["Send Time"]
    seconds = df2["Diffrence Time"].astype('timedelta64[s]').astype(np.int32)
    df2["Diffrence Secs"] = seconds
    # print("data types of column present in the dataset\n\n",df2.dtypes)
    # print("\n")
    # print("rows and column of the dataset\t",df2.shape)
    #print("print the dataset which cointaining diffrence seconds column",df2.head())
    # print("\n")
    # Here we grouped the the df2
    df3 = df2.groupby("Campaign name")
    df3
    # for x,y in df3:
    #     print(x)
    #     print(y.head())
    #     print()
    df4 = df3.get_group("APP1")
    # providers in APP1 and their frequency messages in APP1
    df5 = df4.groupby('Provider').size().sort_values(ascending=False).reset_index()
    df5.rename(columns =  {0:'Frequency'},inplace = True)
    # print(df5)
    data_dict = df5.to_dict()
    # print(data_dict)
    #return delivered rate of caimpaign     APP1----
    total_sent = df4['Message'].count()
    # print("total messages sent",total_sent)
    num_delivered = (df4['Status'] == 'Delivered').sum()
    # print(num_delivered)
    delivered_rate = (num_delivered / total_sent) * 100
    # print("delivered rate of APP1",delivered_rate)
    #undelivered rate-----------
    total_sent = df4['Status'].count()
    num_undelivered = (df4['Status'] == 'No').sum()
    # print("number of undelivered msges\t",num_undelivered)
    undelivered_rate = (num_undelivered / total_sent) * 100
    # print("undelivered rate of APP1\t",undelivered_rate)
    #response rate-----------
    total_sent = df4['Click Status'].count()
    # print("total messages sent \n",total_sent)
    clicked_msg = (df4['Click Status'] == 'Yes').sum()
    # print("number of messages clicked\t",clicked_msg)
    response_rate = (clicked_msg  / total_sent)*100
    # print("response rate of APP1\t",response_rate)
    #now calculating the failure rate of APP1---
    total_sent = df4['Click Status'].count()
    # print("total messages sent\n\t",total_sent)
    options = ['No']
    df6 = df4[(df4['Status'] == 'Delivered') & (df4['Click Status'].isin(options))]
    unclicked_msg = df6['Status'].count()
    # print("number of unclicked messages\t",unclicked_msg)
    nonreaction_rate = (unclicked_msg  / total_sent)*100
    # print("nonreaction_rate  of APP1\t",nonreaction_rate)
    # find the frequeancy of status of the messages of APP1
    df7 =  df4.groupby('Status').size().sort_values(ascending=False).reset_index()
    df7.rename(columns =  {0:'No_of_msges'},inplace = True)
    # print("status of  messages sent\n\n",df7)
    data_dict2 = df7.to_dict()
    if (ansString == "deliveredRate"):
        return str(delivered_rate)
    if(ansString == "undeliverRate"):
        return str(undelivered_rate)
    if(ansString== "responseRate"):
        return str(response_rate)
    if(ansString=="nonReactionRate"):
        return str(nonreaction_rate)
    return data_dict
# res = dataset('deli', 'undeli', 'resp',  'nreac')
# deli  = True
# res = dataset(deli)
# print("delivered rate of APP1 => ",res)
# undeli  = True
# res = dataset(undeli)
# print("undelivered rate of APP1 => ",res)
# resp  = True
# res = dataset(resp)
# print("response rate of APP1 => ",res)
# nreac  = True
# res = dataset(nreac)
# print("nonreaction rate of APP1 => ",res)
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
        elif request.method == 'GET':
            args = request.args
            args = args.to_dict()
            if 'get' in args:
                rec = args['get']
                if rec == 'deliveredRate':
                    res = dataset("deliveredRate")
                    deliveredRate = res
                    print('delivered rate: '+deliveredRate)
                    return jsonify({"deliverRate": deliveredRate})
            if 'get' in args:
                rec = args['get']
                if rec == 'undeliverRate':
                    res = dataset("undeliverRate")
                    undeliverRate = res
                    print("undeliverRate: " + str(undeliverRate))
                    return jsonify({"undeliverRate": undeliverRate})
            if 'get' in args:
                rec = args['get']
                if rec == 'responseRate':
                    res = dataset("responseRate")
                    responseRate = res
                    print("responseRate : " + responseRate)
                    return jsonify({"responseRate": responseRate})
            if 'get' in args:
                rec = args['get']
                if rec == 'nonReactionRate':
                    res = dataset("nonReactionRate")
                    nonReactionRate = res
                    print("nonReactionRate : " + nonReactionRate)
                    return jsonify({"nonReactionRate": nonReactionRate})
            res = dataset("akainu")
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
            return jsonify({"final data":ans}) ,200
        else:
            return jsonify({"status":"Invalid request"}), 400
    except Exception as e:
        print(e)
        return jsonify({"error":e})
    
  
if __name__ == '__main__':
    app.run(debug = True)
  