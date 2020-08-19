import pandas as pd
data = pd.DataFrame(columns = ['id','I','U','P','T','I_max','U_max','timecode'])
data.to_csv('s_data.csv',index = None) 
