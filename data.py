import pandas as pd
import numpy as np
import datetime
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from tensorflow import keras
data2 = pd.read_csv('csv/Sochi_new.csv')
data_reg = pd.read_csv('csv/Id_and_address.csv')
regions_cities = {
    0: ['Город'],
    50: ['Город','Москва', 'Долгопрудный', 'Подольск', 'Химки', 'Люберцы'],
    47: ['Город','Санкт-Петербург', 'Кудрово', 'Выборг', 'Гатчина', 'Всеволжск'],
    16: ['Город','Казань', 'Тетюши', 'Елабуга', 'Нижнекамск', 'Набережные Челны'],
    69: ['Город','Тверь', 'Калязин', 'Ржев', 'Осташков', 'Торжок'],
    33: ['Город','Владимир', 'Ковров', 'Муром', 'Суздаль', 'Гороховец']
}  
streets = ['Ул. Ладожская', 'Ул. Чкалова', 'Ул. Бабаевская', 'Ул. Есенина', 'Ул. Речников']
data_to_analysis = [streets,[i for i in range(1,6)], [i for i in range(1,11)]]
def data_add(data, response): # Accepts pandas-loaded csv table and formated json response
    temp_data = pd.DataFrame(columns=data.columns)
    for name in temp_data.columns:
        temp_data[name] = pd.Series(response[name])
    return data.append(temp_data) #ouputs new appended DataFrame

def save_data(data,name, ext): #LMAO bottom text
    if ext == 'csv' :
        data.to_csv(name, index = None)
    elif ext == 'html':
        data.to_html(name, index = None)
def html_update(response):
    ids, current, voltage, temp, max_current, max_voltage, timecode  = [response[x] for x in [i for i in response]]
    ending = '</tbody>\n</table>'
    sample = f'<tr>\n      <td>{ids}</td>\n      <td>{current}</td>\n      <td>{voltage}</td>\n      <td>{temp}</td>\n      <td>{max_current}</td>\n      <td>{max_voltage}</td>\n      <td>{timecode}</td>\n    </tr>\n'
    with open("templates/s_data.html", "r", encoding='utf-8') as f:
        text= f.read()
    strs = text[:-17] + sample + ending
    f= open("templates/s_data.html","w+")
    f.write(strs)
    f.close()
    
 #dataset related functions   
def get_id(region,city,street,building,flat):
    col = data_reg.columns #get column names
    return data_reg[(data_reg[col[1]] == region) & (data_reg[col[2]] == city) & (data_reg[col[3]] == street) & (data_reg[col[4]] == building)&(data_reg[col[5]] == flat)].iloc[0][0]

def load_id(x):
    data = pd.read_csv('csv/main/{}.csv'.format(x))
    return data
def load_region(x):
    data = pd.read_csv('csv/regions/{}.csv'.format(x))
    return data
'''
dependepcy codes are in table below
1: I(time)
2: U(time)
3: P(time)
4: T(time)
5: I_max(time)
6: U_max(time)
'''
code_to_labels = {1:['Сила тока','I, A','Дата и время'],
                  2:["Напряжение",'U, В','Дата и время'],
                  3:['Потребление','P, КВт*час','Дата и время'],
                  4:['Температура','T, °С','Дата и время'],
                  5:['Max сила тока','I_max, A','Дата и время'],
                  6:['Max напряжение','U_max, В','Дата и время'],
                 }
def get_plot_data(data,time_start,time_end,x,dep_code):
    temp_time = data[(data['timecode'] > time_start) & (data['timecode'] < time_end)& (data['id']== x)]#x == id  
    outer_json =  {
   "jsonarray": [],
    "labelarray":{"label":'',"labelString":'',"xlabelString":''}
    };       

    for i in range(len(temp_time)):
        inner_json = {
          "xs": "2020-02-03",
          "ys": 20
        }
        temp = temp_time.iloc[i]
        inner_json['xs'] = str(temp[7])# hardcoded time
        inner_json['ys'] = int(temp[dep_code])
        outer_json['jsonarray'].append(inner_json)
        
    outer_json['labelarray']['label'] = code_to_labels[dep_code][0]
    outer_json['labelarray']['labelString'] = code_to_labels[dep_code][1]
    outer_json['labelarray']['xlabelString'] = code_to_labels[dep_code][2]
    return outer_json

