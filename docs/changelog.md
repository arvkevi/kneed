# Changelog

## 0.8.6 (2026-03-20)

- Fixed knee detection to pause after local minima per the Kneedle algorithm specification
- Migrated documentation from Sphinx to MkDocs Material with dark mode and improved search
- Added new documentation: getting started guide, curve types reference, multi-knee detection, `find_shape()` guide, troubleshooting, and real-world examples (K-means, PCA)
- Converted docstrings from Sphinx to NumPy style and fixed type errors (`online` was documented as `str` instead of `bool`, `S` as `integer` instead of `float`)
- Updated Python support: dropped 3.5-3.7, added 3.12 to CI matrix
- Updated project classifier from "Alpha" to "Production/Stable"
- Added changelog to documentation

## 0.8.5 (2023-07-08)

- Removed all warnings when no knees are found — `knee` simply returns `None`

## 0.8.4 (2023-07-08)

- No longer warns when no knee/elbow is found (graceful `None` return)
- Updated ReadTheDocs configuration

## 0.8.3 (2023-04-27)

- Added Python 3.11 to CI test matrix
- Added Codecov token for reliable coverage uploads
- Removed unused MANIFEST file (using hatch build system)

## 0.8.2 (2023-01-08)

- Migrated to hatch build system
- Added customizable `title`, `xlabel`, and `ylabel` parameters to `plot_knee()` and `plot_knee_normalized()`
- Improved test coverage for no-matplotlib environments

## 0.8.1 (2022-07-30)

- Fixed error reading VERSION file from the package distribution

## 0.8.0 (2022-07-30)

- Made matplotlib an optional dependency — install with `pip install kneed[plot]`
- Dropped Python 3.6 support
- Added Python 3.10 to CI test matrix
- Migrated from Travis CI to GitHub Actions

## 0.7.0 (2020-08-12)

- Added `polynomial_degree` parameter for controlling polynomial fit degree
- Added Sphinx documentation hosted on ReadTheDocs
- Added `interp_method="polynomial"` option
- Updated type hints

## 0.6.0 (2020-03-05)

- Fixed `IndexError` when no knee is found — now returns `None` gracefully

## 0.5.2 (2020-02-12)

- Added `knee_y` and `norm_knee_y` attributes to expose y values at knee point
- Added type hints throughout
- Added optional `figsize` parameter to plotting methods

## 0.5.1 (2019-11-27)

- Fixed knee detection when the difference curve has a flat maximum

## 0.5.0 (2019-10-01)

- Implemented online and offline detection modes
- Fixed variable naming: "distance" curve renamed to "difference" curve

## 0.4.0 (2019-07-06)

- Major refactoring of `KneeLocator` class for improved readability
- Added `all_knees`, `all_elbows` collections for multi-knee detection
- Added sensitivity parameter (`S`) documentation and examples
