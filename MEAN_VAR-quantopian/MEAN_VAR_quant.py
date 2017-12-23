def modern_optimize(inputDict, period, data, context):
	"""Takes a dictionary and period. Returns weights.

	The input dictionary should map the SID keys to a float 
	ROI (return on investment) value.
	"""
	try:
		if not inputDict:
			raise ValueError("No dictionary found.")
		if not period:
			raise ValueError("No time period found.")
		if type(period) is not int:
			raise ValueError("Time period not of type int")
		if type(inputDict) is not dict:
			raise ValueError("Input not dictionary.")

		inputKeys = inputDict.keys()
		inputValues = inputDict.values()

		if not inputKeys:
			raise ValueError("Input is dictionary. Keys are empty")
		if not inputValues:
			raise ValueError("Input is dictionary. Values are empty")
		if type(inputValues[0]) is not float:
			raise ValueError("Input is dictionary. Values are not of type"
			" float")
		if type(inputKeys[0]) is not int:
			raise ValueError("Input is dictionary. Keys are not of type"
			" int")
	except ValueError as err:
		print err
	except:
		print("Unknown error occurred")
	
	inputKeys = inputDict.keys()
	inputValues = inputDict.values()
	for key in inputKeys:
		context.var_calc1 = data.history(key, "price", bar_count = period, frequency = "1d")