# import libraries for data pre-processing.
import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt

data = [json.loads(line) for line in open('final1.json', 'r',encoding="utf8")]
df = pd.json_normalize(data)
pd.set_option('display.max_columns',500)
print(df.head())

# print shape of the dataframe.
print(df.shape)

# Rename some selected column-------------->
df.rename(columns = {'properties.uniq_id':'uniqid','chatbot_id.$oid':'chatbot_id','properties.instance_id':'instance_id','properties.message_text':'user message','properties.message':'chatbot message','properties.flowchart':'flowchart_name'}, inplace = True)
df.head()

# here we select some features(columns) to find out some insights.
df2 = df[['instance_id','uniqid','chatbot_id','event','user message','chatbot message','flowchart_name']].copy()


# Here i fetch those record where the instance id is not null--------------->
res = df2[df2['instance_id'].notna()]
print(res.head())


# check the null value in particular column---------->
res.isnull().sum()

# select only one chatbot id----->
rslt_df = res.loc[res['chatbot_id'] == '63a304d4cb2b4006beee1097']
rslt_df.head()

# Find Unique instance_id present in the chatbot.
count = rslt_df.instance_id.unique().size
print("Unique instance id count : "+ str(count))

# count  chatbot id
count = rslt_df.chatbot_id.unique().size
print("Unique chatbot id count : "+ str(count))

# unique id present in that particular chatbot id.
count = rslt_df.uniqid.unique()
print("Unique unique id  : "+ str(count))

#count of unique id on that particular chatbot id.
count = rslt_df.uniqid.unique().size
print("Unique unique id count : "+ str(count))



