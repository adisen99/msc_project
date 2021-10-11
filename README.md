# msc_project
Code, functions and notebooks used for my Masters Project/Thesis.

### Some usefule  resources for data binning technique -

- http://xarray.pydata.org/en/stable/user-guide/reshaping.html?highlight=stack#stack-and-unstack [READ THIS for refactoring]
- https://groups.google.com/g/xarray/c/fz7HHgpgwk0/m/h0umDBIHAAAJ [related to the link above]

- https://www.saedsayad.com/unsupervised_binning.htm
- https://www.statology.org/equal-frequency-binning-python/
- https://stackoverflow.com/questions/56485160/xarray-equivalent-of-pandas-qcut-function

### TODO -

- [ ] Fix the stippling for the plots - CHECK THIS link - https://stackoverflow.com/questions/46803626/fix-location-of-stippling-for-subplots
- [ ] Implement quantile regression as an alternative regressor and compare the time and results with the binning method. Link to the technique - [click here](https://www.statology.org/quantile-regression-in-python/)
- [ ] Refactor the binning for 3d plotting
- [x] Get slope and significance of the fit
- [x] Take the precipitation cutoff using mm/day rather than mm/hr i.e. use a forward/backward running sum. (Ask- should I use precipitation daily rate for the bining or use `mm/hr` for binning and keep `mm/day` values only for selecting the cut-off)
- [x] Bin temperature data and take 99th and 50th percentile of precipitation.
- [x] Bin the temperature data such that the precipitation has same frequency in each bin.
- [x] Get the slope of the final plot.
- [x] Find a way to present this for a lat-lon plot.
