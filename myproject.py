from flask import Flask, render_template, url_for, request, jsonify
import pandas as pd
import numpy as np
import data as dt
import datetime
app = Flask(__name__)

@app.route('/shinobu', methods = ['GET'])
def kawaii():
    return render_template("index.html")
#mainblock
@app.route('/', methods = ['GET'])
def profile():
    return render_template("profile.html")
@app.route('/data', methods = ['GET'])
def data():
    data = pd.read_csv('s_data.csv')
    dataset = []
    for i in range(len(data)):
        temp = []
        for x in data.iloc[i]:
            temp.append(x)
        dataset.append(temp)
    dataset2 = dt.data_to_analysis
    return render_template("data.html",dataset = dataset,data=dataset2)
@app.route('/analysis', methods = ['GET'])
def analysis():
    dataset = dt.data_to_analysis
    return render_template("analysis.html",data = dataset)
    
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

@app.route('/charts')
def charts():
    dataset = dt.data_to_analysis
    return render_template("charts.html",data = dataset)

@app.route('/background_plot')#This page accessable only for js script
def background_process():
    date_start = request.args.get('date_start', 0, type= str)
    date_end = request.args.get('date_end', 0, type= str)
    region = request.args.get('region', 0, type= int)
    city = request.args.get('city', 0, type= str)
    street = request.args.get('street', 0, type= str)
    building = request.args.get('building', 0, type= int)
    flat = request.args.get('flat', 0, type= int)
    dep = int(request.args.get('dep', 0, type= int))
    dep_value = int(request.args.get('dep_value', 0, type= int))
    typee = request.args.get('typee', 0, type= int)
    if dep_value == 1:
        id_req = dt.get_id(region, city, street, building, flat)
        return jsonify(dt.get_temperature(dt.load_id(id_req),dep))
    else:
        if typee == 2:
            if city == "Город":
                return jsonify(dt.get_mean_region(dt.load_region(region),dep))
            else:
                id_req = dt.get_id(region, city, street, building, flat)
                return jsonify(dt.get_mean(dt.load_id(id_req),id_req,dep))
        else:
            if city == "Город":
                return jsonify(dt.get_plot_data_region(dt.load_region(region),date_start,date_end,dep))
            else:
                id_req = dt.get_id(region, city, street, building, flat)
                return jsonify(dt.get_plot_data(dt.load_id(id_req),date_start,date_end,id_req,dep))

    #return jsonify(dt.get_plot_data(dt.load_id(id_req),date_start,date_end,id_req,dep))

@app.route('/background_select', methods = ['GET'])
def select():   
    regions_cities = dt.regions_cities
    region = request.args.get('region', 0, type= int)
    if region == 0:
        cities = regions_cities[region]
        return jsonify(city = data)
    else:
        cities = regions_cities[region]
        return jsonify(city = cities)
@app.route('/background_analysis', methods = ['GET'])   
def do_analysis():
    date_start = request.args.get('date_start', 0, type= str)
    output = {'y': ['6', '1', '2'], 'x1': [1, 2], 'x2': [1, 2,5, 4]}
    return jsonify(dt.get_neural(date_start))
@app.route('/background_data', methods = ['GET'])
def bg_data():   
    date_start = request.args.get('date_start', 0, type= str)
    date_end = request.args.get('date_end', 0, type= str)
    region = request.args.get('region', 0, type= int)
    city = request.args.get('city', 0, type= str)
    street = request.args.get('street', 0, type= str)
    building = request.args.get('building', 0, type= int)
    flat = request.args.get('flat', 0, type= int)
    
    if city == "Город":
        return jsonify(dt.get_data_region(dt.load_region(region),date_start,date_end))
    else:
        id_req = dt.get_id(region, city, street, building, flat)
        return jsonify(dt.get_data(dt.load_id(id_req),date_start,date_end,id_req,1))

@app.route('/time', methods = ['GET'])
def time():
   return(datetime.datetime.now().isoformat()[:10] + '-' + datetime.datetime.now().isoformat()[11:-7])
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.debug = True
    app.run(host = '0.0.0.0')
