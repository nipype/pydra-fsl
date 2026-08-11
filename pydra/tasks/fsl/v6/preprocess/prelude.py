import attrs
from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _gen_filename(name, inputs):
    if name == "unwrapped_phase_file":
        return _list_outputs(
            complex_phase_file=inputs["complex_phase_file"],
            output_type=inputs["output_type"],
            phase_file=inputs["phase_file"],
            unwrapped_phase_file=inputs["unwrapped_phase_file"],
        )["unwrapped_phase_file"]
    return None


def unwrapped_phase_file_default(inputs):
    return _gen_filename("unwrapped_phase_file", inputs=inputs)


@shell.define(
    xor=[
        ["complex_phase_file", "magnitude_file"],
        ["complex_phase_file", "magnitude_file", "phase_file"],
        ["complex_phase_file", "phase_file"],
        ["labelprocess2d", "process2d"],
        ["labelprocess2d", "process2d", "process3d"],
    ]
)
class PRELUDE(shell.Task["PRELUDE.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.preprocess.prelude import PRELUDE

    """

    executable = "prelude"
    complex_phase_file: File | None = shell.arg(
        help="complex phase input volume", argstr="--complex={complex_phase_file}"
    )
    magnitude_file: File | None = shell.arg(
        help="file containing magnitude image", argstr="--abs={magnitude_file}"
    )
    phase_file: File | None = shell.arg(
        help="raw phase file", argstr="--phase={phase_file}"
    )
    num_partitions: int = shell.arg(
        help="number of phase partitions to use",
        argstr="--numphasesplit={num_partitions}",
    )
    labelprocess2d: bool = shell.arg(
        help="does label processing in 2D (slice at a time)", argstr="--labelslices"
    )
    process2d: bool = shell.arg(
        help="does all processing in 2D (slice at a time)", argstr="--slices"
    )
    process3d: bool = shell.arg(
        help="forces all processing to be full 3D", argstr="--force3D"
    )
    threshold: float = shell.arg(
        help="intensity threshold for masking", argstr="--thresh={threshold:.10}"
    )
    mask_file: File = shell.arg(
        help="filename of mask input volume", argstr="--mask={mask_file}"
    )
    start: int = shell.arg(
        help="first image number to process (default 0)", argstr="--start={start}"
    )
    end: int = shell.arg(
        help="final image number to process (default Inf)", argstr="--end={end}"
    )
    savemask_file: File = shell.arg(
        help="saving the mask volume", argstr="--savemask={savemask_file}"
    )
    rawphase_file: File = shell.arg(
        help="saving the raw phase output", argstr="--rawphase={rawphase_file}"
    )
    label_file: File = shell.arg(
        help="saving the area labels output", argstr="--labels={label_file}"
    )
    removeramps: bool = shell.arg(
        help="remove phase ramps during unwrapping", argstr="--removeramps"
    )

    class Outputs(shell.Outputs):
        unwrapped_phase_file: Path = shell.outarg(
            help="file containing unwrapepd phase",
            argstr="--unwrap={unwrapped_phase_file}",
            path_template="unwrapped_phase_file",
        )


def _gen_fname(
    basename, cwd=None, suffix=None, change_ext=True, ext=None, output_type=None
):
    """Generate a filename based on the given parameters.

    The filename will take the form: cwd/basename<suffix><ext>.
    If change_ext is True, it will use the extensions specified in
    <instance>inputs.output_type.

    Parameters
    ----------
    basename : str
        Filename to base the new filename on.
    cwd : str
        Path to prefix to the new filename. (default is output_dir)
    suffix : str
        Suffix to add to the `basename`.  (defaults is '' )
    change_ext : bool
        Flag to change the filename extension to the FSL output type.
        (default True)

    Returns
    -------
    fname : str
        New filename based on given parameters.

    """

    if basename == "":
        msg = "Unable to generate filename for command %s. " % "prelude"
        msg += "basename is not set!"
        raise ValueError(msg)
    if cwd is None:
        cwd = output_dir
    if ext is None:
        ext = Info.output_type_to_ext(output_type)
    if change_ext:
        if suffix:
            suffix = f"{suffix}{ext}"
        else:
            suffix = ext
    if suffix is None:
        suffix = ""
    fname = fname_presuffix(basename, suffix=suffix, use_ext=False, newpath=cwd)
    return fname


def _list_outputs(
    complex_phase_file=None,
    output_type=None,
    phase_file=None,
    unwrapped_phase_file=None,
):
    outputs = {}
    out_file = unwrapped_phase_file
    if out_file is attrs.NOTHING:
        if phase_file is not attrs.NOTHING:
            out_file = _gen_fname(
                phase_file, suffix="_unwrapped", output_type=output_type
            )
        elif complex_phase_file is not attrs.NOTHING:
            out_file = _gen_fname(
                complex_phase_file, suffix="_phase_unwrapped", output_type=output_type
            )
    outputs["unwrapped_phase_file"] = os.path.abspath(out_file)
    return outputs


IFLOGGER = logging.getLogger("nipype.interface")
