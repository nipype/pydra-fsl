import attrs
from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import (
    fname_presuffix,
    split_filename,
)
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    formatted = argstr.format(**inputs)
    if name == "in_files":

        formatted = "-S %d %s" % (len(value), formatted)
    return formatted

    return argstr.format(**inputs)


def in_files_formatter(field, inputs):
    return _format_arg("in_files", field, inputs, argstr="{in_files}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    if inputs["number_classes"] is attrs.NOTHING:
        nclasses = 3
    else:
        nclasses = inputs["number_classes"]

    _gen_fname_opts = {}
    if inputs["out_basename"] is not attrs.NOTHING:
        _gen_fname_opts["basename"] = inputs["out_basename"]
        _gen_fname_opts["cwd"] = os.getcwd()
    else:
        _gen_fname_opts["basename"] = inputs["in_files"][-1]
        _gen_fname_opts["cwd"], _, _ = split_filename(_gen_fname_opts["basename"])

    outputs["tissue_class_map"] = _gen_fname(
        suffix="_seg",
        output_type=inputs["output_type"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
        **_gen_fname_opts,
    )
    if inputs["segments"]:
        outputs["tissue_class_files"] = []
        for i in range(nclasses):
            outputs["tissue_class_files"].append(
                _gen_fname(
                    suffix="_seg_%d" % i,
                    output_type=inputs["output_type"],
                    inputs=inputs["inputs"],
                    output_dir=inputs["output_dir"],
                    stderr=inputs["stderr"],
                    stdout=inputs["stdout"],
                    **_gen_fname_opts,
                )
            )
    if inputs["output_biascorrected"] is not attrs.NOTHING:
        outputs["restored_image"] = []
        if len(inputs["in_files"]) > 1:

            for val, f in enumerate(inputs["in_files"]):

                outputs["restored_image"].append(
                    _gen_fname(
                        suffix="_restore_%d" % (val + 1),
                        output_type=inputs["output_type"],
                        inputs=inputs["inputs"],
                        output_dir=inputs["output_dir"],
                        stderr=inputs["stderr"],
                        stdout=inputs["stdout"],
                        **_gen_fname_opts,
                    )
                )
        else:

            outputs["restored_image"].append(
                _gen_fname(
                    suffix="_restore",
                    output_type=inputs["output_type"],
                    inputs=inputs["inputs"],
                    output_dir=inputs["output_dir"],
                    stderr=inputs["stderr"],
                    stdout=inputs["stdout"],
                    **_gen_fname_opts,
                )
            )

    outputs["mixeltype"] = _gen_fname(
        suffix="_mixeltype",
        output_type=inputs["output_type"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
        **_gen_fname_opts,
    )
    if not inputs["no_pve"]:
        outputs["partial_volume_map"] = _gen_fname(
            suffix="_pveseg",
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
            **_gen_fname_opts,
        )
        outputs["partial_volume_files"] = []
        for i in range(nclasses):
            outputs["partial_volume_files"].append(
                _gen_fname(
                    suffix="_pve_%d" % i,
                    output_type=inputs["output_type"],
                    inputs=inputs["inputs"],
                    output_dir=inputs["output_dir"],
                    stderr=inputs["stderr"],
                    stdout=inputs["stdout"],
                    **_gen_fname_opts,
                )
            )
    if inputs["output_biasfield"]:
        outputs["bias_field"] = []
        if len(inputs["in_files"]) > 1:

            for val, f in enumerate(inputs["in_files"]):

                outputs["bias_field"].append(
                    _gen_fname(
                        suffix="_bias_%d" % (val + 1),
                        output_type=inputs["output_type"],
                        inputs=inputs["inputs"],
                        output_dir=inputs["output_dir"],
                        stderr=inputs["stderr"],
                        stdout=inputs["stdout"],
                        **_gen_fname_opts,
                    )
                )
        else:

            outputs["bias_field"].append(
                _gen_fname(
                    suffix="_bias",
                    output_type=inputs["output_type"],
                    inputs=inputs["inputs"],
                    output_dir=inputs["output_dir"],
                    stderr=inputs["stderr"],
                    stdout=inputs["stdout"],
                    **_gen_fname_opts,
                )
            )

    if inputs["probability_maps"]:
        outputs["probability_maps"] = []
        for i in range(nclasses):
            outputs["probability_maps"].append(
                _gen_fname(
                    suffix="_prob_%d" % i,
                    output_type=inputs["output_type"],
                    inputs=inputs["inputs"],
                    output_dir=inputs["output_dir"],
                    stderr=inputs["stderr"],
                    stdout=inputs["stdout"],
                    **_gen_fname_opts,
                )
            )
    return outputs


def tissue_class_map_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("tissue_class_map")


def tissue_class_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("tissue_class_files")


def restored_image_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("restored_image")


def mixeltype_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("mixeltype")


def partial_volume_map_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("partial_volume_map")


def partial_volume_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("partial_volume_files")


def bias_field_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("bias_field")


def probability_maps_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("probability_maps")


@shell.define
class FAST(shell.Task["FAST.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.preprocess.fast import FAST

    >>> task = FAST()
    >>> task.in_files = [Nifti1.mock("s"), Nifti1.mock("t"), Nifti1.mock("r"), Nifti1.mock("u"), Nifti1.mock("c"), Nifti1.mock("t"), Nifti1.mock("u"), Nifti1.mock("r"), Nifti1.mock("a"), Nifti1.mock("l"), Nifti1.mock("."), Nifti1.mock("n"), Nifti1.mock("i"), Nifti1.mock("i")]
    >>> task.init_transform = File.mock()
    >>> task.manual_seg = File.mock()
    >>> task.cmdline
    'None'


    """

    executable = "fast"
    in_files: list[Nifti1] = shell.arg(
        help="image, or multi-channel set of images, to be segmented",
        position=-1,
        formatter=in_files_formatter,
    )
    out_basename: Path = shell.arg(
        help="base name of output files", argstr="-o {out_basename}"
    )
    number_classes: ty.Any = shell.arg(
        help="number of tissue-type classes", argstr="-n {number_classes}"
    )
    output_biasfield: bool = shell.arg(help="output estimated bias field", argstr="-b")
    output_biascorrected: bool = shell.arg(
        help="output restored image (bias-corrected image)", argstr="-B"
    )
    img_type: ty.Any = shell.arg(
        help="int specifying type of image: (1 = T1, 2 = T2, 3 = PD)",
        argstr="-t {img_type}",
    )
    bias_iters: ty.Any = shell.arg(
        help="number of main-loop iterations during bias-field removal",
        argstr="-I {bias_iters}",
    )
    bias_lowpass: ty.Any = shell.arg(
        help="bias field smoothing extent (FWHM) in mm", argstr="-l {bias_lowpass}"
    )
    init_seg_smooth: ty.Any = shell.arg(
        help="initial segmentation spatial smoothness (during bias field estimation)",
        argstr="-f {init_seg_smooth:.3}",
    )
    segments: bool = shell.arg(
        help="outputs a separate binary image for each tissue type", argstr="-g"
    )
    init_transform: File = shell.arg(
        help="<standard2input.mat> initialise using priors",
        argstr="-a {init_transform}",
    )
    other_priors: list[File] = shell.arg(
        help="alternative prior images", argstr="-A {other_priors}"
    )
    no_pve: bool = shell.arg(
        help="turn off PVE (partial volume estimation)", argstr="--nopve"
    )
    no_bias: bool = shell.arg(help="do not remove bias field", argstr="-N")
    use_priors: bool = shell.arg(help="use priors throughout", argstr="-P")
    segment_iters: ty.Any = shell.arg(
        help="number of segmentation-initialisation iterations",
        argstr="-W {segment_iters}",
    )
    mixel_smooth: ty.Any = shell.arg(
        help="spatial smoothness for mixeltype", argstr="-R {mixel_smooth:.2}"
    )
    iters_afterbias: ty.Any = shell.arg(
        help="number of main-loop iterations after bias-field removal",
        argstr="-O {iters_afterbias}",
    )
    hyper: ty.Any = shell.arg(
        help="segmentation spatial smoothness", argstr="-H {hyper:.2}"
    )
    verbose: bool = shell.arg(help="switch on diagnostic messages", argstr="-v")
    manual_seg: File = shell.arg(
        help="Filename containing intensities", argstr="-s {manual_seg}"
    )
    probability_maps: bool = shell.arg(
        help="outputs individual probability maps", argstr="-p"
    )

    class Outputs(shell.Outputs):
        tissue_class_map: File | None = shell.out(
            help="path/name of binary segmented volume file one val for each class  _seg",
            callable=tissue_class_map_callable,
        )
        tissue_class_files: list[File] | None = shell.out(
            callable=tissue_class_files_callable
        )
        restored_image: list[File] | None = shell.out(callable=restored_image_callable)
        mixeltype: File | None = shell.out(
            help="path/name of mixeltype volume file _mixeltype",
            callable=mixeltype_callable,
        )
        partial_volume_map: File | None = shell.out(
            help="path/name of partial volume file _pveseg",
            callable=partial_volume_map_callable,
        )
        partial_volume_files: list[File] | None = shell.out(
            callable=partial_volume_files_callable
        )
        bias_field: list[File] | None = shell.out(callable=bias_field_callable)
        probability_maps: list[File] | None = shell.out(
            callable=probability_maps_callable
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
        msg = "Unable to generate filename for command %s. " % "fast"
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
