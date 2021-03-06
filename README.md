# msc_project
Code, functions and notebooks used for my Masters Project/Thesis.

### Some useful resources for -

#### data binning technique

- http://xarray.pydata.org/en/stable/user-guide/reshaping.html?highlight=stack#stack-and-unstack [READ THIS for refactoring]
- https://groups.google.com/g/xarray/c/fz7HHgpgwk0/m/h0umDBIHAAAJ [related to the link above]

- https://www.saedsayad.com/unsupervised_binning.htm
- https://www.statology.org/equal-frequency-binning-python/
- https://stackoverflow.com/questions/56485160/xarray-equivalent-of-pandas-qcut-function

#### Quantile-Regression

- The theory behind the pseudo R-squared is here - https://stats.stackexchange.com/questions/129200/r-squared-in-quantile-regression

#### Miscellaneous -

- https://scitools.org.uk/cartopy/docs/latest/gallery/lines_and_polygons/features.html?highlight=cfeatures#sphx-glr-download-gallery-lines-and-polygons-features-py (Cartopy features and coastlines)
- https://stats.stackexchange.com/questions/129200/r-squared-in-quantile-regression (**Local measure of goodness for quantreg**)
- https://towardsdatascience.com/calculating-confidence-interval-with-bootstrapping-872c657c058d (Bootstrap confidence interval calculation)

### TODO -

#### Priority

- [ ] Implementation of Dynamic and Thermodynamic Effects

- [ ] Inter-annual variability

- [ ] Precip-temp varying plot in regions of dipole behavior

- [ ] Complete winter season binning

- [x] Repeat the regridding using the `conservative` method which is recommended for upscaling using `xesmf` - The `conservative` method is not working so sticking to the `bilinear` method. The difference of the output is quite low.

#### If time available

- [ ] Implement quantile regression as an alternative regressor and also the ZM method from Ali 2018 paper and compare the time and results with the binning method. Link to the technique - click [here](https://www.statology.org/quantile-regression-in-python/) and [here](https://subramgo.github.io/2017/03/13/Quantile-Regression/) or using SKlearn. (NOT DOING)


- [ ] Figure out the use of finding Block maxima and Climate change Indices - Resources -'
  https://search.brave.com/search?q=calculate+block+maxima+python&source=desktop
  https://pypi.org/project/evt/
  https://kikocorreoso.github.io/scikit-extremes/index.html
  http://etccdi.pacificclimate.org/list_27_indices.shtml
  https://search.brave.com/search?q=calculation+of+climate+change+indices&source=desktop
