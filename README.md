## Converter

`FSLConverter` class (from `tools/converter.py`) requires three parts of information:

- Nipype spec: converter loads nipype interface and reads `_cmd`, `input_spec` and `output_spec`
- yml file with additional spec: `specs/fsl_conv_params.yml` contains additional spec that are written based 
on additional functions from nipype (including `list_outputs`), each interface can have the following fields:
    - inputs_metadata: additional fields for metadata for fields from input_spec, 
    e.g., used for `FAST` to set default for `number_classes` 
    (it's not part of nipype's spec, but it's set in `list_output`)

    - output_requirements: providing required field for the output to be created, 
    taken from `list_output` structure; 
    it's a part of the `requires` field in metadata
    
    - output_templates: providing template to create the output file name, 
    taken from `list_output` structure; 
    it is set as `output_file_template` in metadata
    
    - output_callables: providing function name that should be used to gather output,
    based on the `list_output` structure and used only for `FAST`;
    it is set as `output_file_template` in metadata

- python file with functions used as callables to gather the outputs: 
`specs/callables.py` should contain all the functions from `output_callables`;
the source code of the functions is read and written again in the pydra interface file


### How to convert

Currently, the converter is temporarly used in a pytest test, so can be run as `pytest tools/converter.py`
in order to run `test_convert_file` (other tests should be skipped).
The tests will create a converter for interfaces names provided in the 
`parametrize` decorator and for each interface `pydra_specs` will be run.
The method creates file with the pydra task in the `preprocess` directory,
and two tests in the `preprocess/tests` directory. 

Tests are written based on the fields from the yml file: 
`tests_inputs` and `tests_outputs` (the lengths should be the same).
One test, `test_specs_*` checks only the correctness of the spec based
on the `test_inputs/outputs` pairs, i.e. predicts which output fields
should be created based on the list of the input fields.
The second test, `test_run_*` should run teh interfaces, this is temporary, 
should be removed from the final repo. 

