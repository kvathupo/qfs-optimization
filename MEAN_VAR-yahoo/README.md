## Purpose

The Python module intakes a dictionary mapping string asset keys to float expected returns. It also takes a time-period for determining the covariance matrix and it takes a, now unimplemented, initial capital value.

### Constraints

The `csv` files must be the unmodified historical information files obtains from Yahoo Finance. The timeframes for all of the equities' historical data must be the **same**.

For an example, see the example folder found in the root repository. 

## Completed

The function now returns a dictionary describing the optimal weights for the global minimum variance portfolio (GMVP), and the portfolio's expected return and variance (risk). The weights are given in decimal form as a percentage of the initial capital. 

Future implementations hope to return integer shares, as opposed to percentages that can lead to holding fractions of assets (impossible!).

## To Do

Add a visual representation of the graphed portfolios with the `Bokeh` module. Apply linear integer programming algorithms to determine all possible configurations for the GMVP in terms of integer number of shares, as opposed to percentage of initial capital.
