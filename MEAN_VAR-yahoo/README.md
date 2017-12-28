## Purpose

The Python module intakes a dictionary mapping string asset keys to float expected returns. It also takes a time-period for determining the covariance matrix and it takes a `sensitivity` variable that determines the amount of expected returns to be optimized (a value of `0.0005` or lower is appropriate). If the `sensitivity` is lower, then it might take longer to process.

It returns the global minimum variance portfolio's values.

### Constraints

The `csv` files must be the unmodified historical information files obtains from Yahoo Finance. The timeframes for all of the equities' historical data must be the **same**.

For an example, see the sample folder found in the root repository. 

## Troubleshooting

* Make sure your `csv` files are unmodified and occur over the same time-period. Some assets may be newer than others!
* If you receive weird values, then your covariance matrix may not be invertible.
