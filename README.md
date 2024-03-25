# pydra-tasks-fsl

[![PyPI - Version][pypi-version]][pypi-project]
[![PyPI - Python Version][pypi-pyversions]][pypi-project]

-----

Pydra tasks for FSL.

[Pydra][pydra] is a dataflow engine which provides
a set of lightweight abstractions for DAG
construction, manipulation, and distributed execution.

[FSL][fsl] is a comprehensive library of analysis tools
for FMRI, MRI and DTI brain imaging data.

**Table of contents**

- [Available interfaces](#available-interfaces)
- [Installation](#installation)
- [Development](#development)
- [License](#license)

## Available interfaces

- bet
    - bet
    - robustfov
- flirt
    - convert_xfm
    - flirt
- fnirt
    - fnirt
- utils
    - fslmerge
    - fslreorient2std
    - fslroi

## Installation

```console
pip install pydra-tasks-fsl
```

## Development

This project is managed with [Hatch][hatch]:

```console
pipx install hatch
```

To run the test suite:

```console
hatch run test:no-cov
```

To fix linting issues:

```console
hatch run lint:fix
```

## License

`pydra-tasks-fsl` is distributed under the terms of the [Apache License 2.0][license] license.

[pypi-project]: https://pypi.org/project/pydra-tasks-fsl

[pypi-version]: https://img.shields.io/pypi/v/pydra-tasks-fsl.svg

[pypi-pyversions]: https://img.shields.io/pypi/pyversions/pydra-tasks-fsl.svg

[pydra]: https://pydra.readthedocs.io/

[fsl]: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSL

[hatch]: https://hatch.pypa.io/

[license]: https://spdx.org/licenses/Apache-2.0.html
