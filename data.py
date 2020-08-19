import pandas as pd
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
