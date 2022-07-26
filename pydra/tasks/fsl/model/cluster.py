from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty


def Cluster_output(inputs):
    import attr
    from pydra.engine.helpers_file import split_filename

    in_file = inputs.in_file

    if in_file not in [None, attr.NOTHING]:
        pth, fname, ext = split_filename(in_file)
        return f"{fname}_localmax.txt"
    else:
        raise Exception(f"this function should be run only for out_localmax_txt_file not {name}")


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
        str,
        {
            "help_string": "output of cluster index (in size order)",
            "argstr": "--oindex={out_index_file}",
            "output_file_template": "{in_file}_index",
        },
    ),
    (
        "out_threshold_file",
        str,
        {
            "help_string": "thresholded image",
            "argstr": "--othresh={out_threshold_file}",
            "output_file_template": "{in_file}_threshold",
        },
    ),
    (
        "out_localmax_txt_file",
        str,
        {
            "help_string": "local maxima text file",
            "argstr": "--olmax={out_localmax_txt_file}",
            "output_file_template": Cluster_output,
        },
    ),
    (
        "out_localmax_vol_file",
        str,
        {
            "help_string": "output of local maxima volume",
            "argstr": "--olmaxim={out_localmax_vol_file}",
            "output_file_template": "{in_file}_localmax",
        },
    ),
    (
        "out_size_file",
        str,
        {
            "help_string": "filename for output of size image",
            "argstr": "--osize={out_size_file}",
            "output_file_template": "{in_file}_size",
        },
    ),
    (
        "out_max_file",
        str,
        {
            "help_string": "filename for output of max image",
            "argstr": "--omax={out_max_file}",
            "output_file_template": "{in_file}_max",
        },
    ),
    (
        "out_mean_file",
        str,
        {
            "help_string": "filename for output of mean image",
            "argstr": "--omean={out_mean_file}",
            "output_file_template": "{in_file}_mean",
        },
    ),
    (
        "out_pval_file",
        str,
        {
            "help_string": "filename for image output of log pvals",
            "argstr": "--opvals={out_pval_file}",
            "output_file_template": "{in_file}_pval",
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
Cluster_input_spec = specs.SpecInfo(name="Input", fields=input_fields, bases=(specs.ShellSpec,))

output_fields = []
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
    >>> task.cmdline # doctest: +ELLIPSIS
    'cluster --in=zstat1.nii.gz --thresh=2.3000000000 --mm' 
    """

    input_spec = Cluster_input_spec
    output_spec = Cluster_output_spec
    executable = "cluster"
