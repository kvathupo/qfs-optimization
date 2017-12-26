## Quick Overview
Purpose:

This repository serves as a partial record of work done as a member of the University of Maryland's Quantitative Finance Society. Specifically, this repository is concerned with developing user-friendly portfolio optimization functions for use in Quantopian.

Language:

Python 2.7.13

Modules:

NumPy, pandas, sys

## Current Developments
Writing two separate functions that interface with Quantopian and Yahoo Finance respectively. For the former, the function will simply be copy-pasted; for the latter, the function will be imported as a module to the Python interpreter.

The Quantopian function should intake a dictionary of `sid` keys mapped to Return on Investment (ROI) values along with a period, and the `data` and `context` arguments.

The Yahoo Finance function intakes a integer time-period, a float initial capital, and a dictionary that maps string equity keys to float expected return values over the same time-period. The function returns information on the **global minimum variance portfolio** to be constructed in the form of a dictionary with each asset's weight and the portfolio's variance and expected return.

## Future Developments
For the Quantopian implementation, writing a function that returns a dictionary with all the feasible weights for any given variance and expected ROI. For the Yahoo Finance function, implementing an interactive graph of the feasible portfolios; ideally, this graph's data can be exported. See each respective folder for more details.

## How Can I See a Demonstration?
Consult the README in `./MEAN_VAR-yahoo-sample`.

## External Links
  * https://www.umdqfs.com/
  * https://www.quantopian.com/
  * https://finance.yahoo.com/
