import pandas as pd

regions_cities = {
    0: ['Город'],
    50: ['Москва', 'Долгопрудный', 'Подольск', 'Химки', 'Люберцы'],
    47: ['Санкт-Петербург', 'Кудрово', 'Выборг', 'Гатчина', 'Всеволжск'],
    16: ['Казань', 'Тетюши', 'Елабуга', 'Нижнекамск', 'Набережные Челны'],
    69: ['Тверь', 'Калязин', 'Ржев', 'Осташков', 'Торжок'],
    33: ['Владимир', 'Ковров', 'Муром', 'Суздаль', 'Гороховец']
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

