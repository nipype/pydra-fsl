from nipype.interfaces import fsl
from nipype.interfaces.base import traits_extension
import pydra
from pydra.engine import specs

import os, sys, yaml, black, imp
import traits
import attr
from pathlib import Path
import typing as ty
import pytest


INPUT_KEYS = ["allowed_values", "argstr", "container_path", "copyfile", "desc",
              "mandatory", "position", "requires", "sep", "xor",]
OUTPUT_KEYS = ["desc"]
NAME_MAPPING = {"desc": "help_string"}

TRAITS_IRREL = ['output_type', 'args', 'environ', 'environ_items', '__all__',
                'trait_added', 'trait_modified']

INTERFACE = "BET"

TYPE_REPLACE = [("\'File\'", "specs.File"), ("\'bool\'", "bool"), ("\'str\'", "str"), ("\'Any\'", "ty.Any"),
                ("\'int\'", "int"), ("\'float\'", "float"), ("\'list\'", "list"), ("\'dict\'", "dict")]

with (Path(os.path.dirname(__file__)) / "fsl_conv_param.yml").open() as f:
    INTERF_PARAMS = yaml.safe_load(f)[INTERFACE]


def converter_specs(input_spec, output_spec, interf_params=INTERF_PARAMS, write=False, dirname=None):
    input_fields_pdr = converter_input_fields(input_spec=input_spec, interf_params=interf_params)
    output_fields_pdr = converter_output_spec(output_spec=output_spec, interf_params=interf_params)

    input_spec_pydra = specs.SpecInfo(name="Input", fields=input_fields_pdr, bases=(specs.ShellSpec,))
    output_spec_pydra = specs.SpecInfo(name="Output", fields=output_fields_pdr, bases=(specs.ShellOutSpec,))


    if write and dirname:
        filename = dirname / f"{interf_params['filename']}.py"
        filename_test = dirname / "tests" / f"test_{filename.name}"

        print("\n FILENAME", filename)
        write_file(filename, input_fields_pdr, output_fields_pdr, interf_params=interf_params)

        # fielname_test = filename.parent / f"test_{filename.name}"
        write_test(filename_test=filename_test, interf_params=interf_params)

    return input_spec_pydra, output_spec_pydra


def write_file(filename, input_fields, output_fields, interf_params):
    def types_to_names(spec_fields):
        spec_fields_str = []
        for el in spec_fields:
            el = list(el)
            try:
                el[1] = el[1].__name__
            except(AttributeError):
                el[1] = el[1]._name
            spec_fields_str.append(tuple(el))
        return spec_fields_str

    input_fields_str = types_to_names(spec_fields=input_fields)
    output_fields_str = types_to_names(spec_fields=output_fields)
    cmd = interf_params["cmd"]
    name = interf_params["name"]

    spec_str = "from pydra.engine import specs \nfrom pydra import ShellCommandTask \n"
    spec_str += f"from pydra.utils.messenger import AuditFlag\n"
    spec_str += f"import traits \nimport attr \nimport typing as ty\n"
    spec_str += f"input_fields = {input_fields_str}\n"
    spec_str += f"bet_input_spec = specs.SpecInfo(name='Input', fields=input_fields, bases=(specs.ShellSpec,))\n\n"
    spec_str += f"output_fields = {output_fields_str}\n"
    spec_str += f"bet_output_spec = specs.SpecInfo(name='Output', fields=output_fields, bases=(specs.ShellOutSpec,))\n\n"

    spec_str += f"class {name}(ShellCommandTask):\n"
    spec_str += f"    def __init__(self, audit_flags: AuditFlag = AuditFlag.NONE, cache_dir=None, " \
                f"input_spec=None, messenger_args=None, messengers=None, name=None, output_spec=None," \
            f"rerun=False, strip=False, **kwargs):\n"
    spec_str += f"        if input_spec is None: input_spec = bet_input_spec\n"
    spec_str += f"        if output_spec is None: output_spec = bet_output_spec\n"
    spec_str += f"        if name is None: name = '{name}'\n"
    spec_str += f"        super().__init__(name='{name}', input_spec=input_spec, output_spec=output_spec, " \
                f"audit_flags=audit_flags, messengers=messengers, messenger_args=messenger_args, " \
                f"cache_dir=cache_dir, strip=strip, rerun=rerun, executable='{cmd}', **kwargs)\n"


    for tp_repl in TYPE_REPLACE:
        spec_str = spec_str.replace(*tp_repl)

    spec_str_black = black.format_file_contents(spec_str, fast=False, mode=black.FileMode())

    with open(filename, "w") as f:
        f.write(spec_str_black)


