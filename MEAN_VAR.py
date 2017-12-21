def modern_optimize(input):
    """Takes a dictionary and returns weights.
    The input dictionary should map the integer SID keys to a float 
    ROI (return on investment) value
    """
    try:
        if type(input) is not dict:
           raise ValueError("Input not dictionary")
        inputKeys = input.keys()
        inputValues = input.values()
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
    pass