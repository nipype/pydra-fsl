import attrs
from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["dyads"] = _gen_fname(
        inputs["output"],
        output_type=inputs["output_type"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    outputs["dispersion"] = _gen_fname(
        inputs["output"],
        suffix="_dispersion",
        output_type=inputs["output_type"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )

    return outputs


def dyads_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("dyads")


def dispersion_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("dispersion")


@shell.define
class MakeDyadicVectors(shell.Task["MakeDyadicVectors.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fsl.v6.dti.make_dyadic_vectors import MakeDyadicVectors

    """

    executable = "make_dyadic_vectors"
    theta_vol: File = shell.arg(help="", argstr="{theta_vol}", position=1)
    phi_vol: File = shell.arg(help="", argstr="{phi_vol}", position=2)
    mask: File = shell.arg(help="", argstr="{mask}", position=3)
    output: File = shell.arg(help="", argstr="{output}", position=4, default="dyads")
    perc: float = shell.arg(
        help="the {perc}% angle of the output cone of uncertainty (output will be in degrees)",
        argstr="{perc}",
        position=5,
    )

    class Outputs(shell.Outputs):
        dyads: File | None = shell.out(callable=dyads_callable)
        dispersion: File | None = shell.out(callable=dispersion_callable)


def _gen_fname(
    basename,
    cwd=None,
    suffix=None,
    change_ext=True,
    ext=None,
    output_type=None,
    inputs=None,
    output_dir=None,
    stderr=None,
    stdout=None,
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
        msg = "Unable to generate filename for command %s. " % "make_dyadic_vectors"
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


IFLOGGER = logging.getLogger("nipype.interface")
