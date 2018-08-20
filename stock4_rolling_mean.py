import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def sym_to_path(symbol, base_dir ="./data"):
	return os.path.join(base_dir, "%s.csv"%(symbol))

def ReadCSV(symbol):
	print(sym_to_path(symbol))
	try:
		df = pd.read_csv(sym_to_path(symbol), index_col = "Date"
			,parse_dates = True, usecols = ['Date', "Adj Close", "Close"]
			,na_values=['nan'])
		return (df)
	except:
		return


def get_rolling_mean(df,rolling_window):
	print("1. Rolling Mean of Columns")
	#Calculate Rolling Mean
	df = pd.DataFrame(df.rolling(rolling_window).mean()) #Rolling Mean with 20days window
	df.columns = [df.columns[0]+"_RM"]
	return (df)

def get_rolling_std(df, rolling_window):
	print("2. Rolling std of Columns")
	df = pd.DataFrame(df.rolling(rolling_window).std()) #Rolling Mean with 20days window
	df.columns = [df.columns[0]+"_RSTD"]
	return (df)

def bollinger_band(df): # DF with first column = "Mean" and second column = std
	df["upper_band"] = df.iloc[:,1] + df.iloc[:,2]*2
	df["lower_band"] = df.iloc[:,1] - df.iloc[:,2]*2
	return (df)

def daily_return(df):
	lst = list(((df.iloc[:,0] / df.iloc[:,0].shift(1))-1))
	lst[0] = 0.0
	df["Daily_Return"] = lst
	return(df)
	
	    	

def plot_data(df, plot_title ):
	ax = df.plot(title=plot_title, fontsize=2)
	ax.set_xlabel("Date", fontsize=10)
	ax.set_ylabel("Close Price", fontsize=10)
	ax.legend(loc="lower right")
	ax.tick_params(axis='both', which='major',labelsize=7)
	ax.tick_params(axis='both', which='minor',labelsize=1)
	plt.show()

def createDF(startDate, endDate):
	dates = pd.date_range(startDate, endDate)
	df1 = pd.DataFrame(index=dates)
	return(df1)

def extract_stock_col(symbol):
	dfsym = ReadCSV(symbol)
	#print(dfsym)
	if dfsym is None:
		pass
	else:
		#Rename Columns
		dfsym.rename(columns={'Adj Close': symbol+"_AC",'Close':symbol+"_C"}, inplace=True)
		if symbol == "SPY":
			#Drop all the rows when SPY is NA Cell
			dfsym.dropna(subset=[symbol+"_AC", symbol+"_C" ])
	return (dfsym)

def combine_tbl(baseDF, stockDF):
	baseDF = baseDF.join(stockDF, how="inner")
	return(baseDF)

def normalize_data(df):
	return (df/df.ix[0,:])

def TestRun():
	
	startDate = "2017-08-01"
	endDate = " 2018-08-30"
	df1 = createDF(startDate, endDate)
	for sym in ["SPY","IBM","JJ","HCP","GOOG"]:
		#print("Max Close: %s %f"%(sym,get_max_close(sym)))
		#print("Mean Volume: %s %f"%(sym,get_mean_vol(sym)))
		#get_plot_high_low(sym)
		#get_plot_close(sym)
		#get_plot_high(sym)
		#print(ReadCSV(sym))
		dfsym = extract_stock_col(sym)
		if dfsym is not None:
			df1 = combine_tbl(df1, dfsym)
		else:
			pass
	
	df1.dropna(inplace=True)
	#Subset of DF based on input dates
	startDate = "2017-09-01"
	endDate = "2018-08-30"
	df1 = df1.ix[startDate : endDate,[ "SPY_C"]]#,"GOOG_C" , "IBM_C", "HCP_C"]]

	#Find the rolling Mean DF
	df_RM = get_rolling_mean(df1.SPY_C,20)

	#Find the rolling std DF
	df_STD = get_rolling_std(df1.SPY_C,20)
	
	#Combine Close Price and Rolling mean and Rolling std
	df1= combine_tbl(df1, df_RM)
	df1= combine_tbl(df1, df_STD)

	#Get the Bollinger Upper and Lower Band
	df1= bollinger_band(df1)
	
	#Get daily return
	df_DR = daily_return(df1)
	print(df_DR)

	#Plotting DF with Close Price, Rolling Mean, upper band and lower band
	
	plot_data(df1.iloc[:,[0,1,3,4]], "Close Price with Rolling Mean")

	#Plotting DF for Daily Return
	plot_data(df_DR.iloc[:,5], "Darily Return")	



	#Plot normalize data
	#df1 = normalize_data(df1)
	#plot_data(df1, "Normalized Close Price vs Date")		

if __name__ == "__main__":
	TestRun()