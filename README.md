# FSICdata

**I no longer maintain this package. I may, however, re-implement some features
in
[https://github.com/ChrisThoung/economic-data](https://github.com/ChrisThoung/economic-data)**

`FSICdata` is a Python package to provide tools to convert raw economic data to
common data formats. It provides data-processing tools to support macroeconomic
modelling using [FSIC](https://github.com/cthoung/fsic).

## Currently supported:

* [Eurostat](http://epp.eurostat.ec.europa.eu/portal/page/portal/eurostat/home/)
  [bulk download](http://epp.eurostat.ec.europa.eu/portal/page/portal/statistics/bulk_download):
	* tab-separated value (TSV) files

## Dependencies

### Required

* [pandas](http://pandas.pydata.org/):
  Version 0.14.1 or higher
	* See the `pandas` documentation for further dependencies
	  (`FSICdata` also uses [NumPy](http://www.numpy.org/) directly)
