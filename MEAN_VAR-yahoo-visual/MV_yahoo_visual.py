# Note:
#
# When making edits, please adhere to PEP8 style guidelines and avoid
# exceeding 75 characters in one line.
#

import sys
import numpy as np
import pandas as pd

#
# Importing bokeh functions
#
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool

#
# Samples
#
samp1 = {'AAPL': 0.02, 'GOOG': 0.01}
samp2 = {'HBIO': 0.0013, 'IBM': 0.001}
samp3 = {'MSFT': 0.0019, 'MTU': 0.0005}
samp4 = {'AAPL': 0.00101, 'GOOG': 0.0002, 'HBIO': 0.0015, 'IBM': 0.007}
samp5 = {'AAPL': 0.00101, 'GOOG': 0.0005, 'HBIO': 0.0015,
	'IBM': 0.007, 'MSFT': 0.0002, 'MTU': 0.004}

#
# The sensitivity refers to the iteration value of the expected return
# when optimizing for variance. A value of 0.0005 is typically appropriate
#
def modern_show(inputDict, period, sensitivity):
	"""Takes a dictionary, and int period. Returns weights.

	The input dictionary should map the string Equity keys to a float 
	expected return value over `period` time
	"""
	
	#
	# Error Testing inputs
	#
	try:
		if not inputDict:
			raise ValueError("No dictionary found.")
		if not period:
			raise ValueError("No time period found.")
		if not sensitivity:
			raise ValueError("No sensitivity found.")
		
		if type(period) is not int:
			raise ValueError("Time period not of type int")
		if type(inputDict) is not dict:
			raise ValueError("Input not dictionary.")
		if type(sensitivity) is not float:
			raise ValueError("Sensitivity not of type float")
		
		inputKeys = inputDict.keys()
		inputValues = inputDict.values()
		
		if not inputKeys:
			raise ValueError("Input is dictionary. Keys are empty")
		if not inputValues:
			raise ValueError("Input is dictionary. Values are empty")
		if type(inputValues[0]) is not float:
			raise ValueError("Input is dictionary. Values are not of type"
			" float")
		if type(inputKeys[0]) is not str:
			raise ValueError("Input is dictionary. Keys are not of type"
			" str")
		
	except ValueError as err:
		print(err)
		print ("Now returning to Console...")
		sys.exit(1)
	except:
		print("Unknown error occurred")
		print ("Now returning to Console...")
		sys.exit(1)
	
	
	assets = pd.DataFrame()
	recent_close = []
	
	#
	# Imports the data from the .csv files listed in the dictionary keys.
	# It only imports the `Date` once and imports `Close` data from 
	# additional files into subsequent columns
	#
	# For example, for a key 'PZZA', its close data is imported under the 
	# column title 'PZZA' in the DataFrame `assets`
	#
	FIRST_READ = True
	for key in inputDict.keys():
		asset = key + '.csv'
		asset = str(asset)
		if FIRST_READ:
			assets = assets.append(pd.read_csv(asset, usecols = ['Date',
			'Close'], header = 0))
			column_names = ['Date', asset.replace('.csv', '')]
			assets.columns = column_names
			FIRST_READ = False
		else:
			column_names.append(asset.replace('.csv', ''))
			assets = pd.concat([assets, pd.read_csv(asset, 
			usecols = ['Close'], header = 0)], axis = 1)
			assets.columns = column_names
		recent_close.append(assets.get_value(assets.shape[0]-1, 
			asset.replace('.csv', '')))
	
	#
	# Calculates the daily returns from the previously derived `assets`
	# DataFrame. It then imports the daily returns for an asset `KEY`
	# to the column `KEY Return` in `assets`. The `KEY` column holding
	# daily close prices is then deleted. The `Date` data should be 
	# ordered from OLDEST TO NEWEST with the most recent date being 
	# in the last row.
	#
	# At the end of the loop, `assets` contains only the `Date` column 
	# and columns of daily returns for each equity. 
	#
	# The covariance matrix can be calculated from this DataFrame since 
	# the `Date` column is ignored in the calculation
	#
	for asset in inputDict.keys():
		dummy_array = []
		for i in list(reversed(range(assets.shape[0]-1))):
			rdiff = (assets.get_value(assets.shape[0]-1-i, asset)-
				assets.get_value(assets.shape[0]-2-i, asset))
			daily_return = rdiff / assets.get_value(assets.shape[0]-2-i, 
				asset)
			dummy_array.append(daily_return)
		dummy_dict = {asset + ' Return': dummy_array}
		dummy_DF = pd.DataFrame(dummy_dict)
		assets[asset + ' Return'] = dummy_DF[asset + ' Return']
		del assets[asset]
	
	#
	# Since the new DataFrame has `assets.shape[0]-1` rows, we calculate
	# the covariance matrix with an offset of 1. It is calculated over 
	# time `period`
	#
	cov_matrix = assets[assets.shape[0]-1-period:assets.shape[0]-1].cov()
	
	#
	# Creating the ones vector, covariance matrix, and vector of returns
	# respectively within the numpy framework.
	#
	iota = np.ones((len(inputDict.keys()), 1), int)
	sigma = cov_matrix.as_matrix()
	mu = np.array(inputDict.values()).reshape((len(inputDict.values()), 1))
	
	#
	# Computing constants
	#
	A = np.matmul(np.matmul(iota.transpose(), np.linalg.inv(sigma)), 
		iota)[0,0]
	B = np.matmul(np.matmul(iota.transpose(), np.linalg.inv(sigma)), 
		mu)[0,0]
	C = np.matmul(np.matmul(mu.transpose(), np.linalg.inv(sigma)), 
		mu)[0,0]

	G = np.matmul(np.linalg.inv(sigma), C*iota -B*mu)*(1/(A*C-B**2))
	H = np.matmul(np.linalg.inv(sigma), A*mu - B*iota)*(1/(A*C-B**2))
	
	#
	# Initializing lists to hold data to later be graphed
	#
	exp_rets_p = []
	var_p = []
	weight_p = []
	
	expected_return_p = 0.1
	exp_rets_p.append(expected_return_p)
	
	weight_vector_old = G + H*expected_return_p
	weight_p.append(weight_vector_old)
	
	variance_old = np.matmul(np.matmul(weight_vector_old.transpose(), 
		sigma), weight_vector_old)
	var_p.append(variance_old)
	
	expected_return_p = 0.1 - sensitivity
	exp_rets_p.append(expected_return_p)
	
	#
	# Searching for the global minimum variance portfolio by iterating
	# the expected portfolio return by `sensitivity` until the newly calculated
	# variance is less than the one calculated by the previous expected
	# return.
	#
	while(expected_return_p > 0):
		weight_vector = G + H*expected_return_p
		variance = np.matmul(np.matmul(weight_vector.transpose(), 
			sigma), weight_vector)
		if (variance > variance_old):
			exp_rets_p.remove(expected_return_p)
			
			expected_return_p = expected_return_p + sensitivity
			variance = variance_old
			weight_vector = weight_vector_old
			break
		else:
			variance_old = variance
			var_p.append(variance_old)
			
			weight_vector_old = weight_vector
			weight_p.append(weight_vector_old)
			
			expected_return_p = expected_return_p - sensitivity
			exp_rets_p.append(expected_return_p)
			
	#
	# If the `while` loop was broken and the `expected_return_p` is 
	# zero, then we remove that expected return value from the list 
	# of weights.
	#
	if (expected_return_p < 0):
		exp_rets_p.remove(expected_return_p)
	
	#
	# Calculating the Standard Deviation
	#
	std_dev_p = []
	for i in range(len(var_p)):
		std_dev_p.append((var_p[i][0][0])**2)
	
	#
	# Converting the weight list from one of ndarrays to one of strings, 
	# held in `weight_p_f`
	#
	j = 0
	weight_p_f = []
	while (j < len(weight_p)):
		placeholder = ""
		i = 0
		for key in inputDict.keys():
			placeholder = (placeholder + key + ' : ' + 
				str(weight_p[j][i][0]) + ' ')
			i = i + 1
		j = j + 1
		weight_p_f.append(placeholder)
	
	#
	# Finding the index when the weight of any asset exceeds 1. This is
	# done to adjust the  bokeh graph
	#
	j = 1
	weight_limit = 0
	while (j > 0):
		for j in list(reversed(range(len(weight_p)))):
			for i in range(len(inputDict.keys())):
				if (weight_p[j][i][0] > 1):
					weight_limit =  j
					j = -1
					break
			if (j < 0):
				break
	
	#
	# Outputting an `.html` with bokeh embedded
	#
	output_file("MPT_Graph.html", mode="inline")
	
	#
	# Initializing the data source
	#
	source = ColumnDataSource(
		dict(x = std_dev_p, 
		y = exp_rets_p, 
		desc = weight_p_f)
		)
	
	#
	# Hover options
	#
	hover = HoverTool(tooltips = [("(x,y)", "(@x, @y)"), 
		("desc", "@desc"),])
	
	#
	# Defining the plot and its axes
	#
	fig = figure(tools = [hover], 
		title="Portfolio Graph",
		x_range = [0, std_dev_p[weight_limit]],
		y_range = [0, exp_rets_p[weight_limit]]
		)
	
	#
	# Display preferences
	#
	fig.circle('x', 'y', size = 10, source=source)
	fig.xaxis.axis_label = "Standard Deviation (Risk)"
	fig.yaxis.axis_label = "Expected Return"
	
	show(fig)