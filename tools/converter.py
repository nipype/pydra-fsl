from attr import has
from nipype.interfaces import fsl
from nipype.interfaces.base import traits_extension
from pydra.engine import specs
from pydra.engine.helpers import ensure_list

import os, sys, yaml, black, imp
import traits
from pathlib import Path
import typing as ty
import inspect
import click
import warnings
import functools

sys.path.append(str(Path(__file__).resolve().parent.parent / "specs"))
import callables


class FSLConverter:

    INPUT_KEYS = [
        "allowed_values",
        "argstr",
        "container_path",
        "copyfile",
        "desc",
        "mandatory",
        "position",
        "requires",
        "sep",
        "xor",
    ]
    OUTPUT_KEYS = ["desc"]
    NAME_MAPPING = {"desc": "help_string"}

    TRAITS_IRREL = [
        "output_type",
        "args",
        "environ",
        "environ_items",
        "__all__",
        "trait_added",
        "trait_modified",
    ]

    TYPE_REPLACE = [
        ("'File'", "specs.File"),
        ("'bool'", "bool"),
        ("'str'", "str"),
        ("'Any'", "ty.Any"),
        ("'int'", "int"),
        ("'float'", "float"),
        ("'list'", "list"),
        ("'dict'", "dict"),
        ("'MultiInputObj'", "specs.MultiInputObj"),
        ("'MultiOutputObj'", "specs.MultiOutputObj"),
        ("'MultiInputFile'", "specs.MultiInputFile"),
        ("'MultiOutputFile'", "specs.MultiOutputFile"),
    ]

    def __init__(self, interface_name, interface_spec_file):
        self.interface_name = interface_name
        with interface_spec_file.open() as f:
            self.interface_spec = yaml.safe_load(f)[self.interface_name]
        if self.interface_spec.get("output_requirements") is None:
            self.interface_spec["output_requirements"] = []
        if self.interface_spec.get("inputs_metadata") is None:
            self.interface_spec["inputs_metadata"] = {}
        if self.interface_spec.get("inputs_drop") is None:
            self.interface_spec["inputs_drop"] = []
        if self.interface_spec.get("output_templates") is None:
            self.interface_spec["output_templates"] = {}
        if self.interface_spec.get("output_callables") is None:
            self.interface_spec["output_callables"] = {}
        if (
            not self.interface_spec["output_callables"]
            .keys()
            .isdisjoint(self.interface_spec["output_templates"].keys())
        ):
            raise Exception("output_callables and output_templates have the same keys")
        if self.interface_spec.get("doctest") is None:
            self.interface_spec["doctest"] = {}

        # getting input/output spec from nipype
        nipype_interface = getattr(fsl, self.interface_name)
        self.cmd = nipype_interface._cmd
        self.nipype_input_spec = nipype_interface.input_spec()
        self.nipype_output_spec = nipype_interface.output_spec()

    def pydra_specs(self, write=False, dirname=None):
        """creating pydra input/output spec from nipype specs
        if write is True, a pydra Task class will be written to the file together with tests
        """
        input_fields_pdr, inp_templates = self.convert_input_fields()
        output_fields_pdr = self.convert_output_spec(fields_from_template=inp_templates)

        input_spec_pydra = specs.SpecInfo(
            name="Input", fields=input_fields_pdr, bases=(specs.ShellSpec,)
        )
        output_spec_pydra = specs.SpecInfo(
            name="Output", fields=output_fields_pdr, bases=(specs.ShellOutSpec,)
        )

        if write:
            if dirname is None:
                raise Exception("dirname has to be provided if write is True")
            self.write_pydra_files(
                dirname=dirname,
                pydra_input_spec=input_fields_pdr,
                pydra_output_spec=output_fields_pdr,
            )
        return input_spec_pydra, output_spec_pydra

    def write_pydra_files(self, dirname, pydra_input_spec, pydra_output_spec):
        """writing pydra task and tests to the files"""
        testdir = dirname / "tests"
        testdir.mkdir(parents=True, exist_ok=True)
        Path.touch(dirname / "__init__.py")
        Path.touch(testdir / "__init__.py")
        filename = dirname / f"{self.interface_name.lower()}.py"
        filename_test = testdir / f"test_spec_{filename.name}"
        filename_test_run = testdir / f"test_run_{filename.name}"

        print("\n FILENAME", filename)
        self.write_task(filename, pydra_input_spec, pydra_output_spec)

        self.write_test(filename_test=filename_test)
        self.write_test(filename_test=filename_test_run, run=True)

    def write_task(self, filename, input_fields, output_fields):
        """writing pydra task to the dile based on the input and output spec"""

        def types_to_names(spec_fields):
            spec_fields_str = []
            for el in spec_fields:
                el = list(el)
                try:
                    el[1] = el[1].__name__
                except (AttributeError):
                    el[1] = el[1]._name
                spec_fields_str.append(tuple(el))
            return spec_fields_str

        input_fields_str = types_to_names(spec_fields=input_fields)
        output_fields_str = types_to_names(spec_fields=output_fields)
        functions_str = self.function_callables()
        spec_str = (
            "from pydra.engine import specs \nfrom pydra import ShellCommandTask \n"
        )
        spec_str += f"import typing as ty\n"
        spec_str += functions_str
        spec_str += f"input_fields = {input_fields_str}\n"
        spec_str += f"{self.interface_name}_input_spec = specs.SpecInfo(name='Input', fields=input_fields, bases=(specs.ShellSpec,))\n\n"
        spec_str += f"output_fields = {output_fields_str}\n"
        spec_str += f"{self.interface_name}_output_spec = specs.SpecInfo(name='Output', fields=output_fields, bases=(specs.ShellOutSpec,))\n\n"

        spec_str += f"class {self.interface_name}(ShellCommandTask):\n"
        if self.interface_spec["doctest"]:
            spec_str += self.create_doctest()
        spec_str += f"    input_spec = {self.interface_name}_input_spec\n"
        spec_str += f"    output_spec = {self.interface_name}_output_spec\n"
        spec_str += f"    executable='{self.cmd}'\n"

        for tp_repl in self.TYPE_REPLACE:
            spec_str = spec_str.replace(*tp_repl)

        spec_str_black = black.format_file_contents(
            spec_str, fast=False, mode=black.FileMode()
        )

        with open(filename, "w") as f:
            f.write(spec_str_black)

    def write_test(self, filename_test, run=False):
        """writing tests for the specific interface based on the test spec (from interface_spec)
        if run is True the test contains task run,
        if run is False only the spec is check by the test
        """
        tests_inputs = self.interface_spec["tests_inputs"]
        tests_outputs = self.interface_spec["tests_outputs"]
        if len(tests_inputs) != len(tests_outputs):
            raise Exception("tests and tests_outputs should have the same length")

        tests_inp_outp = []
        tests_inp_error = []
        for i, out in enumerate(tests_outputs):
            if isinstance(out, list):
                tests_inp_outp.append((tests_inputs[i], out))
            elif out is None:
                tests_inp_outp.append((tests_inputs[i], []))
            # allowing for incomplete or incorrect inputs that should raise an exception
            elif out not in ["AttributeError", "Exception"]:
                tests_inp_outp.append((tests_inputs[i], [out]))
            else:
                tests_inp_error.append((tests_inputs[i], out))

        spec_str = f"import os, pytest \nfrom pathlib import Path\n"
        spec_str += (
            f"from ..{self.interface_name.lower()} import {self.interface_name} \n\n"
        )
        if run:
            spec_str += (
                "@pytest.mark.xfail('FSLDIR' not in os.environ, reason='no FSL found', "
                "raises=FileNotFoundError)\n"
            )
        spec_str += f"@pytest.mark.parametrize('inputs, outputs', {tests_inp_outp})\n"
        spec_str += f"def test_{self.interface_name}(test_data, inputs, outputs):\n"
        spec_str += f"    in_file = Path(test_data) / 'test.nii.gz'\n"
        spec_str += f"    if inputs is None: inputs = {{}}\n"
        spec_str += f"    for key, val in inputs.items():\n"
        spec_str += f"        try: inputs[key] = eval(val)\n"
        spec_str += f"        except: pass\n"
        spec_str += f"    task = {self.interface_name}(in_file=in_file, **inputs)\n"
        spec_str += (
            f"    assert set(task.generated_output_names) == "
            f"set(['return_code', 'stdout', 'stderr'] + outputs)\n"
        )

        if run:
            spec_str += f"    res = task()\n"
            spec_str += f"    print('RESULT: ', res)\n"
            spec_str += f"    for out_nm in outputs: assert getattr(res.output, out_nm).exists()\n"

        # if test_inp_error is not empty, than additional test function will be created
        if tests_inp_error:
            spec_str += self.write_test_error(input_error=tests_inp_error)

        spec_str_black = black.format_file_contents(
            spec_str, fast=False, mode=black.FileMode()
        )

        with open(filename_test, "w") as f:
            f.write(spec_str_black)

    def write_test_error(self, input_error):
        """creating a tests for incorrect or incomplete inputs
        checking if the exceptions are raised
        """
        spec_str = "\n\n"
        spec_str += f"@pytest.mark.parametrize('inputs, error', {input_error})\n"
        spec_str += (
            f"def test_{self.interface_name}_exception(test_data, inputs, error):\n"
        )
        spec_str += f"    in_file = Path(test_data) / 'test.nii.gz'\n"
        spec_str += f"    if inputs is None: inputs = {{}}\n"
        spec_str += f"    for key, val in inputs.items():\n"
        spec_str += f"        try: inputs[key] = eval(val)\n"
        spec_str += f"        except: pass\n"
        spec_str += f"    task = {self.interface_name}(in_file=in_file, **inputs)\n"
        spec_str += f"    with pytest.raises(eval(error)):\n"
        spec_str += f"        task.generated_output_names\n"

        return spec_str

    def create_doctest(self):
        """adding doctests to the interfaces"""
        cmdline = self.interface_spec["doctest"].pop("cmdline")
        doctest = '    """\n    Example\n    -------\n'
        doctest += f"    >>> task = {self.interface_name}()\n"
        for key, val in self.interface_spec["doctest"].items():
            if type(val) is str:
                doctest += f'    >>> task.inputs.{key} = "{val}"\n'
            else:
                doctest += f"    >>> task.inputs.{key} = {val}\n"
        doctest += "    >>> task.cmdline\n"
        doctest += f"    '{cmdline}'"
        doctest += '\n    """\n'
        return doctest

    def convert_input_fields(self):
        """creating fields list for pydra input spec"""
        fields_pdr_dict = {}
        position_dict = {}
        has_template = []
        for name, fld in self.nipype_input_spec.traits().items():
            if name in self.TRAITS_IRREL:
                continue
            if name in self.interface_spec["inputs_drop"]:
                continue
            fld_pdr, pos = self.pydra_fld_input(fld, name)
            meta_pdr = fld_pdr[-1]
            if "output_file_template" in meta_pdr:
                has_template.append(name)
            fields_pdr_dict[name] = (name,) + fld_pdr
            if pos is not None:
                position_dict[name] = pos

        fields_pdr_l = list(fields_pdr_dict.values())
        return fields_pdr_l, has_template

    def pydra_fld_input(self, field, nm):
        """converting a single nipype field to one element of fields for pydra input_spec"""
        tp_pdr = self.pydra_type_converter(field, spec_type="input", name=nm)
        if nm in self.interface_spec["inputs_metadata"]:
            metadata_extra_spec = self.interface_spec["inputs_metadata"][nm]
        else:
            metadata_extra_spec = {}

        if "default" in metadata_extra_spec:
            default_pdr = metadata_extra_spec.pop("default")
        elif (
            getattr(field, "usedefault")
            and field.default is not traits.ctrait.Undefined
        ):
            default_pdr = field.default
        else:
            default_pdr = None

        metadata_pdr = {"help_string": ""}
        for key in self.INPUT_KEYS:
            key_nm_pdr = self.NAME_MAPPING.get(key, key)
            val = getattr(field, key)
            if val is not None:
                if key == "argstr" and "%" in val:
                    val = self.string_formats(argstr=val, name=nm)
                metadata_pdr[key_nm_pdr] = val

        if getattr(field, "name_template"):
            template = getattr(field, "name_template")
            name_source = ensure_list(getattr(field, "name_source"))

            metadata_pdr["output_file_template"] = self.string_formats(
                argstr=template, name=name_source[0]
            )
            if tp_pdr in [specs.File, specs.Directory]:
                tp_pdr = str
        elif getattr(field, "genfile"):
            if nm in self.interface_spec["output_templates"]:
                metadata_pdr["output_file_template"] = self.interface_spec[
                    "output_templates"
                ][nm]
                if tp_pdr in [
                    specs.File,
                    specs.Directory,
                ]:  # since this is a template, the file doesn't exist
                    tp_pdr = str
            elif nm not in self.interface_spec["output_callables"]:
                raise Exception(
                    f"the filed {nm} has genfile=True, but no output template or callables provided"
                )

        metadata_pdr.update(metadata_extra_spec)

        pos = metadata_pdr.get("position", None)

        if default_pdr is not None and not metadata_pdr.get("mandatory", None):
            return (tp_pdr, default_pdr, metadata_pdr), pos
        else:
            return (tp_pdr, metadata_pdr), pos

    def convert_output_spec(self, fields_from_template):
        """creating fields list for pydra input spec"""
        fields_pdr_l = []
        for name, fld in self.nipype_output_spec.traits().items():
            if (
                name in self.interface_spec["output_requirements"]
                and name not in fields_from_template
            ):
                fld_pdr = self.pydra_fld_output(fld, name)
                fields_pdr_l.append((name,) + fld_pdr)
        return fields_pdr_l

    def pydra_fld_output(self, field, name):
        """converting a single nipype field to one element of fields for pydra output_spec"""
        tp_pdr = self.pydra_type_converter(field, spec_type="output", name=name)

        metadata_pdr = {}
        for key in self.OUTPUT_KEYS:
            key_nm_pdr = self.NAME_MAPPING.get(key, key)
            val = getattr(field, key)
            if val:
                metadata_pdr[key_nm_pdr] = val

        if self.interface_spec["output_requirements"][name]:
            if all(
                [
                    isinstance(el, list)
                    for el in self.interface_spec["output_requirements"][name]
                ]
            ):
                requires_l = self.interface_spec["output_requirements"][name]
                nested_flag = True
            elif all(
                [
                    isinstance(el, (str, dict))
                    for el in self.interface_spec["output_requirements"][name]
                ]
            ):
                requires_l = [self.interface_spec["output_requirements"][name]]
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

        if name in self.interface_spec["output_templates"]:
            metadata_pdr["output_file_template"] = self.interface_spec[
                "output_templates"
            ][name]
        elif name in self.interface_spec["output_callables"]:
            metadata_pdr["callable"] = self.interface_spec["output_callables"][name]
        return (tp_pdr, metadata_pdr)

    def function_callables(self):
        if not self.interface_spec["output_callables"]:
            return ""
        python_functions_spec = (
            Path(os.path.dirname(__file__)) / "../specs/callables.py"
        )
        if not python_functions_spec.exists():
            raise Exception(
                "specs/callables.py file is needed if output_callables in the spec files"
            )
        fun_str = ""
        fun_names = list(set(self.interface_spec["output_callables"].values()))
        fun_names.sort()
        for fun_nm in fun_names:
            fun = getattr(callables, fun_nm)
            fun_str += inspect.getsource(fun) + "\n"
        return fun_str

    def pydra_type_converter(self, field, spec_type, name):
        """converting types to types used in pydra"""
        if spec_type not in ["input", "output"]:
            raise Exception(
                f"spec_type has to be input or output, but {spec_type} provided"
            )
        tp = field.trait_type
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
        elif isinstance(tp, traits_extension.InputMultiObject):
            if isinstance(field.inner_traits[0].trait_type, traits_extension.File):
                tp_pdr = specs.MultiInputFile
            else:
                tp_pdr = specs.MultiInputObj
        elif isinstance(tp, traits_extension.OutputMultiObject):
            if isinstance(field.inner_traits[0].trait_type, traits_extension.File):
                tp_pdr = specs.MultiOutputFile
            else:
                tp_pdr = specs.MultiOutputObj
        elif isinstance(tp, traits.trait_types.List):
            if isinstance(field.inner_traits[0].trait_type, traits_extension.File):
                if spec_type == "input":
                    tp_pdr = specs.MultiInputFile
                else:
                    tp_pdr = specs.MultiOutputFile
            else:
                tp_pdr = list
        elif isinstance(tp, traits_extension.File):
            if (
                spec_type == "output" or tp.exists is True
            ):  # TODO check the hash_file metadata in nipype
                tp_pdr = specs.File
            else:
                tp_pdr = str
        else:
            tp_pdr = ty.Any
        return tp_pdr

    def string_formats(self, argstr, name):
        import re

        if "%s" in argstr:
            argstr_new = argstr.replace("%s", f"{{{name}}}")
        elif "%d" in argstr:
            argstr_new = argstr.replace("%d", f"{{{name}}}")
        elif "%f" in argstr:
            argstr_new = argstr.replace("%f", f"{{{name}}}")
        elif "%g" in argstr:
            argstr_new = argstr.replace("%g", f"{{{name}}}")
        elif len(re.findall("%[0-9.]+f", argstr)) == 1:
            old_format = re.findall("%[0-9.]+f", argstr)[0]
            argstr_new = argstr.replace(old_format, f"{{{name}:{old_format[1:]}}}")
        else:
            raise Exception(f"format from {argstr} is not supported TODO")
        return argstr_new


