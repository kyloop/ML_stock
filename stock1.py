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

def combine(startDate, endDate):
	dates = pd.date_range(startDate, endDate)
	df1 = pd.DataFrame(index=dates)
	return(df1)


def TestRun():
	startDate = "2017-08-16"
	endDate = " 2018-06-30"
	df1 = combine(startDate, endDate)
	for sym in ["SPY","IBM","JJ","HCP"]:
		#print("Max Close: %s %f"%(sym,get_max_close(sym)))
		#print("Mean Volume: %s %f"%(sym,get_mean_vol(sym)))
		#get_plot_high_low(sym)
		#get_plot_close(sym)
		#get_plot_high(sym)
		#print(ReadCSV(sym))
		dfsym = ReadCSV(sym)
		#print(dfsym)
		if dfsym is None:
			pass
		else:
			#Rename Columns
			dfsym.rename(columns={'Adj Close': sym+"_AC",'Close':sym+"_C"}, inplace=True)
			if sym== "SPY":
				#Drop all the rows when SPY is NA Cell
				dfsym.dropna(subset=[sym+"_AC", sym+"_C" ])

			df1 = df1.join(dfsym, how="inner"	)
	
	df1.dropna(inplace=True)

	print(df1.shape)
		

if __name__ == "__main__":
	TestRun()