def get_plot_data_region(data,time_start,time_end,dep_code):
    temp_time = data[(data['timecode'] > time_start) & (data['timecode'] < time_end)] 
    outer_json =  {
   "jsonarray": [],
    "labelarray":{"label":'',"labelString":'',"xlabelString":''}
    };     

    for i in range(len(temp_time)):
        inner_json = {
          "xs": "2020-02-03",
          "ys": 20
        }
        temp = temp_time.iloc[i]
        inner_json['xs'] = str(temp[7])# hardcoded time
        inner_json['ys'] = float(np.round(temp[dep_code],3))# y value
        outer_json['jsonarray'].append(inner_json)
        
    outer_json['labelarray']['label'] = code_to_labels[dep_code][0]
    outer_json['labelarray']['labelString'] = code_to_labels[dep_code][1]
    outer_json['labelarray']['xlabelString'] = code_to_labels[dep_code][2]
    return outer_json

# for data.html visualisation
def get_data(data, time_start,time_end,x,dep_code):
    temp_time = data[(data['timecode'] > time_start) & (data['timecode'] < time_end)& (data['id']== x)]#x == id
    outer_json =  {
   "jsonarray": []
    };     

    for i in range(len(temp_time)):
        inner_json = {"id": 0, "I": 1.5, "U":3.1, "P":36, "T":1.2, "I_max":3.6, "U_max":36, "timecode": "2020-08-14-19:48"}
        temp = temp_time.iloc[i]
        col = temp_time.columns
        for j in range(len(temp_time.columns)-1):
            inner_json[col[j]] = int(temp[j])
        inner_json[col[7]] = str(temp[7])
        outer_json['jsonarray'].append(inner_json)
    return outer_json

def get_data_region(data,time_start,time_end):
    temp_time = data[(data['timecode'] > time_start) & (data['timecode'] < time_end)]
    outer_json =  {
   "jsonarray": []
    }; 

    for i in range(len(temp_time)):
        inner_json = {"id": 0, "I": 1.5, "U":3.1, "P":36, "T":1.2, "I_max":3.6, "U_max":36, "timecode": "2020-08-14-19:48"}
        temp = temp_time.iloc[i]
        col = temp_time.columns
        for j in range(len(temp_time.columns)):
            inner_json[col[j]] = temp[j]
        outer_json['jsonarray'].append(inner_json)
    return outer_json
#Get mean value for every hour of a day
code_to_labels2 = {1:['Суточная сила тока','I, A','Время, ч'],
                  2:["Суточное напряжение",'U, В','Время, ч'],
                  3:['Суточное потребление','P, КВт*час','Время, ч'],
                  4:['Суточная температура','T, °С','Время, ч'],
                  5:['Суточная max сила тока','I_max, A','Время, ч'],
                  6:['Суточное max напряжение','U_max, В','Время, ч'],
                 }
def get_mean(data,x,dep_code):
    outer_json =  {
   "jsonarray": [],
    "labelarray":{"label":'',"labelString":'',"xlabelString":''}
    };     
        
    temp = data[(data['id'] ==x)]
    temp_list = [[] for z in range(24)]
    times = [y for y in range(24)]
    for i in temp['timecode'].tolist():
        temp_list[int(i[11:13])].append(temp[temp['timecode']==i].iloc[0][dep_code])
    temp_list = [float(np.round(np.mean(temp_list[z]),3)) for z in range(len(temp_list))]
    for i in range(len(temp_list)):
        inner_json = {
          "xs": "2020-02-03",
          "ys": 20
        }
        inner_json['xs'] = int(times[i])
        inner_json['ys'] = temp_list[i]
        outer_json['jsonarray'].append(inner_json)

    outer_json['labelarray']['label'] = code_to_labels2[dep_code][0]
    outer_json['labelarray']['labelString'] = code_to_labels2[dep_code][1]
    outer_json['labelarray']['xlabelString'] = code_to_labels2[dep_code][2]
    return outer_json

def get_mean_region(data,dep_code):
    outer_json =  {
   "jsonarray": [],
    "labelarray":{"label":'',"labelString":'',"xlabelString":''}
    };     
        
    temp = data
    temp_list = [[] for z in range(24)]
    times = [y for y in range(24)]
    for i in temp['timecode'].tolist():
        temp_list[int(i[11:13])].append(temp[temp['timecode']==i].iloc[0][dep_code])
    temp_list = [float(np.round(np.mean(temp_list[z]),3)) for z in range(len(temp_list))]
    for i in range(len(temp_list)):
        inner_json = {
          "xs": "2020-02-03",
          "ys": 20
        }
        inner_json['xs'] = int(times[i])
        inner_json['ys'] = temp_list[i]
        outer_json['jsonarray'].append(inner_json)

    outer_json['labelarray']['label'] = code_to_labels2[dep_code][0]
    outer_json['labelarray']['labelString'] = code_to_labels2[dep_code][1]
    outer_json['labelarray']['xlabelString'] = code_to_labels2[dep_code][2]
    return outer_json

