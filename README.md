# pydra-tasks-fsl

[![PyPI - Version][pypi-version]][pypi-project]
[![PyPI - Python Version][pypi-pyversions]][pypi-project]
[![PyPI - Downloads][pypi-downloads]][pypi-project]
[![Status-docs][status-docs-badge]][status-docs-link]
[![Status-CICD][status-cicd-badge]][status-cicd-link]

----

Pydra tasks for FSL.

[Pydra][pydra] is a dataflow engine which provides
a set of lightweight abstractions for DAG
construction, manipulation, and distributed execution.

[FSL][fsl] is a comprehensive library of analysis tools
for FMRI, MRI and DTI brain imaging data.

**Table of contents**

- [Available tasks](#available-tasks)
- [Installation](#installation)
- [Development](#development)
- [License](#license)

## Tested interfaces

| Module | Tasks                                                                                                              |
|--------|--------------------------------------------------------------------------------------------------------------------|
| bet    | BET, RobustFOV                                                                                                     |
| eddy   | Eddy, ApplyTopup, Topup                                                                                            |
| fast   | FAST                                                                                                               |
| flirt  | FLIRT, ApplyXFM, ConcatXFM, ConvertXFM, InvertXFM, FixScaleSkew, Img2ImgCoord, Img2StdCoord, Std2ImgCoord          |
| fnirt  | FNIRT, FNIRTFileUtils, ApplyWarp, ConvertWarp, InvWarp                                                             |
| fugue  | FUGUE, PrepareFieldmap, Prelude, SigLoss                                                                           |
| maths  | (**experimental**) Maths, Mul                                                                                      |
| susan  | SUSAN                                                                                                              |
| utils  | ChFileType, FFT, Info, Interleave, Merge, Orient, Reorient2Std, ROI, SelectVols, Slice, SmoothFill, Split, SwapDim |

## Installation

```console
pip install pydra-tasks-fsl
```

A separate installation of FSL is required to use this package.
Please review the FSL [installation instructions][fsl-install]
and [licensing details][fsl-license].


## Automatic Conversion

Automatically generated tasks can be found in the `pydra.tasks.fsl.auto` sub-package.
These interfaces should be treated with caution as they likely do not pass testing.
Generated tasks that have been edited and pass testing will be imported into one or more of the
`pydra.tasks.fsl.v*` sub-packages (e.g. `pydra.tasks.fsl.v7_4`) corresponding
to the version of the fsl toolkit they are designed for.


### Continuous integration

This template uses [GitHub Actions](https://docs.github.com/en/actions/) to run tests and
deploy packages to PYPI. New packages are built and uploaded when releases are created on
GitHub, or new releases of Nipype or the Nipype2Pydra conversion tool are released.
Releases triggered by updates to Nipype or Nipype2Pydra are signified by the `postN`
suffix where `N = <nipype-version><nipype2pydra-version>` with the '.'s stripped, e.g.
`v0.2.3post185010` corresponds to the v0.2.3 tag of this repository with auto-generated
packages from Nipype 1.8.5 using Nipype2Pydra 0.1.0.

## Development

### Methodology

The development of this package is expected to have two phases

1. Where the corresponding Nipype interfaces are considered to be the ground truth, and
   the Pydra tasks are generated from them
2. When the Pydra tasks are considered be mature and they are edited by hand

Different tasks will probably mature at different times so there will probably be an
intermediate phase between 1 and 2.

### Developer installation

Before the pydra task interfaces can be generated and installed, the file-format classes
[fileformats](https://arcanaframework.github.io/fileformats/) packages
corresponding to FSL specific file formats will need to be installed

```console
pip install -e ./related-packages/fileformats[dev]
pip install -e ./related-packages/fileformats-extras[dev]
```

Next install the requirements for running the auto-conversion script and generate the
Pydra task interfaces from their Nipype counterparts

```console
pip install -r nipype-auto-conv/requirements.txt
```

The run the conversion script to convert Nipype interfaces to Pydra

```console
nipype-auto-conv/generate
```

Install repo in developer mode from the source directory and install pre-commit to
ensure consistent code-style and quality.

```console
pip install -e .[test,dev]
pre-commit install
```

### Auto-conversion phase

The auto-converted Pydra tasks are generated from their corresponding Nipype interface
in combination with "conversion hints" contained in YAML specs
located in `nipype-auto-conv/specs/`. The self-documented conversion specs are
to be edited by hand in order to assist the auto-converter produce valid pydra tasks.
After editing one or more conversion specs the `pydra.tasks.fsl.auto` package should
be regenerated by running

```console
nipype-auto-conv/generate
```

The tests should be run on the auto-generated tasks to see if they are valid

```console
pytest pydra/tasks/fsl/auto/tests/test_<the-name-of-the-task-you-edited>.py
```

If the test passes you should then edit the `pydra/tasks/fsl/v*/__init__.py` file
to import the auto-generated task interface to signify that it has been validated and is
ready for use, where v* corresponds to the version of FSL that you have tested
it against e.g.

```console
from pydra.tasks.fsl.auto import <the-task-you-have-validated>
```

and copy the test file `pydra/tasks/fsl/auto/tests/test_<validated-task>.py`
into `pydra/tasks/fsl/v*/tests`.


### File-formats and sample test data

The automatically generated tests will attempt to provided the task instance to be tested
with sensible default values based on the type of the field and any constraints it has
on it. However, these will often need to be manually overridden after consulting the
underlying tool's documentation.

For file-based data, automatically generated file-system objects will be created for
selected format types, e.g. Nifti, Dicom. Therefore, it is important to specify the
format of the file using the "mime-like" string corresponding to a
[fileformats](https://github.com/ArcanaFramework/fileformats) class
in the `inputs > types` and `outputs > types` dicts of the YAML spec.

If the required file-type is not found implemented within fileformats, please see the `fileformats`
docs [https://arcanaframework.github.io/fileformats/developer.html] for instructions on how to define
new fileformat types, and see
[fileformats-medimage-extras](https://github.com/ArcanaFramework/fileformats-medimage-extras/blob/6c2dabe91e95687eebc2639bb6f034cf9595ecfc/fileformats/extras/medimage/nifti.py#L30-L48)
for an example on how to implement methods to generate sample data for them. Implementations of
new fileformats that are specific to FSL, and functions to
generate sample data for them, should be defined in `related-packages/fileformats`
and `related-packages/fileformats-extras`, respectively.


## License

This project is distributed under the terms of the [Apache License, Version 2.0][license].

[pypi-project]: https://pypi.org/project/pydra-tasks-fsl

[pypi-version]: https://img.shields.io/pypi/v/pydra-tasks-fsl.svg

[pypi-pyversions]: https://img.shields.io/pypi/pyversions/pydra-tasks-fsl.svg

[pypi-downloads]: https://static.pepy.tech/badge/pydra-tasks-fsl

[status-docs]: https://github.com/aramis-lab/pydra-tasks-fsl/actions/workflows/docs.yaml/badge.svg

[status-test]: https://github.com/aramis-lab/pydra-tasks-fsl/actions/workflows/test.yaml/badge.svg

[pydra]: https://pydra.readthedocs.io/

[fsl]: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSL

[fsl-install]: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation

[fsl-license]: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Licence

[license]: https://spdx.org/licenses/Apache-2.0.html

[status-docs-badge]: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat

[status-cicd-badge]: https://github.com/nipype/pydra-tasks-fsl/actions/workflows/ci-cd.yaml/badge.svg

[status-docs-link]: https://nipype.github.io/pydra-tasks-fsl/

[status-cicd-link]: https://github.com/nipype/pydra-tasks-fsl/actions/workflows/ci-cd.yaml
