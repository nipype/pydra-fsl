# Intent of this template

The intent of this repo is to help you get started with creating Pydra tasks.
All tasks will be inserted into pydra.tasks.<yourtaskpackagename> namespace.

# To use this template:

1. Click on new repo.
2. Select this template from the repository template drop down list.
3. Give your repo a name.
4. Once the repo is created and cloned, search for TODO (`grep -rn TODO . `) and
  replace with appropriate name.
5. One of the folders is called TODO. This should also be renamed to your package
   name.
6. Add tasks to the pydra/tasks/<yourpackagename> folder.
7. You may want to initialize a sphinx docs directory.

# TODO: Change this README after creating your new repo.


## For developers

Install repo in developer mode from the source directory. It is also useful to
install pre-commit to take care of styling via black:

```
pip install -e .[dev]
pre-commit install
```
