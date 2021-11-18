import pandas as pd

def writeConfig():
	# values = pd.DataFrame({"user_name":["dasith"],"password":["1234"],"user_type":["staff"],"privilege_level":[2]})
	config = pd.read_csv('./config/configuration.csv')
	config.loc[config.shape[0]] = ['dasith','1234','staff',2]
	config.to_csv('./config/configuration.csv',index=False)
	

writeConfig()