def write_test(filename_test, interf_params):
    cmd = interf_params["cmd"]
    name = interf_params["name"]
    filename = interf_params["filename"]
    tests_inputs = interf_params["tests_inputs"]
    if "tests_outputs" in interf_params:
        tests_outputs = interf_params["tests_outputs"]
        if len(tests_inputs) != len(tests_outputs):
            raise Exception("tests and tests_outputs should have the same length")
    else:
        tests_outputs = len(tests_inputs) * [[]]
    tests_inp_outp = list(zip(tests_inputs, tests_outputs))

    print("\FILENAME TEST", filename_test)
    in_file = str(filename_test.parent / 'data_tests/test.nii.gz')

    spec_str = f"import pytest \nfrom ..{filename} import {name} \n\n"
    spec_str += f"@pytest.mark.parametrize('inputs, outputs', {tests_inp_outp})\n"
    spec_str += f"def test_{name}(inputs, outputs):\n"
    spec_str += f"    if inputs is None: inputs = {{}}\n"
    spec_str += f"    task = {name}(in_file='{in_file}', **inputs)\n"
    spec_str += f"    res = task()\n"
    spec_str += f"    print('RESULT: ', res)\n"
    spec_str += f"    if isinstance(outputs, str): outputs = [outputs]\n"
    spec_str += f"    for out_nm in outputs: assert getattr(res.output, out_nm).exists()\n"

    spec_str_black = black.format_file_contents(spec_str, fast=False, mode=black.FileMode())

    with open(filename_test, "w") as f:
        f.write(spec_str_black)



def converter_input_fields(input_spec, interf_params):
    """creating fields list for pydra input spec """
    fields_pdr_dict = {}
    position_dict = {}
    for name, fld in input_spec.traits().items():
        if name in TRAITS_IRREL:
            continue
        fld_pdr, pos = pydra_fld_input(fld, name, interf_params=interf_params)
        fields_pdr_dict[name] = (name,) + fld_pdr
        if pos is not None:
            position_dict[name] = pos

    if position_dict:
        fields_pdr_dict = fix_position(fields_pdr_dict, position_dict)

    fields_pdr_l = list(fields_pdr_dict.values())
    return fields_pdr_l


def pydra_fld_input(field, nm, interf_params):
    """converting a single nipype field to one element of fields for pydra input_spec"""
    tp = field.trait_type
    tp_pdr = pydra_type_converter(tp)

    if getattr(field, "usedefault") and field.default is not traits.ctrait.Undefined:
        default_pdr = field.default
    else:
        default_pdr = None

    metadata_pdr = {}
    for key in INPUT_KEYS:
        key_nm_pdr = NAME_MAPPING.get(key, key)
        val = getattr(field, key)
        if val is not None:
            if key == "argstr" and "%" in val:
                val = string_formats(argstr=val, name=nm)
            metadata_pdr[key_nm_pdr] = val

    if getattr(field, "genfile"):
        if nm in interf_params["output_templates"]:
            metadata_pdr["output_file_template"] = interf_params["output_templates"][nm]
            if tp_pdr in [specs.File, specs.Directory]: # since this is a template, the file doesn't exist
                tp_pdr = str
        else:
            raise Exception(f"the filed {nm} has genfile=True, but no output template provided")

    pos = metadata_pdr.get("position", None)

    if default_pdr is not None and not metadata_pdr.get("mandatory", None):
        return (tp_pdr, default_pdr, metadata_pdr), pos
    else:
        return (tp_pdr, metadata_pdr), pos


