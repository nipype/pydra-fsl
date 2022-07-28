from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty


def Cluster_output(field, inputs):
    import os, attr
    from pydra.engine.helpers_file import split_filename

    in_file = inputs.in_file
    name = field.name
    pth, fname, ext = split_filename(in_file)

    if name == "out_index_file":
        return os.path.join(pth, f"{fname}_index{ext}")
    elif name == "out_localmax_txt_file":
        return os.path.join(pth, f"{fname}_localmax.txt")
    elif name == "out_localmax_vol_file":
        return os.path.join(pth, f"{fname}_localmax{ext}")
    elif name == "out_max_file":
        return os.path.join(pth, f"{fname}_max{ext}")
    elif name == "out_mean_file":
        return os.path.join(pth, f"{fname}_mean{ext}")
    elif name == "out_pval_file":
        return os.path.join(pth, f"{fname}_pval{ext}")
    elif name == "out_size_file":
        return os.path.join(pth, f"{fname}_size{ext}")
    elif name == "out_threshold_file":
        return os.path.join(pth, f"{fname}_threshold{ext}")

    else:
        raise Exception(
            f"this function should be run only for index_file, localmax_txt_file, localmax_vol_file, max_file, mean_file, pval_file, size_file, or threshold_file not {name}"
        )


