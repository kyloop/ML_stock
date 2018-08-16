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

def get_max_close(symbol):
	df = ReadCSV(symbol)
	return(df.Close.max())

def get_mean_vol(symbol):
	df = ReadCSV(symbol)
	return(df.Volume.mean())

def get_plot_close(symbol):
	df = ReadCSV(symbol)
	df["Close"].plot()
	plt.show()

def get_plot_high(symbol):
	df = ReadCSV(symbol)
	df["High"].plot()
	plt.show()

def get_plot_high_low(symbol):
	df = ReadCSV(symbol)
	df[["Low","High"] ].plot()
	plt.show()

def plot_data(df, plot_title ):
	ax = df.plot(title=plot_title, fontsize=2)
	ax.set_xlabel("Date", fontsize=10)
	ax.set_ylabel("Close Price", fontsize=10)
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
	df1 = df1.ix[startDate : endDate,[ "SPY_C","GOOG_C" , "IBM_C", "HCP_C"]]
	#print(df1.ix[0,:])

	#Plot the data over time
	plot_data(df1, "Close Price vs Date")

	#Plot normalize data
	df1 = normalize_data(df1)
	plot_data(df1, "Normalized Close Price vs Date")		

if __name__ == "__main__":
	TestRun()