def converter_output_spec(output_spec, interf_params):
    """creating fields list for pydra input spec """
    fields_pdr_l = []
    for name, fld in output_spec.traits().items():
        if name in interf_params["output_files"]:
            fld_pdr = pydra_fld_output(fld, name, interf_params=interf_params)
            fields_pdr_l.append((name,) + fld_pdr)
    return fields_pdr_l


def pydra_fld_output(field, name, interf_params):
    """converting a single nipype field to one element of fields for pydra output_spec"""
    tp = field.trait_type
    tp_pdr = pydra_type_converter(tp)

    metadata_pdr = {}
    for key in OUTPUT_KEYS:
        key_nm_pdr = NAME_MAPPING.get(key, key)
        val = getattr(field, key)
        if val:
            metadata_pdr[key_nm_pdr] = val

    if interf_params["output_files"][name]:
        if all([isinstance(el, list) for el in interf_params["output_files"][name]]):
            requires_l = interf_params["output_files"][name]
            nested_flag = True
        elif all([isinstance(el, (str, dict)) for el in interf_params["output_files"][name]]):
            requires_l = [interf_params["output_files"][name]]
            nested_flag = False
        else:
            Exception("has to be either list of list or list of str/dict")

        metadata_pdr["requires"] = []
        for requires in requires_l:
            requires_mod = []
            for el in requires:
                if isinstance(el, str):
                    requires_mod.append(el)
                elif isinstance(el, dict):
                    requires_mod += list(el.items())
            metadata_pdr["requires"].append(requires_mod)
        if nested_flag is False:
            metadata_pdr["requires"] = metadata_pdr["requires"][0]

    if name in interf_params["output_templates"]:
        metadata_pdr["output_file_template"] = interf_params["output_templates"][name]

    return (tp_pdr, metadata_pdr)


def pydra_type_converter(tp):
    """converting types to types used in pydra"""
    if isinstance(tp, traits.trait_types.Int):
        tp_pdr = int
    elif isinstance(tp, traits.trait_types.Float):
        tp_pdr = float
    elif isinstance(tp, traits.trait_types.Str):
        tp_pdr = str
    elif isinstance(tp, traits.trait_types.Bool):
        tp_pdr = bool
    elif isinstance(tp, traits.trait_types.Dict):
        tp_pdr = dict
    elif isinstance(tp, traits.trait_types.List):
        tp_pdr = list
    elif isinstance(tp, traits_extension.File):
        tp_pdr = specs.File
    else:
        tp_pdr = ty.Any
    return tp_pdr



def fix_position(fields_dict, positions):
    """ fixing positions all of the fields"""
    positions_list = list(positions.values())
    positions_list.sort()
    if positions_list[0] < -1:
        raise Exception("position in nipype interface < -1")
    if positions_list[0] == -1:
        positions_list.append(positions_list.pop(0))

    positions_map = {}
    for ii, el in enumerate(positions_list):
        if el != ii + 1:
            positions_map[el] = ii + 1

    for nm, pos in positions.items():
        if pos in positions_map:
            # dictionary with metadata should be the last element
            fields_dict[nm][-1]["position"] = positions_map[pos]

    return fields_dict


def string_formats(argstr, name):
    argstr_l = argstr.split(" ")
    for ii, el in enumerate(argstr_l):
        if "%" in el:
            #argstr_l[ii] = "{" + el.replace("%", "{}:".format(name)) + "}"
            argstr_l[ii] = "{" + name + "}"
    return " ".join(argstr_l)


