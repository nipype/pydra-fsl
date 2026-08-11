import attrs
from fileformats.datascience import TextMatrix
from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import (
    fname_presuffix,
    split_filename,
)
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _gen_filename(name, inputs):
    if name == "out_file":
        return _list_outputs(
            concat_xfm=inputs["concat_xfm"],
            in_file=inputs["in_file"],
            in_file2=inputs["in_file2"],
            invert_xfm=inputs["invert_xfm"],
            out_file=inputs["out_file"],
        )["out_file"]
    return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define(xor=[["concat_xfm", "fix_scale_skew", "invert_xfm"]])
class ConvertXFM(shell.Task["ConvertXFM.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.convert_xfm import ConvertXFM

    >>> task = ConvertXFM()
    >>> task.in_file = TextMatrix.mock("flirt.mat")
    >>> task.in_file2 = File.mock()
    >>> task.out_file = "flirt_inv.mat"
    >>> task.cmdline
    'convert_xfm -omat flirt_inv.mat -inverse flirt.mat'


    """

    executable = "convert_xfm"
    in_file: TextMatrix = shell.arg(
        help="input transformation matrix", argstr="{in_file}", position=-1
    )
    in_file2: File = shell.arg(
        help="second input matrix (for use with fix_scale_skew or concat_xfm)",
        argstr="{in_file2}",
        position=-2,
    )
    invert_xfm: bool = shell.arg(
        help="invert input transformation", argstr="-inverse", position=-3
    )
    concat_xfm: bool = shell.arg(
        help="write joint transformation of two input matrices",
        argstr="-concat",
        position=-3,
        requires=["in_file2"],
    )
    fix_scale_skew: bool = shell.arg(
        help="use secondary matrix to fix scale and skew",
        argstr="-fixscaleskew",
        position=-3,
        requires=["in_file2"],
    )

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="final transformation matrix",
            argstr="-omat {out_file}",
            position=1,
            path_template='"flirt_inv.mat"',
        )


def _list_outputs(
    concat_xfm=None, in_file=None, in_file2=None, invert_xfm=None, out_file=None
):
    outputs = {}
    outfile = out_file
    if outfile is attrs.NOTHING:
        _, infile1, _ = split_filename(in_file)
        if invert_xfm:
            outfile = fname_presuffix(
                infile1, suffix="_inv.mat", newpath=output_dir, use_ext=False
            )
        else:
            if concat_xfm:
                _, infile2, _ = split_filename(in_file2)
                outfile = fname_presuffix(
                    f"{infile1}_{infile2}",
                    suffix=".mat",
                    newpath=output_dir,
                    use_ext=False,
                )
            else:
                outfile = fname_presuffix(
                    infile1, suffix="_fix.mat", newpath=output_dir, use_ext=False
                )
    outputs["out_file"] = os.path.abspath(outfile)
    return outputs
