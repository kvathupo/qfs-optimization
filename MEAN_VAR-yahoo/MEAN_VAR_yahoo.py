# The sample yahoo csv's are from 01-01-2005 to 01-01-2015

import sys
import numpy as np
import pandas as pd

# Used for test purposes
test = {'HBIO': 0.02, 'PZZA': 0.01}

def modern_optimize(inputDict, period, capital):
	"""Takes a dictionary, and int period. Returns weights.

	The input dictionary should map the string Equity keys to a float 
	expected return value over `period` time
	"""
	try:
		if not inputDict:
			raise ValueError("No dictionary found.")
		if not period:
			raise ValueError("No time period found.")
		if not capital:
			raise ValueError("No initial capital found.")
		
		if type(period) is not int:
			raise ValueError("Time period not of type int")
		if type(inputDict) is not dict:
			raise ValueError("Input not dictionary.")
		if (type(capital) is not int) and (type(capital) is not float):
			raise ValueError("Capital neither integer nor float")
		
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
			" int")
		
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
	
	# TO DO: Fix the ugly `i` work-around
	#
	# The first `for` loop imports the data from the .csv files listed in 
	# the dictionary keys. It only imports the `Date` once and imports 
	# `Close` data from subsequent files into subsequent columns
	#
	# For example, for a key 'PZZA', its close data is imported under the 
	# column title 'PZZA' in the DataFrame `assets`
	#
	i = 0
	for key in inputDict.keys():
		asset = key + '.csv'
		asset = str(asset)
		if (i == 0):
			assets = assets.append(pd.read_csv(asset, usecols = ['Date',
			'Close'], header = 0))
			column_names = ['Date', asset.replace('.csv', '')]
			assets.columns = column_names
		else:
			column_names.append(asset.replace('.csv', ''))
			assets = pd.concat([assets, pd.read_csv(asset, 
			usecols = ['Close'], header = 0)], axis = 1)
			assets.columns = column_names
		recent_close.append(assets.get_value(assets.shape[0]-1, asset.replace('.csv', '')))
		i = i + 1
	
	#
	# The `for` loop calculates the daily returns from the previously derived
	# `assets` DataFrame. It then imports the daily returns for an asset `KEY`
	# to the column `KEY Return` in `assets`. The `KEY` column holding daily
	# close prices is then deleted. The `Date` data should be ordered from 
	# OLDEST TO NEWEST with the most recent date being in the last row.
	#
	# At the end of the loop, `assets` contains only the `Date` column and columns
	# of daily returns for each equity. 
	#
	# It is fine to determine the covariance matrix from this DataFrame since 
	# the `Date` column is ignored in the calculation
	#
	for asset in inputDict.keys():
		dummy_array = []
		for i in list(reversed(range(assets.shape[0]-1))):
			rdiff = assets.get_value(assets.shape[0]-1-i, asset)-assets.get_value(assets.shape[0]-2-i, asset)
			daily_return = rdiff / assets.get_value(assets.shape[0]-2-i, asset)
			dummy_array.append(daily_return)
		dummy_dict = {asset + ' Return': dummy_array}
		dummy_DF = pd.DataFrame(dummy_dict)
		assets[asset + ' Return'] = dummy_DF[asset + ' Return']
		del assets[asset]
	
	#
	# Since the new DataFrame has `assets.shape[0]-1` rows, we calculate
	# the covariance matrix with an offset of 1
	#
	cov_matrix = assets[assets.shape[0]-1-period:assets.shape[0]-1].cov()
	
	#
	# The following block of code maps asset strings to the most recent close
	#
	# TO DO: Add implementation for returning feasible weights
	#
	asset_list = []
	for asset in inputDict.keys():
		asset_list.append(asset)
	recent_close_dict = dict(zip(asset_list, recent_close))
	
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
	A = np.matmul(np.matmul(iota.transpose(), np.linalg.inv(sigma)), iota)[0,0]
	B = np.matmul(np.matmul(iota.transpose(), np.linalg.inv(sigma)), mu)[0,0]
	C = np.matmul(np.matmul(mu.transpose(), np.linalg.inv(sigma)), mu)[0,0]

	G = np.matmul(np.linalg.inv(sigma), C*iota -B*mu)*(1/(A*C-B**2))
	H = np.matmul(np.linalg.inv(sigma), A*mu - B*iota)*(1/(A*C-B**2))
	
	#
	# Searching for the global minimum variance portfolio
	#
	expected_return_p = 0.1
	weight_vector_old = G + H*expected_return_p
	variance_old = np.matmul(np.matmul(weight_vector_old.transpose(), sigma), weight_vector_old)
	expected_return_p = 0.0995
	while(expected_return_p > 0):
		weight_vector = G + H*expected_return_p
		variance = np.matmul(np.matmul(weight_vector.transpose(), sigma), weight_vector)
		if (variance > variance_old):
			expected_return_p = expected_return_p + 0.0005
			variance = variance_old
			weight_vector = weight_vector_old
			break
		else:
			variance_old = variance
			weight_vector_old = weight_vector
			expected_return_p = expected_return_p - 0.0005
	if (expected_return_p < 0):
		expected_return_p = expected_return_p + 0.0005
	
	#
	# Denesting the converted list of weights
	#
	weight_list = []
	for i in range(len(weight_vector.tolist())):
		weight_list.append(weight_vector.tolist()[i][0])
	
	weight_list.extend([variance[0][0], expected_return_p])
	descrip = asset_list
	descrip.extend(['variance', 'expected return'])
	
	GMVP = dict(zip(descrip, weight_list))
	
	return GMVP