import pandas as pd
import numpy as np
import json
import requests
from matplotlib import pyplot as plt
from datetime import datetime
from fastapi import FastAPI


app = FastAPI()

df = pd.read_csv("https://mtalkzplatformstorage.blob.core.windows.net/mtalkz-files-transfer/ig138I5Ecgez1TL.csv",low_memory=False)


def parse_csv(df):
    res = df.to_json(orient="records")
    parsed = json.loads(res)
    return parsed
    
@app.get("/questions")
def load_questions():
    return parse_csv(df)



@app.get("/delivered_rate")
def pie_chart():

    STATUS = ['Delivered', ' No', 'Failed']

    data = [6667, 1667, 1666]
    explode = (0.1, 0.0, 0.2)

    # Creating color parameters
    colors = ("green", "blue", "red")

    # Wedge properties
    wp = {'linewidth': 1, 'edgecolor': "green"}

    # Creating autocpt arguments
    def func(pct, allvalues):
        absolute = int(pct / 100.*np.sum(allvalues))
        return "{:.1f}%\n({:d} g)".format(pct, absolute)

    # Creating plot
    fig, ax = plt.subplots(figsize=(10, 4))
    wedges, texts, autotexts = ax.pie(data,
                                      autopct=lambda pct: func(pct, data),
                                      explode=explode,
                                      labels=STATUS,
                                      shadow=True,
                                      colors=colors,
                                      startangle=90,
                                      wedgeprops=wp,
                                      textprops=dict(color="black"))

    plt.setp(autotexts, size=8, weight="bold")
    ax.set_title("pie chart shows status of messages in campaign 1")

    # show plot
    return plt.show()




    

