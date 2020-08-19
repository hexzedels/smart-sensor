from flask import Flask, render_template, url_for
from flask import request
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import json
import numpy as np
import data as dt
import datetime
app = Flask(__name__)

@app.route('/shinobu', methods = ['GET'])
def kawaii():
    return render_template("index.html")

@app.route('/', methods = ['GET'])
def hello_world():
    return '<h1 style="text-align:center;">Intellectual monitoring!</h1>' 
@app.route('/dataformat')
def send_to():
    return '{"id": 0, "current": 1.5, "voltage":3.1, "temp":36, "max_current":1.2, "max_voltage":3.6, "timecode": "2020-08-14-19:48"}'
@app.route('/postdata', methods = ['POST'])
def postJSON():
    response = request.get_json(force=True)
    data = pd.read_csv('s_data.csv')
    data = dt.data_add(data,response)
    dt.save_data(data,'s_data.csv','csv')
    #dt.html_update(response)
    return 'Recieved'

@app.route('/plot')
def build_plot():
    data = pd.read_csv('s_data.csv')
    img = io.BytesIO()
    
    y = np.random.randint(1,25,6)
    x = [0,1,2,3,4,5]
    plt.plot(x,y)
    plt.savefig(img, format = 'png')
    img.seek(0)
    
    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)
@app.route('/data', methods = ['GET'])
def show_table():
    data = pd.read_csv('s_data.csv')
    dataset = []
    for i in range(len(data)):
        temp = []
        for x in data.iloc[i]:
            temp.append(x)
        dataset.append(temp)
        
    return render_template("s_data.html",dataset = dataset)
@app.route('/data', methods = ['GET'])
def time():
   return(datetime.datetime.now())
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config["CACHE_TYPE"] = "null"
    app.run(host = '0.0.0.0')
