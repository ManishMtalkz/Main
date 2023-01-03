from flask import*
import pandas as pd 
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

df = pd.read_csv("App2Camp.csv")

df2 = df.head()

app = Flask(__name__)

@app.route('/')
@app.route('/pandas',methods = ['GET','post'])

def data():
    return render_template('pandas.html',table = [df2.to_html(classes='data',index=False)],titles=df2.columns.values)


@app.route('/matplot',methods=['GET','POST'])
def mpl():
    return render_template('matplot.html',PageTitle = 'Matplotlib')


@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():
    STATUS = ['Delivered', ' No', 'Failed']
    data = [6667,1667,1666]
    # Creating plot
    fig = plt.figure(figsize =(10, 5))
    plt.pie(data, labels = STATUS)
    
    
    
    return fig


if __name__ == '__main__':
    app.run(debug = True)