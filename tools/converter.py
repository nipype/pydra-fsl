from nipype.interfaces import fsl
from nipype.interfaces.base import traits_extension
import pydra
from pydra.engine import specs

import os, sys, yaml, black, imp
import traits
import attr
from pathlib import Path


INPUT_KEYS = ["allowed_values", "argstr", "container_path", "copyfile", "desc",
              "mandatory", "position", "requires", "sep", "xor",]
OUTPUT_KEYS = ["desc"]
NAME_MAPPING = {"desc": "help_string"}

TRAITS_IRREL = ['output_type', 'args', 'environ', 'environ_items', '__all__',
                'trait_added', 'trait_modified']

INTERFACE = "BET"

TYPE_REPLACE = [("\'File\'", "specs.File"), ("\'bool\'", "bool"), ("\'str\'", "str"),
                ("\'int\'", "int"), ("\'float\'", "float"), ("\'list\'", "list"), ("\'dict\'", "dict")]

with (Path(os.path.dirname(__file__)) / "fsl_conv_param.yml").open() as f:
    INTERF_PARAMS = yaml.safe_load(f)[INTERFACE]


def converter_specs(input_spec, output_spec, write=False, filename=None):
    input_fields_pdr = converter_input_fields(input_spec=input_spec)
    output_fields_pdr = converter_output_spec(output_spec=output_spec)

    input_spec_pydra = specs.SpecInfo(name="Input", fields=input_fields_pdr, bases=(specs.ShellSpec,))
    output_spec_pydra = specs.SpecInfo(name="Output", fields=output_fields_pdr, bases=(specs.ShellOutSpec,))


    if write and filename:
        print("\n FILENAME", filename)
        write_file(filename, input_fields_pdr, output_fields_pdr)

    return input_spec_pydra, output_spec_pydra


def write_file(filename, input_fields, output_fields):
    def types_to_names(spec_fields):
        spec_fields_str = []
        for el in spec_fields:
            el = list(el)
            el[1] = el[1].__name__
            spec_fields_str.append(tuple(el))
        return spec_fields_str

    input_fields_str = types_to_names(spec_fields=input_fields)
    output_fields_str = types_to_names(spec_fields=output_fields)
    cmd = INTERF_PARAMS["cmd"]
    name = INTERF_PARAMS["name"]

    spec_str = "from pydra.engine import specs \nfrom pydra import ShellCommandTask \nimport traits \nimport attr \n"
    spec_str += f"input_fields = {input_fields_str}\n"
    spec_str += f"input_spec = specs.SpecInfo(name='Input', fields=input_fields, bases=(specs.ShellSpec,))\n\n"
    spec_str += f"output_fields = {output_fields_str}\n"
    spec_str += f"output_spec = specs.SpecInfo(name='Output', fields=output_fields, bases=(specs.ShellOutSpec,))\n\n"
    spec_str += f"{name} = ShellCommandTask(name='{name}', executable='{cmd}', input_spec=input_spec, output_spec=output_spec)"

    for tp_repl in TYPE_REPLACE:
        spec_str = spec_str.replace(*tp_repl)

    spec_str_black = black.format_file_contents(spec_str, fast=False, mode=black.FileMode())

    with open(filename, "w") as f:
        f.write(spec_str_black)



def converter_input_fields(input_spec):
    """creating fields list for pydra input spec """
    fields_pdr_dict = {}
    position_dict = {}
    for name, fld in input_spec.traits().items():
        if name in TRAITS_IRREL:
            continue
        fld_pdr, pos = pydra_fld_input(fld, name)
        fields_pdr_dict[name] = (name,) + fld_pdr
        if pos is not None:
            position_dict[name] = pos

    if position_dict:
        fields_pdr_dict = fix_position(fields_pdr_dict, position_dict)

    fields_pdr_l = list(fields_pdr_dict.values())
    return fields_pdr_l


def pydra_fld_input(field, nm):
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
        if nm in INTERF_PARAMS["output_templates"]:
            metadata_pdr["output_file_template"] = INTERF_PARAMS["output_templates"][nm]
            if tp_pdr in [specs.File, specs.Directory]: # since this is a template, the file doesn't exist
                tp_pdr = str
        else:
            raise Exception(f"the filed {nm} has genfile=True, but no output template provided")

    pos = metadata_pdr.get("position", None)

    if default_pdr is not None and not metadata_pdr.get("mandatory", None):
        return (tp_pdr, default_pdr, metadata_pdr), pos
    else:
        return (tp_pdr, metadata_pdr), pos


def converter_output_spec(output_spec):
    """creating fields list for pydra input spec """
    fields_pdr_l = []
    for name, fld in output_spec.traits().items():
        if name in INTERF_PARAMS["output_files"]:
            fld_pdr = pydra_fld_output(fld, name)
            fields_pdr_l.append((name,) + fld_pdr)
    return fields_pdr_l


def pydra_fld_output(field, name):
    """converting a single nipype field to one element of fields for pydra output_spec"""
    tp = field.trait_type
    tp_pdr = pydra_type_converter(tp)

    metadata_pdr = {}
    for key in OUTPUT_KEYS:
        key_nm_pdr = NAME_MAPPING.get(key, key)
        val = getattr(field, key)
        if val:
            metadata_pdr[key_nm_pdr] = val

    metadata_pdr["requires"] = INTERF_PARAMS["output_files"][name]
    if name in INTERF_PARAMS["output_templates"]:
        metadata_pdr["output_file_template"] = INTERF_PARAMS["output_templates"][name]

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
    assert shelly.cmdline == f"bet {in_file} {out_file}"
    res = shelly()
    print("\n Result: ", res)


    shelly_mask = pydra.ShellCommandTask(
        name="bet_task", executable=INTERF_PARAMS["cmd"], input_spec=input_spec_pydra, output_spec=output_spec_pydra
    )
    shelly_mask.inputs.in_file = in_file
    shelly_mask.inputs.mask = True
    assert shelly_mask.cmdline == f"bet {in_file} {out_file} -m"
    res = shelly_mask()
    print("\n Result: ", res)


def test_spec_from_file(tmpdir):
    interface_name = INTERFACE
    interface = getattr(fsl, interface_name)
    in_file = Path(os.path.dirname(__file__)) / "data_tests/test.nii.gz"
    out_file = Path(os.path.dirname(__file__)) / "data_tests/test_brain.nii.gz"

    filename_spec = tmpdir.join("spec.py")

    input_spec = interface.input_spec()
    output_spec = interface.output_spec()
    _, _ = converter_specs(input_spec, output_spec, write=True, filename=filename_spec)

    imp.load_source("bet_module", str(filename_spec))
    import bet_module as bm


    shelly = bm.bet
    shelly.inputs.in_file = in_file
    assert shelly.inputs.executable == "bet"
    assert shelly.cmdline == f"bet {in_file} {out_file}"
    res = shelly()
    print("\n Result: ", res)


    shelly_mask = bm.bet
    shelly_mask.inputs.in_file = in_file
    shelly_mask.inputs.mask = True
    assert shelly_mask.cmdline == f"bet {in_file} {out_file} -m"
    res = shelly_mask()
    print("\n Result: ", res)
