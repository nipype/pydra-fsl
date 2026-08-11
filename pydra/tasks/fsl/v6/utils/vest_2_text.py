from fileformats.datascience import TextMatrix
from fileformats.generic import File
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def out_file_callable(output_dir, inputs, stdout, stderr):
    raise NotImplementedError


@shell.define
class Vest2Text(shell.Task["Vest2Text.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.vest_2_text import Vest2Text

    >>> task = Vest2Text()
    >>> task.in_file = TextMatrix.mock("design.mat")
    >>> task.cmdline
    'None'


    """

    executable = "Vest2Text"
    in_file: TextMatrix = shell.arg(
        help="matrix data stored in the format used by FSL tools",
        argstr="{in_file}",
        position=1,
    )
    out_file: Path = shell.arg(
        help="file name to store text output from matrix",
        argstr="{out_file}",
        position=2,
        default="design.txt",
    )

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="plain text representation of FSL matrix", callable=out_file_callable
        )
