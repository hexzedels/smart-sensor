import pandas as pd
import numpy as np
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
