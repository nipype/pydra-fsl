import attrs
from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import load_json, save_json
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "mask_file":
        return ""
    if name == "op_string":
        if "-k %s" in inputs["op_string"]:
            if inputs["mask_file"] is not attrs.NOTHING:
                return inputs["op_string"] % inputs["mask_file"]
            else:
                raise ValueError("-k %s option in op_string requires mask_file")

    return argstr.format(**inputs)


def mask_file_formatter(field, inputs):
    return _format_arg("mask_file", field, inputs, argstr="")


def op_string_formatter(field, inputs):
    return _format_arg("op_string", field, inputs, argstr="{op_string}")


def aggregate_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)
    needed_outputs = ["out_stat"]

    outputs = {}

    outfile = os.path.join(os.getcwd(), "stat_result.json")
    if runtime is None:
        try:
            out_stat = load_json(outfile)["stat"]
        except OSError:
            return None.outputs
    else:
        out_stat = []
        for line in stdout.split("\n"):
            if line:
                values = line.split()
                if len(values) > 1:
                    out_stat.append([float(val) for val in values])
                else:
                    out_stat.extend([float(val) for val in values])
        if len(out_stat) == 1:
            out_stat = out_stat[0]
        save_json(outfile, dict(stat=out_stat))
    outputs["out_stat"] = out_stat
    return outputs


def out_stat_callable(output_dir, inputs, stdout, stderr):
    outputs = aggregate_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_stat")


@shell.define
class ImageStats(shell.Task["ImageStats.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fsl.v6.utils.image_stats import ImageStats

    >>> task = ImageStats()
    >>> task.in_file = File.mock(funcfile)
    >>> task.op_string = "-M"
    >>> task.mask_file = File.mock()
    >>> task.index_mask_file = File.mock()
    >>> task.cmdline
    'None'


    """

    executable = "fslstats"
    split_4d: bool = shell.arg(
        help="give a separate output line for each 3D volume of a 4D timeseries",
        argstr="-t",
        position=1,
    )
    in_file: File = shell.arg(
        help="input file to generate stats of", argstr="{in_file}", position=3
    )
    op_string: str = shell.arg(
        help="string defining the operation, options are applied in order, e.g. -M -l 10 -M will report the non-zero mean, apply a threshold and then report the new nonzero mean",
        position=4,
        formatter=op_string_formatter,
    )
    mask_file: File = shell.arg(
        help="mask file used for option -k %s", formatter=mask_file_formatter
    )
    index_mask_file: File = shell.arg(
        help="generate separate n submasks from indexMask, for indexvalues 1..n where n is the maximum index value in indexMask, and generate statistics for each submask",
        argstr="-K {index_mask_file}",
        position=2,
    )

    class Outputs(shell.Outputs):
        out_stat: ty.Any | None = shell.out(
            help="stats output", callable=out_stat_callable
        )
