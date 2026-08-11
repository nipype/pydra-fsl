from fileformats.generic import File
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def out_file_callable(output_dir, inputs, stdout, stderr):
    return inputs.dest_file


@shell.define
class CopyGeom(shell.Task["CopyGeom.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.copy_geom import CopyGeom

    """

    executable = "fslcpgeom"
    in_file: File = shell.arg(help="source image", argstr="{in_file}", position=1)
    dest_file: Path = shell.arg(
        help="destination image",
        argstr="{dest_file}",
        position=2,
        copy_mode="File.CopyMode.copy",
    )
    ignore_dims: bool = shell.arg(
        help="Do not copy image dimensions", argstr="-d", position=-1
    )

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="image with new geometry header", callable=out_file_callable
        )