code_to_labels3 = {1:['Сила тока','I, A','Температура, °С'],
                  2:["Напряжение",'U, В','Температура, °С'],
                  3:['Потребление','P, КВт*час','Температура, °С'],
                  4:['Температура','T, °С','Температура, °С'],
                  5:['Max сила тока','I_max, A','Температура, °С'],
                  6:['Max напряжение','U_max, В','Температура, °С'],
                 }
def get_temperature(data,dep_code):
    outer_json =  {
   "jsonarray": [],
    "labelarray":{"label":'',"labelString":''}
    };   
    temperature = sorted(data['T'].unique().tolist())
    output = [[[],[]] for t in temperature]
    k = 0
    for t in temperature:
        output[k][0].append(t)
        temp = data[data['T'] == t]
        for i in range(len(temp)):
            temp_temp = temp.iloc[i]
            output[k][1].append(temp_temp[dep_code])
        k+=1
    for j in range(len(output)):
        inner_json = {
          "xs": "2020-02-03",
          "ys": 20
        }
        inner_json['xs'] = int(output[j][0][0])
        inner_json['ys'] = float(np.round(np.mean(output[j][1]),3))
        outer_json['jsonarray'].append(inner_json)
    outer_json['labelarray']['label'] = code_to_labels3[dep_code][0]
    outer_json['labelarray']['labelString'] = code_to_labels3[dep_code][1]
    outer_json['labelarray']['xlabelString'] = code_to_labels3[dep_code][2]
    return outer_json
def load_model():
    global model13 
    model13 = Sequential() # 
    model13.add(Dense(units = 20,activation='relu', input_dim = 20 ))
    model13.add(Dense(units = 20,activation='relu'))
    model13.add(Dense(units = 25,activation='relu'))
    model13.add(Dense(units = 25,activation='relu'))
    model13.add(Dense(units = 20,activation='relu'))
    model13.add(Dense(units = 4,activation='sigmoid'))
    model13.compile(loss='mean_squared_error',
                  optimizer=Adam(lr=0.0009))
    model13.summary()

    model13 = keras.models.load_model("model13((20)-20-20-25-25-20-Adam-lr00065).h5")
def predict(start_hour):
    start = datetime.datetime.strptime(data2[(data2['datetime'] == start_hour)].iloc[0][0],'%Y-%m-%d %H:%M:%S')
    temp_data = data2[(data2['datetime'] >= start_hour)&(data2['datetime'] <= datetime.datetime.strftime(start+ datetime.timedelta(hours = 5),'%Y-%m-%d %H:%M:%S'))]
    output = []
    for i in range(5):
        temp_temp = temp_data.iloc[i]
        output.append(datetime.datetime.strptime(str(temp_temp[0]),'%Y-%m-%d %H:%M:%S').hour)
        for x in range(1,4):
            output.append(temp_temp[x])
    return output
def normalise(pre_predict):
    codes = np.load('codes.npy').tolist()
    codes_for_codes = []
    
    for x in range(5):
        codes_for_codes.extend([i for i in range(1,5)])
    temp = []
    for i in range(len(pre_predict)):
        temp.append((pre_predict[i]-codes[codes_for_codes[i]][0])/(codes[codes_for_codes[i]][1]-codes[codes_for_codes[i]][0]))
    return temp
def unnormalize(predict):
    codes = np.load('codes.npy').tolist()
    temp = []
    for i in range(len(predict)):
        temp.append(predict[i]*(codes[i+1][1]-codes[i+1][0])+codes[i+1][0])
    return temp
def get_neural(time_start):
    load_model()
    outer_json ={"y":[],"x1":[],"x2":[]} 
    indx = data2[data2['datetime'] == time_start].index[0]
    times = []
    for x in range(indx,indx+24):
        temp_temp = data2.iloc[x]
        outer_json['x1'].append(int(temp_temp[3]))
        times.append(temp_temp[0])
    outer_json['y'].extend([int(time[11:13]) for time in times])
    outer_json['x2'].extend(outer_json['x1'][:5])
    for time in times[:-5]:
        outer_json['x2'].append(float(np.round(unnormalize(model13.predict(np.array([normalise(predict(time))]))[0])[3],2)))
    return outer_json