input_fields = [
    (
        "in_file",
        specs.File,
        {"help_string": "input volume", "argstr": "--in={in_file}", "mandatory": True},
    ),
    (
        "threshold",
        float,
        {
            "help_string": "threshold for input volume",
            "argstr": "--thresh={threshold:.10f}",
            "mandatory": True,
        },
    ),
    (
        "out_index_file",
        ty.Any,
        {
            "help_string": "output of cluster index (in size order)",
            "argstr": "--oindex={out_index_file}",
        },
    ),
    (
        "out_threshold_file",
        ty.Any,
        {
            "help_string": "thresholded image",
            "argstr": "--othresh={out_threshold_file}",
        },
    ),
    (
        "out_localmax_txt_file",
        ty.Any,
        {
            "help_string": "local maxima text file",
            "argstr": "--olmax={out_localmax_txt_file}",
        },
    ),
    (
        "out_localmax_vol_file",
        ty.Any,
        {
            "help_string": "output of local maxima volume",
            "argstr": "--olmaxim={out_localmax_vol_file}",
        },
    ),
    (
        "out_size_file",
        ty.Any,
        {
            "help_string": "filename for output of size image",
            "argstr": "--osize={out_size_file}",
        },
    ),
    (
        "out_max_file",
        ty.Any,
        {
            "help_string": "filename for output of max image",
            "argstr": "--omax={out_max_file}",
        },
    ),
    (
        "out_mean_file",
        ty.Any,
        {
            "help_string": "filename for output of mean image",
            "argstr": "--omean={out_mean_file}",
        },
    ),
    (
        "out_pval_file",
        ty.Any,
        {
            "help_string": "filename for image output of log pvals",
            "argstr": "--opvals={out_pval_file}",
        },
    ),
    (
        "pthreshold",
        float,
        {
            "help_string": "p-threshold for clusters",
            "argstr": "--pthresh={pthreshold:.10f}",
            "requires": ["dlh", "volume"],
        },
    ),
    (
        "peak_distance",
        float,
        {
            "help_string": "minimum distance between local maxima/minima, in mm (default 0)",
            "argstr": "--peakdist={peak_distance:.10f}",
        },
    ),
    ("cope_file", str, {"help_string": "cope volume", "argstr": "--cope={cope_file}"}),
    (
        "volume",
        int,
        {"help_string": "number of voxels in the mask", "argstr": "--volume={volume}"},
    ),
    (
        "dlh",
        float,
        {
            "help_string": "smoothness estimate = sqrt(det(Lambda))",
            "argstr": "--dlh={dlh:.10f}",
        },
    ),
    (
        "fractional",
        bool,
        False,
        {
            "help_string": "interprets the threshold as a fraction of the robust range",
            "argstr": "--fractional",
        },
    ),
    (
        "connectivity",
        int,
        {
            "help_string": "the connectivity of voxels (default 26)",
            "argstr": "--connectivity={connectivity}",
        },
    ),
    (
        "use_mm",
        bool,
        False,
        {"help_string": "use mm, not voxel, coordinates", "argstr": "--mm"},
    ),
    (
        "find_min",
        bool,
        False,
        {"help_string": "find minima instead of maxima", "argstr": "--min"},
    ),
    (
        "no_table",
        bool,
        False,
        {
            "help_string": "suppresses printing of the table info",
            "argstr": "--no_table",
        },
    ),
    (
        "minclustersize",
        bool,
        False,
        {
            "help_string": "prints out minimum significant cluster size",
            "argstr": "--minclustersize",
        },
    ),
    (
        "xfm_file",
        str,
        {
            "help_string": "filename for Linear: input->standard-space transform. Non-linear: input->highres transform",
            "argstr": "--xfm={xfm_file}",
        },
    ),
    (
        "std_space_file",
        str,
        {
            "help_string": "filename for standard-space volume",
            "argstr": "--stdvol={std_space_file}",
        },
    ),
    (
        "num_maxima",
        int,
        {"help_string": "no of local maxima to report", "argstr": "--num={num_maxima}"},
    ),
    (
        "warpfield_file",
        str,
        {
            "help_string": "file contining warpfield",
            "argstr": "--warpvol={warpfield_file}",
        },
    ),
]
Cluster_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_index_file",
        specs.File,
        {
            "help_string": "output of cluster index (in size order)",
            "requires": ["in_file", "out_index_file"],
            "callable": Cluster_output,
        },
    ),
    (
        "out_threshold_file",
        specs.File,
        {
            "help_string": "thresholded image",
            "requires": ["in_file", "out_threshold_file"],
            "callable": Cluster_output,
        },
    ),
    (
        "out_localmax_txt_file",
        specs.File,
        {
            "help_string": "local maxima text file",
            "requires": ["in_file", "out_localmax_txt_file"],
            "callable": Cluster_output,
        },
    ),
    (
        "out_localmax_vol_file",
        specs.File,
        {
            "help_string": "output of local maxima volume",
            "requires": ["in_file", "out_localmax_vol_file"],
            "callable": Cluster_output,
        },
    ),
    (
        "out_size_file",
        specs.File,
        {
            "help_string": "filename for output of size image",
            "requires": ["in_file", "out_size_file"],
            "callable": Cluster_output,
        },
    ),
    (
        "out_max_file",
        specs.File,
        {
            "help_string": "filename for output of max image",
            "requires": ["in_file", "out_max_file"],
            "callable": Cluster_output,
        },
    ),
    (
        "out_mean_file",
        specs.File,
        {
            "help_string": "filename for output of mean image",
            "requires": ["in_file", "out_mean_file"],
            "callable": Cluster_output,
        },
    ),
    (
        "out_pval_file",
        specs.File,
        {
            "help_string": "filename for image output of log pvals",
            "requires": ["in_file", "out_pval_file"],
            "callable": Cluster_output,
        },
    ),
]
Cluster_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Cluster(ShellCommandTask):
    """
    Example
    -------
    >>> task = Cluster()
    >>> task.inputs.in_file = "zstat1.nii.gz"
    >>> task.inputs.threshold = 2.3
    >>> task.inputs.use_mm = True
    >>> task.inputs.out_index_file = "zstat1_index.nii.gz"
    >>> task.inputs.out_threshold_file = "zstat1_threshold.nii.gz"
    >>> task.inputs.out_localmax_txt_file = "zstat1_localmax.txt"
    >>> task.inputs.out_localmax_vol_file = "zstat1_localmax.nii.gz"
    >>> task.inputs.out_size_file = "zstat1_size.nii.gz"
    >>> task.inputs.out_max_file = "zstat1_max.nii.gz"
    >>> task.inputs.out_mean_file = "zstat1_mean.nii.gz"
    >>> task.inputs.out_pval_file = "zstat1_pval.nii.gz"
    >>> task.cmdline
    'cluster --in=zstat1.nii.gz --thresh=2.3000000000 --oindex=zstat1_index.nii.gz --othresh=zstat1_threshold.nii.gz --olmax=zstat1_localmax.txt --olmaxim=zstat1_localmax.nii.gz --osize=zstat1_size.nii.gz --omax=zstat1_max.nii.gz --omean=zstat1_mean.nii.gz --opvals=zstat1_pval.nii.gz --mm'
    """

    input_spec = Cluster_input_spec
    output_spec = Cluster_output_spec
    executable = "cluster"
