torsiondrive-on-steroids 💊 💪
==============================
[![Travis Build Status](https://travis-ci.org/lpwgroup/torsiondrive.svg?branch=master)](https://travis-ci.org/lpwgroup/torsiondrive)
[![codecov](https://codecov.io/gh/lpwgroup/torsiondrive/branch/master/graph/badge.svg)](https://codecov.io/gh/lpwgroup/torsiondrive/branch/master)
[![Documentation Status](https://readthedocs.org/projects/torsiondrive/badge/?version=latest)](https://torsiondrive.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/123762164.svg)](https://zenodo.org/badge/latestdoi/123762164)

A modded version of [TorsionDrive](https://github.com/lpwgroup/torsiondrive/tree/master/torsiondrive) from [LPWGROUP](https://github.com/lpwgroup). Unfortunately, the development of the original library seems to be abandoned. I will implement here some useful new functionalities and happily merge them back in the original repository if needed!

Dihedral scanner with wavefront propagation. Please see the [Documentation](https://torsiondrive.readthedocs.io/) for more information.

#### Functionalities under development
 * Orca engine integration, at least with '--native-opt'
 * Make SPE calculation failures (e.g. SCF does not converge) non stopping
 * Native, embarassingly easy parallelization with the [jobdispatcher](https://github.com/mattiafelice-palermo/job-dispatcher) library

#### Funding Information

The development of this code has been supported in part by the following grants and awards:

NIH Grant R01 AI130684-02

ACS-PRF 58158-DNI6
