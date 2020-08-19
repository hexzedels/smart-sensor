import pandas as pd
data = pd.DataFrame(columns = ['id','current','voltage','temp','max_current','max_voltage','timecode'])
data.to_csv('s_data.csv',index = None) 
