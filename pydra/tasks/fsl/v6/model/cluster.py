import attrs
from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name in list(parsed_inputs["filemap"].keys()):
        if isinstance(value, bool):
            fname = _list_outputs(
                in_file=inputs["in_file"], output_type=inputs["output_type"]
            )[name[4:]]
        else:
            fname = value
        return argstr.format(**{name: fname})

    return argstr.format(**inputs)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)
    self_dict = {}

    outputs = {}
    for key, suffix in list(parsed_inputs["filemap"].items()):
        outkey = key[4:]
        inval = getattr(self_dict["inputs"], key)
        if inval is not attrs.NOTHING:
            if isinstance(inval, bool):
                if inval:
                    change_ext = True
                    if suffix.endswith(".txt"):
                        change_ext = False
                    outputs[outkey] = _gen_fname(
                        inputs["in_file"],
                        suffix="_" + suffix,
                        change_ext=change_ext,
                        output_type=inputs["output_type"],
                        inputs=inputs["inputs"],
                        output_dir=inputs["output_dir"],
                        stderr=inputs["stderr"],
                        stdout=inputs["stdout"],
                    )
            else:
                outputs[outkey] = os.path.abspath(inval)
    return outputs


def index_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("index_file")


def threshold_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("threshold_file")


def localmax_txt_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("localmax_txt_file")


def localmax_vol_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("localmax_vol_file")


def size_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("size_file")


def max_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("max_file")


def mean_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("mean_file")


def pval_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("pval_file")


@shell.define
class Cluster(shell.Task["Cluster.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fsl.v6.model.cluster import Cluster

    >>> task = Cluster()
    >>> task.in_file = File.mock()
    >>> task.threshold = 2.3
    >>> task.out_localmax_txt_file = "stats.txt"
    >>> task.cope_file = File.mock()
    >>> task.xfm_file = File.mock()
    >>> task.std_space_file = File.mock()
    >>> task.warpfield_file = File.mock()
    >>> task.cmdline
    'cluster --in=zstat1.nii.gz --olmax=stats.txt --thresh=2.3000000000 --mm'


    """

    executable = "cluster"
    in_file: File = shell.arg(help="input volume", argstr="--in={in_file}")
    threshold: float = shell.arg(
        help="threshold for input volume", argstr="--thresh={threshold:.10}"
    )
    out_index_file: ty.Any = shell.arg(
        help="output of cluster index (in size order)",
        argstr="--oindex={out_index_file}",
    )
    out_threshold_file: ty.Any = shell.arg(
        help="thresholded image", argstr="--othresh={out_threshold_file}"
    )
    out_localmax_txt_file: ty.Any = shell.arg(
        help="local maxima text file", argstr="--olmax={out_localmax_txt_file}"
    )
    out_localmax_vol_file: ty.Any = shell.arg(
        help="output of local maxima volume", argstr="--olmaxim={out_localmax_vol_file}"
    )
    out_size_file: ty.Any = shell.arg(
        help="filename for output of size image", argstr="--osize={out_size_file}"
    )
    out_max_file: ty.Any = shell.arg(
        help="filename for output of max image", argstr="--omax={out_max_file}"
    )
    out_mean_file: ty.Any = shell.arg(
        help="filename for output of mean image", argstr="--omean={out_mean_file}"
    )
    out_pval_file: ty.Any = shell.arg(
        help="filename for image output of log pvals", argstr="--opvals={out_pval_file}"
    )
    pthreshold: float = shell.arg(
        help="p-threshold for clusters",
        argstr="--pthresh={pthreshold:.10}",
        requires=["dlh", "volume"],
    )
    peak_distance: float = shell.arg(
        help="minimum distance between local maxima/minima, in mm (default 0)",
        argstr="--peakdist={peak_distance:.10}",
    )
    cope_file: File = shell.arg(help="cope volume", argstr="--cope={cope_file}")
    volume: int = shell.arg(
        help="number of voxels in the mask", argstr="--volume={volume}"
    )
    dlh: float = shell.arg(
        help="smoothness estimate = sqrt(det(Lambda))", argstr="--dlh={dlh:.10}"
    )
    fractional: bool = shell.arg(
        help="interprets the threshold as a fraction of the robust range",
        argstr="--fractional",
        default=False,
    )
    connectivity: int = shell.arg(
        help="the connectivity of voxels (default 26)",
        argstr="--connectivity={connectivity}",
    )
    use_mm: bool = shell.arg(
        help="use mm, not voxel, coordinates", argstr="--mm", default=False
    )
    find_min: bool = shell.arg(
        help="find minima instead of maxima", argstr="--min", default=False
    )
    no_table: bool = shell.arg(
        help="suppresses printing of the table info", argstr="--no_table", default=False
    )
    minclustersize: bool = shell.arg(
        help="prints out minimum significant cluster size",
        argstr="--minclustersize",
        default=False,
    )
    xfm_file: File = shell.arg(
        help="filename for Linear: input->standard-space transform. Non-linear: input->highres transform",
        argstr="--xfm={xfm_file}",
    )
    std_space_file: File = shell.arg(
        help="filename for standard-space volume", argstr="--stdvol={std_space_file}"
    )
    num_maxima: int = shell.arg(
        help="no of local maxima to report", argstr="--num={num_maxima}"
    )
    warpfield_file: File = shell.arg(
        help="file containing warpfield", argstr="--warpvol={warpfield_file}"
    )

    class Outputs(shell.Outputs):
        index_file: File | None = shell.out(
            help="output of cluster index (in size order)", callable=index_file_callable
        )
        threshold_file: File | None = shell.out(
            help="thresholded image", callable=threshold_file_callable
        )
        localmax_txt_file: File | None = shell.out(
            help="local maxima text file", callable=localmax_txt_file_callable
        )
        localmax_vol_file: File | None = shell.out(
            help="output of local maxima volume", callable=localmax_vol_file_callable
        )
        size_file: File | None = shell.out(
            help="filename for output of size image", callable=size_file_callable
        )
        max_file: File | None = shell.out(
            help="filename for output of max image", callable=max_file_callable
        )
        mean_file: File | None = shell.out(
            help="filename for output of mean image", callable=mean_file_callable
        )
        pval_file: File | None = shell.out(
            help="filename for image output of log pvals", callable=pval_file_callable
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
        msg = "Unable to generate filename for command %s. " % "cluster"
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
