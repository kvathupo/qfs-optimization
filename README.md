## Quick Overview
Purpose:

This repository serves as a partial record of work done as a member of the University of Maryland's Quantitative Finance Society. Specifically, this repository is concerned with developing user-friendly portfolio optimization functions for use in Quantopian.

Language:

Python 2.7.13

Modules:

NumPy, pandas, bokeh, sys

## Current Developments
Writing three separate functions that interface with Quantopian and Yahoo Finance respectively. For the former, the function can simply be copy-pasted into Quantopian for functionality; for the latter, the function will be imported as a module to the Python interpreter. Further information:

`./MEAN_VAR-quant`:

The Quantopian function is in the woodworks.

`./MEAN_VAR-yahoo`:

The Yahoo Finance function returns information on the **global minimum variance portfolio** to be constructed in the form of a dictionary with each asset's weight and the portfolio's variance and expected return.

`./MEAN_VAR-yahoo-visual`:

The Yahoo Finance visual function returns a `html` file (that is automatically opens) that graphs the set of feasible potrfolios based on their standard deviation and expected return. It is interactive and individual dots can be hovered over for information.

## Future Developments
`./MEAN_VAR-quant`:

Writing a function that returns a dictionary with all the feasible weights for any given variance and expected ROI.

`./MEAN_VAR-yahoo` and `./MEAN_VAR-yahoo-visual`:

Applying linear integer programming to determine the integer number of shares to be allocated, as opposed to percentages of capital, which can result in fractional shares.

## How Can I See a Demonstration?
Consult the READMEs in either `./MEAN_VAR-yahoo-sample` or `./MEAN_VAR-yahoo-visual`.

## External Links
  * https://www.umdqfs.com/
  * https://www.quantopian.com/
  * https://finance.yahoo.com/
