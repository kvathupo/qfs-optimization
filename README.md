## Quick Overview
Purpose:

This repository serves as a partial record of work done as a member of the University of Maryland's Quantitative Finance Society. Specifically, this repository is concerned with developing user-friendly portfolio optimization functions for use in Quantopian.

Language:

Python 2.7.13

## Current Developments
Writing two separate functions that interface with Quantopian and Yahoo Finance respectively. For the former, the function will simply be copy-pasted; for the latter, the function will be imported as a module to the Python interpreter.

The Quantopian function should intake a dictionary of `sid` keys mapped to Return on Investment (ROI) values along with a period, and the `data` and `context` arguments.

The Yahoo Finance function intakes a integer time-period, and dictionary that maps string equity keys to ROI float values. The strings are then used to return a DataFrame containing all the raw data of the locally downloaded `csv` files for the specified equities.

## Future Developments
For both implementations, writing a function that returns a dictionary with all the feasible weights for any given variance and expected ROI. Implementing an interactive graph of the feasible portfolios; ideally, this graph's data can be exported.

## External Links
  * https://www.quantopian.com/
  * https://www.umdqfs.com/
