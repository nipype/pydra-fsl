from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "help_string": "input file",
            "argstr": "-in {in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "reference",
        specs.File,
        {
            "help_string": "reference file",
            "argstr": "-ref {reference}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "out_file",
        str,
        {
            "help_string": "registered output file",
            "argstr": "-out {out_file}",
            "position": 2,
            "output_file_template": "{in_file}_flirt",
        },
    ),
    (
        "out_matrix_file",
        str,
        {
            "help_string": "output affine matrix in 4x4 asciii format",
            "argstr": "-omat {out_matrix_file}",
            "position": 3,
            "output_file_template": "{in_file}_flirt.mat",
        },
    ),
    (
        "out_log",
        str,
        {
            "help_string": "output log",
            "requires": ["save_log"],
            "output_file_template": "{in_file}_flirt.log",
        },
    ),
    (
        "in_matrix_file",
        str,
        {"help_string": "input 4x4 affine matrix", "argstr": "-init {in_matrix_file}"},
    ),
    (
        "apply_xfm",
        bool,
        {
            "help_string": "apply transformation supplied by in_matrix_file or uses_qform to use the affine matrix stored in the reference header",
            "argstr": "-applyxfm",
        },
    ),
    (
        "apply_isoxfm",
        float,
        {
            "help_string": "as applyxfm but forces isotropic resampling",
            "argstr": "-applyisoxfm {apply_isoxfm}",
            "xor": ["apply_xfm"],
        },
    ),
    (
        "datatype",
        ty.Any,
        {"help_string": "force output data type", "argstr": "-datatype {datatype}"},
    ),
    ("cost", ty.Any, {"help_string": "cost function", "argstr": "-cost {cost}"}),
    (
        "cost_func",
        ty.Any,
        {"help_string": "cost function", "argstr": "-searchcost {cost_func}"},
    ),
    (
        "uses_qform",
        bool,
        {"help_string": "initialize using sform or qform", "argstr": "-usesqform"},
    ),
    (
        "display_init",
        bool,
        {"help_string": "display initial matrix", "argstr": "-displayinit"},
    ),
    (
        "angle_rep",
        ty.Any,
        {
            "help_string": "representation of rotation angles",
            "argstr": "-anglerep {angle_rep}",
        },
    ),
    (
        "interp",
        ty.Any,
        {
            "help_string": "final interpolation method used in reslicing",
            "argstr": "-interp {interp}",
        },
    ),
    (
        "sinc_width",
        int,
        {"help_string": "full-width in voxels", "argstr": "-sincwidth {sinc_width}"},
    ),
    (
        "sinc_window",
        ty.Any,
        {"help_string": "sinc window", "argstr": "-sincwindow {sinc_window}"},
    ),
    (
        "bins",
        int,
        {"help_string": "number of histogram bins", "argstr": "-bins {bins}"},
    ),
    (
        "dof",
        int,
        {
            "help_string": "number of transform degrees of freedom",
            "argstr": "-dof {dof}",
        },
    ),
    (
        "no_resample",
        bool,
        {"help_string": "do not change input sampling", "argstr": "-noresample"},
    ),
    (
        "force_scaling",
        bool,
        {
            "help_string": "force rescaling even for low-res images",
            "argstr": "-forcescaling",
        },
    ),
    (
        "min_sampling",
        float,
        {
            "help_string": "set minimum voxel dimension for sampling",
            "argstr": "-minsampling {min_sampling}",
        },
    ),
    (
        "padding_size",
        int,
        {
            "help_string": "for applyxfm: interpolates outside image by size",
            "argstr": "-paddingsize {padding_size}",
        },
    ),
    (
        "searchr_x",
        list,
        {
            "help_string": "search angles along x-axis, in degrees",
            "argstr": "-searchrx {searchr_x}",
        },
    ),
    (
        "searchr_y",
        list,
        {
            "help_string": "search angles along y-axis, in degrees",
            "argstr": "-searchry {searchr_y}",
        },
    ),
    (
        "searchr_z",
        list,
        {
            "help_string": "search angles along z-axis, in degrees",
            "argstr": "-searchrz {searchr_z}",
        },
    ),
    (
        "no_search",
        bool,
        {
            "help_string": "set all angular searches to ranges 0 to 0",
            "argstr": "-nosearch",
        },
    ),
    (
        "coarse_search",
        int,
        {
            "help_string": "coarse search delta angle",
            "argstr": "-coarsesearch {coarse_search}",
        },
    ),
    (
        "fine_search",
        int,
        {
            "help_string": "fine search delta angle",
            "argstr": "-finesearch {fine_search}",
        },
    ),
    (
        "schedule",
        specs.File,
        {"help_string": "replaces default schedule", "argstr": "-schedule {schedule}"},
    ),
    (
        "ref_weight",
        specs.File,
        {
            "help_string": "File for reference weighting volume",
            "argstr": "-refweight {ref_weight}",
        },
    ),
    (
        "in_weight",
        specs.File,
        {
            "help_string": "File for input weighting volume",
            "argstr": "-inweight {in_weight}",
        },
    ),
    (
        "no_clamp",
        bool,
        {"help_string": "do not use intensity clamping", "argstr": "-noclamp"},
    ),
    (
        "no_resample_blur",
        bool,
        {
            "help_string": "do not use blurring on downsampling",
            "argstr": "-noresampblur",
        },
    ),
    (
        "rigid2D",
        bool,
        {"help_string": "use 2D rigid body mode - ignores dof", "argstr": "-2D"},
    ),
    ("save_log", bool, {"help_string": "save to log file"}),
    (
        "verbose",
        int,
        {"help_string": "verbose mode, 0 is least", "argstr": "-verbose {verbose}"},
    ),
    (
        "bgvalue",
        float,
        {
            "help_string": "use specified background value for points outside FOV",
            "argstr": "-setbackground {bgvalue}",
        },
    ),
    (
        "wm_seg",
        str,
        {
            "help_string": "white matter segmentation volume needed by BBR cost function",
            "argstr": "-wmseg {wm_seg}",
        },
    ),
    (
        "wmcoords",
        str,
        {
            "help_string": "white matter boundary coordinates for BBR cost function",
            "argstr": "-wmcoords {wmcoords}",
        },
    ),
    (
        "wmnorms",
        str,
        {
            "help_string": "white matter boundary normals for BBR cost function",
            "argstr": "-wmnorms {wmnorms}",
        },
    ),
    (
        "fieldmap",
        str,
        {
            "help_string": "fieldmap image in rads/s - must be already registered to the reference image",
            "argstr": "-fieldmap {fieldmap}",
        },
    ),
    (
        "fieldmapmask",
        str,
        {
            "help_string": "mask for fieldmap image",
            "argstr": "-fieldmapmask {fieldmapmask}",
        },
    ),
    (
        "pedir",
        int,
        {
            "help_string": "phase encode direction of EPI - 1/2/3=x/y/z & -1/-2/-3=-x/-y/-z",
            "argstr": "-pedir {pedir}",
        },
    ),
    (
        "echospacing",
        float,
        {
            "help_string": "value of EPI echo spacing - units of seconds",
            "argstr": "-echospacing {echospacing}",
        },
    ),
    (
        "bbrtype",
        ty.Any,
        {
            "help_string": "type of bbr cost function: signed [default], global_abs, local_abs",
            "argstr": "-bbrtype {bbrtype}",
        },
    ),
    (
        "bbrslope",
        float,
        {"help_string": "value of bbr slope", "argstr": "-bbrslope {bbrslope}"},
    ),
]
FLIRT_input_spec = specs.SpecInfo(name="Input", fields=input_fields, bases=(specs.ShellSpec,))

output_fields = []
FLIRT_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FLIRT(ShellCommandTask):
    input_spec = FLIRT_input_spec
    output_spec = FLIRT_output_spec
    executable = "flirt"
