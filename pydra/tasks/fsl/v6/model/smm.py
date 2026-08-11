import attrs
from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}

    outputs["null_p_map"] = _gen_fname(
        basename="w1_mean",
        cwd="logdir",
        output_type=inputs["output_type"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    outputs["activation_p_map"] = _gen_fname(
        basename="w2_mean",
        cwd="logdir",
        output_type=inputs["output_type"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    if (inputs["no_deactivation_class"] is attrs.NOTHING) or not inputs[
        "no_deactivation_class"
    ]:
        outputs["deactivation_p_map"] = _gen_fname(
            basename="w3_mean",
            cwd="logdir",
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    return outputs


def null_p_map_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("null_p_map")


def activation_p_map_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("activation_p_map")


def deactivation_p_map_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("deactivation_p_map")


@shell.define
class SMM(shell.Task["SMM.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fsl.v6.model.smm import SMM

    """

    executable = "mm --ld=logdir"
    spatial_data_file: File = shell.arg(
        help="statistics spatial map", argstr='--sdf="{spatial_data_file}"', position=1
    )
    mask: File = shell.arg(help="mask file", argstr='--mask="{mask}"', position=2)
    no_deactivation_class: bool = shell.arg(
        help="enforces no deactivation class", argstr="--zfstatmode", position=3
    )

    class Outputs(shell.Outputs):
        null_p_map: File | None = shell.out(callable=null_p_map_callable)
        activation_p_map: File | None = shell.out(callable=activation_p_map_callable)
        deactivation_p_map: File | None = shell.out(
            callable=deactivation_p_map_callable
        )


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
        msg = "Unable to generate filename for command %s. " % "mm --ld=logdir"
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
