# Pydra FSL Tasks

This repository aims to be the canonical set of Pydra tasks for incorporating
[FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/) tools into a Pydra workflow.

Part of this effort is to establish a (mostly) declarative language for describing tasks that
potentially have intricate rules for determining the availability and names from the choice of
inputs. See [Converter](#Converter) for this aspect of the repository.

## Installation

```
pip install pydra-fsl
```

or

```
pip install /path/to/pydra-fsl/
```

## Converter

`FSLConverter` class (from `tools/converter.py`) requires three parts of information:

- Nipype spec: converter loads nipype interface and reads `_cmd`, `input_spec` and `output_spec`
- yml file with additional spec: `specs/fsl_{module_name}_params.yml` contains additional spec that are written based 
on additional functions from nipype (including `list_outputs`), each interface can have the following fields:
    - inputs_metadata: additional metadata for fields from input_spec 
    (it will be included in `metadata` in pydra spec), 
    e.g., used in `specs/fsl_preprocess_params.yml` for `FAST` to set default value for `number_classes` 
    (it's not part of nipype's spec, but it's set in `list_output`)

    - output_requirements: providing required fields for the output to be created, 
    taken from `list_output` structure; 
    it's a part of the `requires` field in metadata in pydra spec
    
    - output_templates: providing template to create the output file name, 
    taken from `list_output` structure; 
    it is set as `output_file_template` in metadata
    
    - output_callables: providing function name that should be used to gather output,
    based on the `list_output` structure and used only for `FAST`;
    it is set as `callable` in metadata
    
    - tests_inputs, tests_outputs: specification for tests, 
    the fields should have the same length and each element should contain 
    the input fields values and list of the expected output fields names
    
    - doctests: specification for doctest,
    should include values for input fields and the expected `cmdline` 

- python file with functions used as callables to gather the outputs: 
`specs/callables.py` should contain all the functions from `output_callables`;
the source code of the functions is read and written again in the pydra interface file


### How to use the convert

The converter can be used by running:
 
    python tools/converter.py --interface_name <name of teh interface> --module_name <module_name>

The pydra task will be created and saved in `pydra/tasks/fsl/{module_name}/{interface_name}.py`.
Note, that the spec file has to be present for the specific module name in order to run the converter.
If no `interface_name` is provided, the default value `all` will be used
 and the converter will be run for all interfaces from the spec file.

Tests are written based on the fields from the yml file: 
`tests_inputs` and `tests_outputs` (the lengths should be the same).
One test, `test_specs_*` checks only the correctness of the spec based
on the `test_inputs/outputs` pairs, i.e. predicts which output fields
should be created based on the list of the input fields.
The second test, `test_run_*` should run the interfaces 
(TODO: this is temporary, should be removed from the final repo). 
Tests can be run using `pytest`:

    pytest -vs pydra/tasks/fsl/{module_name}/tests

