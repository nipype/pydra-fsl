"""
Orient
======

Change the orientation of an image.

Examples
--------

>>> import tempfile
>>> input_file = tempfile.NamedTemporaryFile(suffix="input.nii")

Change orientation to radiological:

>>> task = Orient(input_image=input_file.name, force_radiological=True)
>>> task.cmdline  # doctest: +ELLIPSIS
'fslorient -forceradiological ...input.nii'

Change orientation to neurological:

>>> task = Orient(input_image=input_file.name, force_neurological=True)
>>> task.cmdline  # doctest: +ELLIPSIS
'fslorient -forceneurological ...input.nii'

Swap between radiological and neurological:

>>> task = Orient(input_image=input_file.name, swap_orientation=True)
>>> task.cmdline  # doctest: +ELLIPSIS
'fslorient -swaporient ...input.nii'

Delete orientation:

>>> task = Orient(input_image=input_file.name, delete_orientation=True)
>>> task.cmdline  # doctest: +ELLIPSIS
'fslorient -deleteorient ...input.nii'
"""

__all__ = ["Orient"]

from attrs import define, field
from pydra.engine.specs import File, ShellOutSpec, ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class OrientSpec(ShellSpec):
    """Specifications for fslorient."""

    _xor = {
        "delete_orientation",
        "force_radiological",
        "force_neurological",
        "swap_orientation",
    }

    input_image: File = field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "",
            "position": -1,
            "copyfile": True,
        }
    )

    delete_orientation: bool = field(
        metadata={
            "help_string": "delete orientation",
            "argstr": "-deleteorient",
            "xor": _xor,
        }
    )

    force_radiological: bool = field(
        metadata={
            "help_string": "force orientation to radiological",
            "argstr": "-forceradiological",
            "xor": _xor,
        }
    )

    force_neurological: bool = field(
        metadata={
            "help_string": "force orientation to neurological",
            "argstr": "-forceneurological",
            "xor": _xor,
        }
    )

    swap_orientation: bool = field(
        metadata={
            "help_string": "swap between radiological and neurological",
            "argstr": "-swaporient",
            "xor": _xor,
        }
    )


@define(kw_only=True)
class OrientOutSpec(ShellOutSpec):
    """Output specifications for fslorient."""

    output_image: File = field(
        metadata={
            "help_string": "output image",
            "output_file_template": "{input_image}",
        }
    )


class Orient(ShellCommandTask):
    """Task definition for fslorient."""

    executable = "fslorient"

    input_spec = SpecInfo(name="Input", bases=(OrientSpec,))

    output_spec = SpecInfo(name="Output", bases=(OrientOutSpec,))
