import pandas as pd
import numpy as np
from datetime import datetime
from flask import Flask, jsonify
from flask import Flask, render_template
from flask import*
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import datetime
import time
import pytz
import json
import ast
import io

app = Flask(__name__)


def dataset():
    
    d = dict()
    df = pd.read_csv("eventlogs.csv")
    df.head()

    # shape of the dataframe
    df.shape

    # find null values in each column of the dataframe
    df.isna().sum().reset_index()

    # drop the column which cointain null data
    df.drop(df.columns[[4,7,11,14,15,16,17,20,21,22,23]], axis=1, inplace=True)

    #dealing with null values
    # replace null values by fill null string.
    df = df.fillna('')
    # sending message ----------> chatbot.
    # new message ---------------> user.

    # find out events in the dataset and also count the frequency of that.
    df2 = df.groupby('event').size().sort_values(ascending=False).reset_index()
    df2.rename(columns =  {0:'status'},inplace = True)
    event_freq = df2.set_index('event')['status'].to_json()
    event_count = ast.literal_eval(event_freq)
    # print("events in the dataset and also count the frequency of that \n",df2)


    # Find the number of user intreact with chatboat.
    df['uniq_id'].unique()

    c_id = len(pd.unique(df['chatbot_id']))
    # print("number of unique chatbot id present in the dataframe\t",c_id)
    d['unique_chatbot_id']= c_id

    _id = len(pd.unique(df['_id']))
    d['unique__id']= _id

    # print("number of unique _id in the dtadset\t",u_id)

    u_id = len(pd.unique(df['uniq_id']))
    # print("number of unique id present in the datframe\t",_id)
    d['unique_uniq_id']= u_id

     
    #convert utc timestamp to datetime formate 
    #fetch time fro datatime. 
    df['utc_to_datetime'] = pd.to_datetime(df['createdAt'], utc=False, unit='ms')
    df['time'] = df['utc_to_datetime'].dt.strftime('%H:%M:%S')

    # combining the similar type of column.
    df["Flowchart"] = df["properties.flowchart_name"].map(str) + "" + df["properties.flowchart"]
    df['combined_column'] = df[df.columns[6:13]].apply(
        lambda x: '|'.join(x.dropna().astype(str)),
        axis=1
    )

    # find the frequency of the flow that user follow in the whole sessions.
    df3 = df.groupby('combined_column').size().sort_values(ascending=False).reset_index()
    df3.rename(columns =  {0:'freq'},inplace = True)
    flow_freq = df3.set_index('combined_column')['freq'].to_json()
    flow_count = ast.literal_eval(flow_freq)
    # print("find the frequency of the flow that user follow in the whole sessions\n",df3)
    
    return d,event_count,flow_count


    
d,event_count,flow_count = dataset()

list = []
list.append(d)
list.append(event_count)
list.append(flow_count)
    
    
    
@app.route('/', methods=['GET'])
def home():
    return 'welcome to analytics part'


@app.route('/all', methods = ['GET'])
def all():
    return jsonify(list)



if __name__ == '__main__':
    app.run(debug = True)
