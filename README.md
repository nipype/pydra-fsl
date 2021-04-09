# Intent of this template

The intent of this repository is to help you get started with creating Pydra tasks.
All tasks will be inserted into the `pydra.tasks.<yourtaskpackagename>` namespace.

# To use this template

1. Click on new repo.
1. Select this template from the repository template drop down list.
1. Give your repo a name.
1. Once the repo is created and cloned, search for TODO (`grep -rn TODO . `) and
   replace with appropriate name.
1. One of the folders is called TODO. This should also be renamed to your package
   name.
1. Add tasks to the `pydra/tasks/<yourpackagename>` folder.
1. An example subpackage is found in `pydra/tasks/<yourpackagename>/utils`.
   You may wish to add tools to it or delete it.
1. You may want to initialize a [Sphinx] docs directory.
1. Review the workflow in `.github/workflows/pythonpackage.yml`. Testing editable installations
   is probably not useful unless you are reconfiguring namespace packages.
1. **Update this README after creating the new repository.**

[Sphinx]: https://www.sphinx-doc.org/en/master/usage/quickstart.html

# Features of this template

## Versioneer

The [versioneer](https://github.com/warner/python-versioneer) tool allows for versioning based
on the most recent git tag. The release process can thus be:

```Shell
git tag -a 1.0.0
python setup.py sdist bdist_wheel
twine upload dist/*
```

Note that uploading to PyPI is done via [Continuous integration](#continuous-integration)) when
a tag is pushed to the repository, so only the first step needs to be donne manually.

Note also that we assume tags will be version numbers and not be prefixed with `v` or some other
string. See Versioneer documentation for alternative configurations.

## Namespace packages

[Namespace packages] allow multiple packages to be installed in such a way that they can be
imported from a common namespace. In this case, the base namespace is `pydra.tasks`, and each
task package installs a new module, such as `pydra.tasks.afni`.

To do correctly, task packages **must not** interfere with files higher in the hierarchy.
This includes adding `__init__.py` files in either `pydra` or `pydra/tasks`.

[Namespace packages]: https://www.python.org/dev/peps/pep-0420/

## Tests

This package comes with a default set of test modules, and we encourage users to use pytest.
Tests can be discovered and run using:

```
pytest --doctest-modules pydra/tasks/*
```

## Continuous integration

This template uses [GitHub Actions](https://docs.github.com/en/actions/) to run tests. To simulate
several plausible development or installation environments, we test over all Python versions
supported by Pydra, and install Pydra and the current package in both standard and
[editable](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs) modes.

The combination of standard/editable is in particular designed to ensure that namespace packaging
does not break. We strongly recommend keeping these tests in place for this reason, as one
non-compliant package can potentially affect Pydra or other task packages.

In addition to verifying installations do not break or conflict, pytest is run on the package,
including all tests found in `test/` directories and [doctests].

Finally, packages are built and uploaded as artifacts for inspection. When a tag is pushed,
the packages are uploaded to PyPI if a valid [API token](https://pypi.org/help/#apitoken) is placed
in the [repository secrets](https://docs.github.com/en/actions/reference/encrypted-secrets).

[doctests]: https://docs.python.org/3/library/doctest.html

# Contributing to this template

This template repository is periodically updated as we establish and best practices for task
packages. We welcome contributions from the community to help set a solid baseline for all
task packages.

# Sample post-setup README contents

## For developers

Install repo in developer mode from the source directory. It is also useful to
install pre-commit to take care of styling via black:

```
pip install -e .[dev]
pre-commit install
```
