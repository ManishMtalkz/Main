import pandas as pd
import numpy as np
import json
import warnings
import pandas_profiling as ProfileReport 
warnings.simplefilter(action='ignore', category=FutureWarning)

with open('updated_data.json' ,'r',encoding = 'utf8') as data_file:    
    data = json.load(data_file)
    
df = pd.io.json.json_normalize(data)
print()
# profile = ProfileReport(df, title="Hello")
# df.profile_report().to_file("chatbot_report.html")