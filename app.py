import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast
import requests
from datetime import datetime
from flask import Flask, jsonify
from flask import Flask, render_template
from flask import*
import nltk
import re
import string
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
#--------------------data pre-processing------------------------#
#dataset1
app = Flask(__name__)

def dataset(url1,url2):
    
    #-------------------- data preprocessing----------------------#
        
    df1 =pd.read_csv(str(url1))
    # df1.dtypes
    #dataset2
    df2 = pd.read_csv(str(url2))
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

    d = dict();

    #-----------------------calculate diffrence btwn sent-time and delivered time---------#
    # convert send time and Delivered time into datetime datatype----
    merge_dff["Send Time"] =  pd.to_datetime(merge_dff["Send Time"], infer_datetime_format=True)
    merge_dff["Delivered Time"] =  pd.to_datetime(merge_dff["Delivered Time"], infer_datetime_format=True)
    #Diffrence of send time and delivered time.-------
    merge_dff["Diffrence Time"] = merge_dff["Delivered Time"] - merge_dff["Send Time"]
    seconds = merge_dff["Diffrence Time"].astype('timedelta64[s]').astype(np.int32)
    merge_dff["Diffrence Secs"] = seconds
    # print(merge_dff.dtypes)


        
    #return delivered rate of caimpaign     

    total_sent = merge_dff['Message'].count()
    # print("total messages sent",total_sent)
    num_delivered = (merge_dff['Status'] == 'Delivery').sum()
    # print(f"number of messages delivered in APP1\t{num_delivered}")
    delivered_rate = (num_delivered / total_sent) * 100
    d['delivered_rate'] = delivered_rate


    # undelivered rate-----------


    total_sent = merge_dff['Status'].count()
    num_undelivered = (merge_dff['Status'] == 'Other').sum()
    # print("number of undelivered msges\t",num_undelivered)
    undelivered_rate = (num_undelivered / total_sent) * 100
    d['undelivered_rate']=undelivered_rate

    #response rate-----------
        

    total_sent = merge_dff['Status'].count()
    # print("total messages sent \n",total_sent)
    clicked_msg = (merge_dff['Clicks'] > 0).sum()
    # print("number of messages clicked\t",clicked_msg)
    response_rate = (clicked_msg  / total_sent)*100
    d['response_rate']=response_rate
    

    #now calculating the non-reaction rate ---
    total_sent = merge_dff['Status'].count()
    # print("total messages sent\n\t",total_sent)
    unclicked_msg = (merge_dff['Clicks'] == 0).sum()
    # print("number of unclicked messages\t",unclicked_msg)
    nonreaction_rate = (unclicked_msg  / total_sent)*100
    d['nonreaction_rate']=nonreaction_rate



    #  frequeancy of status of the messages
    df4 =  merge_dff.groupby('Status').size().sort_values(ascending=False).reset_index()
    df4.rename(columns =  {0:'No_of_msges'},inplace = True)
    j = df4.set_index('Status')['No_of_msges'].to_json()
    sta = ast.literal_eval(j)
    
   #----Provider and its frequency-----------
    df5 =  merge_dff.groupby('Provider').size().sort_values(ascending=False).reset_index()
    df5.rename(columns =  {0:'Frequency'},inplace = True)
   
    i = df5.set_index('Provider')['Frequency'].to_json()
    pro = ast.literal_eval(i)



    
    # #---------------------most frequent word---------------------------
    
    df6 = merge_dff[(merge_dff['Clicks'] > 0) & (merge_dff['Campaign name'] !=  'NaN')]

    stop_words = stopwords.words()

    def cleaning(text):        
        # converting to lowercase, removing URL links, special characters, punctuations...
        text = text.lower()
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('[’“”…]', '', text)     

        # removing the stop-words          
        text_tokens = word_tokenize(text)
        tokens_without_sw = [word for word in text_tokens if not word in stop_words]
        filtered_sentence = (" ").join(tokens_without_sw)
        text = filtered_sentence
    
        return text

    dt = df6['Campaign name'].apply(cleaning)

    from collections import Counter
    p = Counter("Message".join(dt).split()).most_common(5)
    rslt = pd.DataFrame(p, columns=['Word', 'Frequency'])
    print(rslt)
    dict1 = {"diff_rates":d,"provider_freq":pro,"status_msg":sta}
    
    return d,pro,sta,dict1
 
# d,pro,sta,dict1 = dataset()
@app.route('/all_analytics', methods=['GET'])
def all_data():
    try:
        url1 = None
        url2 = None
        d={}
        pro ={}
        sta = {}
        dict1 = {}
        mlist = []
        if request.method == 'GET':
            args = request.args
            args = args.to_dict()

            if 'url2' in args and 'url1' in args:
                url2 = args['url2']
                url1 = args['url1']
            else:
                return jsonify({"status":"enter url please"}) ,200
            d,pro,sta,dict1 = dataset(url1,url2)
            mlist.append(d)
            mlist.append(pro)
            mlist.append(sta)
            mlist.append(dict1)
            return jsonify({"data":mlist}) ,200
            
        else:
            return jsonify({"status":"Invalid request"}) ,400
    
    except Exception as e:
        print(e)
        return jsonify({"status":e})
    # return jsonify({"all analytics":dict1})
       
    
    
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
  










