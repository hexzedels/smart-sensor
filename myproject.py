from flask import Flask, render_template, url_for, request, jsonify
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
#mainblock
@app.route('/', methods = ['GET'])
def hello_world():
    return render_template("profile.html")
@app.route('/dat', methods = ['GET'])
def dat():
    data = pd.read_csv('s_data.csv')
    dataset = []
    for i in range(len(data)):
        temp = []
        for x in data.iloc[i]:
            temp.append(x)
        dataset.append(temp)
    return render_template("data.html",dataset = dataset)
@app.route('/analysis', methods = ['GET'])
def analysis():
    return render_template("analysis.html")
@app.route('/notifications', methods = ['GET'])
def notifications():
    return render_template("notifications.html")
@app.route('/payment', methods = ['GET'])
def payment():
    return render_template("payment.html")



@app.route('/dataformat')
def send_to():
    return '{"id": 0, "I": 1.5, "U":3.1, "P":36, "T":1.2, "I_max":3.6, "U_max":36, "timecode": "2020-08-14-19:48"}'
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

    return '<img src="data:imy/png;base64,{}">'.format(plot_url)
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

@app.route('/background_plot')#This page accessable only for js script
def background_process():
    #I'm really sorry for hardcode
    data_msk =  {
   "jsonarray": [{
      "xs": "2020-02-03",
      "ys": 12
   }, {
      "xs": "2020-02-04",
      "ys": 7
   },{
      "xs": "2020-02-05",
      "ys": 15
   },{
      "xs": "2020-02-05",
      "ys": 9
   }]
};
    data_spb =  {
   "jsonarray": [{
      "xs": "2020-02-03",
      "ys": 5
   }, {
      "xs": "2020-02-04",
      "ys": 25
   },{
      "xs": "2020-02-05",
      "ys": 10
   },{
      "xs": "2020-02-05",
      "ys": 4
   }]
};
    data_vlc =  {
   "jsonarray": [{
      "xs": "2020-02-03",
      "ys": 20
   }, {
      "xs": "2020-02-04",
      "ys": 8
   },{
      "xs": "2020-02-05",
      "ys": 12
   },{
      "xs": "2020-02-05",
      "ys": 9
   }]
};      
    answ = request.args.get('region', 0, type= str)
    if answ == '777':
        return jsonify(data_msk)
    elif answ == '25':
        return jsonify(data_vlc)
    else:
        return jsonify(data_spb)
    
@app.route('/time', methods = ['GET'])
def time():
   return(datetime.datetime.now().isoformat()[:10] + '-' + datetime.datetime.now().isoformat()[11:-7])
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    #app.debug = True
    app.run(host = '0.0.0.0')