FSL_MODULES = [
    "aroma",
    "dti",
    "epi",
    "fix",
    "maths",
    "model",
    "possum",
    "preprocess",
    "utils",
]


@click.command()
@click.option(
    "-i",
    "--interface_name",
    required=True,
    default="all",
    help="name of the interface (name used in Nipype, e.g. BET) or all (default)"
    "if all is used all interfaces from the spec file will be created",
)
@click.option(
    "-m",
    "--module_name",
    required=True,
    help=f"name of the module from the list {FSL_MODULES}",
)
def create_pydra_spec(interface_name, module_name):
    if module_name not in FSL_MODULES:
        raise Exception(
            f"module name {module_name} not available;"
            f"should be from the list {FSL_MODULES}"
        )

    spec_file = (
        Path(os.path.dirname(__file__)) / f"../specs/fsl_{module_name}_param.yml"
    )
    if not spec_file.exists():
        raise Exception(
            f"the specification file doesn't exist for the module {module_name},"
            f"create the specification file in {spec_file.parent}"
        )

    @functools.lru_cache()
    def all_interfaces(module):
        nipype_module = getattr(fsl, module)
        all_specs = [el for el in dir(nipype_module) if "InputSpec" in el]
        all_interf = [el.replace("InputSpec", "") for el in all_specs]

        # interfaces in the spec file
        with open(spec_file) as f:
            spec_interf = yaml.safe_load(f).keys()

        if set(all_interf) - set(spec_interf):
            warnings.warn(
                f"some interfaces are not in the spec file: "
                f"{set(all_interf) - set(spec_interf)}, "
                f"and pydra interfaces will not be created for them"
            )
        return spec_interf

    if interface_name == "all":
        interface_list = all_interfaces(module_name)
    elif interface_name in all_interfaces(module_name):
        interface_list = [interface_name]
    else:
        raise Exception(
            f"interface_name has to be 'all' "
            f"or a name from the list {all_interfaces(module_name)}"
        )

    dirname_interf = Path(__file__).parent.parent / f"pydra/tasks/fsl/{module_name}"
    dirname_interf.mkdir(exist_ok=True)

    for interface_el in interface_list:
        converter = FSLConverter(
            interface_name=interface_el,
            interface_spec_file=Path(__file__).parent.parent
            / f"specs/fsl_{module_name}_param.yml",
        )
        converter.pydra_specs(write=True, dirname=dirname_interf)


if __name__ == "__main__":
    create_pydra_spec()