@pytest.mark.parametrize("interface_name", ["BET", "MCFLIRT"])
def test_convert_file(interface_name):
    interface = getattr(fsl, interface_name)
    input_spec = interface.input_spec()
    output_spec = interface.output_spec()

    with (Path(os.path.dirname(__file__)) / "fsl_conv_param.yml").open() as f:
        interf_params = yaml.safe_load(f)[interface_name]

    dirname_interf = Path(os.path.dirname(__file__)) / "../preprocess"

    _, _ = converter_specs(input_spec, output_spec, interf_params=interf_params, write=True, dirname=dirname_interf)


@pytest.mark.skip()
def test_spec(tmpdir):
    interface_name = INTERFACE
    interface = getattr(fsl, interface_name)
    in_file =  Path(os.path.dirname(__file__)) / "data_tests/test.nii.gz"
    out_file = Path(os.path.dirname(__file__)) / "data_tests/test_brain.nii.gz"

    input_spec = interface.input_spec()
    output_spec = interface.output_spec()
    input_spec_pydra, output_spec_pydra = converter_specs(input_spec, output_spec)

    shelly = pydra.ShellCommandTask(
        name="bet_task", executable=INTERF_PARAMS["cmd"],
        input_spec=input_spec_pydra, output_spec=output_spec_pydra
    )
    shelly.inputs.in_file = in_file
    assert shelly.inputs.executable == "bet"
    assert shelly.cmdline == f"bet {in_file} {str(shelly.output_dir / 'test_brain.nii.gz')}"
    res = shelly()
    assert res.output.out_file.exists()
    print("\n Result: ", res)


    shelly_mask = pydra.ShellCommandTask(
        name="bet_task", executable=INTERF_PARAMS["cmd"], input_spec=input_spec_pydra, output_spec=output_spec_pydra
    )
    shelly_mask.inputs.in_file = in_file
    shelly_mask.inputs.mask = True
    assert shelly_mask.cmdline == f"bet {in_file} {str(shelly_mask.output_dir / 'test_brain.nii.gz')} -m"
    res = shelly_mask()
    assert res.output.out_file.exists()
    assert res.output.mask_file.exists()
    print("\n Result: ", res)


@pytest.mark.skip()
def test_spec_from_file(tmpdir):
    interface_name = INTERFACE
    interface = getattr(fsl, interface_name)
    in_file = Path(os.path.dirname(__file__)) / "data_tests/test.nii.gz"

    dirname_spec = Path(tmpdir)
    (dirname_spec / "tests").mkdir()

    input_spec = interface.input_spec()
    output_spec = interface.output_spec()
    _, _ = converter_specs(input_spec, output_spec, write=True, dirname=dirname_spec)

    imp.load_source("bet_module", str(dirname_spec / "bet.py"))
    import bet_module as bm


    shelly = bm.BET(name="my_bet")
    shelly.inputs.in_file = in_file
    assert shelly.inputs.executable == "bet"
    assert shelly.cmdline == f"bet {in_file} {str(shelly.output_dir / 'test_brain.nii.gz')}"
    res = shelly()
    assert res.output.out_file.exists()
    print("\n Result: ", res)


    shelly_mask = bm.BET(name="my_bet")
    shelly_mask.inputs.in_file = in_file
    shelly_mask.inputs.mask = True
    assert shelly_mask.cmdline == f"bet {in_file} {str(shelly_mask.output_dir / 'test_brain.nii.gz')} -m"
    res = shelly_mask()
    assert res.output.out_file.exists()
    assert res.output.mask_file.exists()
    print("\n Result: ", res)


    shelly_surf = bm.BET(name="my_bet")
    shelly_surf.inputs.in_file = in_file
    shelly_surf.inputs.surfaces = True
    assert shelly_surf.cmdline == f"bet {in_file} {str(shelly_surf.output_dir / 'test_brain.nii.gz')} -A"
    res = shelly_surf()
    assert res.output.out_file.exists()
    assert res.output.inskull_mask_file.exists()
    assert res.output.skull_mask_file.exists()
    print("\n Result: ", res)
