import attrs
from fileformats.generic import File
from fileformats.medimage import Bval, Nifti1
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    keys_to_ignore = {"outputtype", "environ", "args"}

    opt_output = {"tensor": inputs["save_tensor"], "sse": inputs["sse"]}

    for output, input_flag in opt_output.items():
        if (input_flag is not attrs.NOTHING) and input_flag:

            continue
        keys_to_ignore.add(output)

    outputs = {}
    for k in set(outputs["keys"]()) - keys_to_ignore:
        outputs[k] = _gen_fname(
            inputs["base_name"],
            suffix="_" + k,
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    return outputs


def V1_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("V1")


def V2_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("V2")


def V3_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("V3")


def L1_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("L1")


def L2_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("L2")


def L3_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("L3")


def MD_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("MD")


def FA_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("FA")


def MO_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("MO")


def S0_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("S0")


def tensor_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("tensor")


def sse_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("sse")


@shell.define
class DTIFit(shell.Task["DTIFit.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Bval, Nifti1
    >>> from pydra.tasks.fsl.v6.dti.dti_fit import DTIFit

    >>> task = DTIFit()
    >>> task.dwi = Nifti1.mock("diffusion.nii")
    >>> task.mask = Nifti1.mock("mask.nii")
    >>> task.bvecs = File.mock()
    >>> task.bvals = Bval.mock("bvals")
    >>> task.cni = File.mock()
    >>> task.gradnonlin = File.mock()
    >>> task.cmdline
    'dtifit -k diffusion.nii -o TP -m mask.nii -r bvecs -b bvals'


    """

    executable = "dtifit"
    dwi: Nifti1 = shell.arg(
        help="diffusion weighted image data file", argstr="-k {dwi}", position=1
    )
    base_name: str = shell.arg(
        help="base_name that all output files will start with",
        argstr="-o {base_name}",
        position=2,
        default="dtifit_",
    )
    mask: Nifti1 = shell.arg(
        help="bet binary mask file", argstr="-m {mask}", position=3
    )
    bvecs: File = shell.arg(help="b vectors file", argstr="-r {bvecs}", position=4)
    bvals: Bval = shell.arg(help="b values file", argstr="-b {bvals}", position=5)
    min_z: int = shell.arg(help="min z", argstr="-z {min_z}")
    max_z: int = shell.arg(help="max z", argstr="-Z {max_z}")
    min_y: int = shell.arg(help="min y", argstr="-y {min_y}")
    max_y: int = shell.arg(help="max y", argstr="-Y {max_y}")
    min_x: int = shell.arg(help="min x", argstr="-x {min_x}")
    max_x: int = shell.arg(help="max x", argstr="-X {max_x}")
    save_tensor: bool = shell.arg(
        help="save the elements of the tensor", argstr="--save_tensor"
    )
    sse: bool = shell.arg(help="output sum of squared errors", argstr="--sse")
    cni: File = shell.arg(help="input counfound regressors", argstr="--cni={cni}")
    little_bit: bool = shell.arg(
        help="only process small area of brain", argstr="--littlebit"
    )
    gradnonlin: File = shell.arg(
        help="gradient non linearities", argstr="--gradnonlin={gradnonlin}"
    )

    class Outputs(shell.Outputs):
        V1: File | None = shell.out(
            help="path/name of file with the 1st eigenvector", callable=V1_callable
        )
        V2: File | None = shell.out(
            help="path/name of file with the 2nd eigenvector", callable=V2_callable
        )
        V3: File | None = shell.out(
            help="path/name of file with the 3rd eigenvector", callable=V3_callable
        )
        L1: File | None = shell.out(
            help="path/name of file with the 1st eigenvalue", callable=L1_callable
        )
        L2: File | None = shell.out(
            help="path/name of file with the 2nd eigenvalue", callable=L2_callable
        )
        L3: File | None = shell.out(
            help="path/name of file with the 3rd eigenvalue", callable=L3_callable
        )
        MD: File | None = shell.out(
            help="path/name of file with the mean diffusivity", callable=MD_callable
        )
        FA: File | None = shell.out(
            help="path/name of file with the fractional anisotropy",
            callable=FA_callable,
        )
        MO: File | None = shell.out(
            help="path/name of file with the mode of anisotropy", callable=MO_callable
        )
        S0: File | None = shell.out(
            help="path/name of file with the raw T2 signal with no diffusion weighting",
            callable=S0_callable,
        )
        tensor: File | None = shell.out(
            help="path/name of file with the 4D tensor volume", callable=tensor_callable
        )
        sse: File | None = shell.out(
            help="path/name of file with the summed squared error",
            callable=sse_callable,
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
        msg = "Unable to generate filename for command %s. " % "dtifit"
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
