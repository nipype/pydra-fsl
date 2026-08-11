from fileformats.generic import File
from fileformats.text import TextFile
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def out_file_callable(output_dir, inputs, stdout, stderr):
    raise NotImplementedError


@shell.define
class Text2Vest(shell.Task["Text2Vest.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.text import TextFile
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.text_2_vest import Text2Vest

    >>> task = Text2Vest()
    >>> task.in_file = TextFile.mock("design.txt")
    >>> task.cmdline
    'None'


    """

    executable = "Text2Vest"
    in_file: TextFile = shell.arg(
        help="plain text file representing your design, contrast, or f-test matrix",
        argstr="{in_file}",
        position=1,
    )
    out_file: Path = shell.arg(
        help="file name to store matrix data in the format used by FSL tools (e.g., design.mat, design.con design.fts)",
        argstr="{out_file}",
        position=2,
    )

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="matrix data in the format used by FSL tools",
            callable=out_file_callable,
        )
