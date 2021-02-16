from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "argstr": "-in {in_file}",
            "help_string": "input file",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "reference",
        specs.File,
        {
            "argstr": "-ref {reference}",
            "help_string": "reference file",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "out_file",
        str,
        {
            "argstr": "-out {out_file}",
            "help_string": "registered output file",
            "position": 3,
            "output_file_template": "{in_file}_flirt",
        },
    ),
    (
        "out_matrix_file",
        str,
        {
            "argstr": "-omat {out_matrix_file}",
            "help_string": "output affine matrix in 4x4 asciii format",
            "position": 4,
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
        {"argstr": "-init {in_matrix_file}", "help_string": "input 4x4 affine matrix"},
    ),
    (
        "apply_xfm",
        bool,
        {
            "argstr": "-applyxfm",
            "help_string": "apply transformation supplied by in_matrix_file or uses_qform to use the affine matrix stored in the reference header",
        },
    ),
    (
        "apply_isoxfm",
        float,
        {
            "argstr": "-applyisoxfm {apply_isoxfm}",
            "help_string": "as applyxfm but forces isotropic resampling",
            "xor": ["apply_xfm"],
        },
    ),
    (
        "datatype",
        ty.Any,
        {"argstr": "-datatype {datatype}", "help_string": "force output data type"},
    ),
    ("cost", ty.Any, {"argstr": "-cost {cost}", "help_string": "cost function"}),
    (
        "cost_func",
        ty.Any,
        {"argstr": "-searchcost {cost_func}", "help_string": "cost function"},
    ),
    (
        "uses_qform",
        bool,
        {"argstr": "-usesqform", "help_string": "initialize using sform or qform"},
    ),
    (
        "display_init",
        bool,
        {"argstr": "-displayinit", "help_string": "display initial matrix"},
    ),
    (
        "angle_rep",
        ty.Any,
        {
            "argstr": "-anglerep {angle_rep}",
            "help_string": "representation of rotation angles",
        },
    ),
    (
        "interp",
        ty.Any,
        {
            "argstr": "-interp {interp}",
            "help_string": "final interpolation method used in reslicing",
        },
    ),
    (
        "sinc_width",
        int,
        {"argstr": "-sincwidth {sinc_width}", "help_string": "full-width in voxels"},
    ),
    (
        "sinc_window",
        ty.Any,
        {"argstr": "-sincwindow {sinc_window}", "help_string": "sinc window"},
    ),
    (
        "bins",
        int,
        {"argstr": "-bins {bins}", "help_string": "number of histogram bins"},
    ),
    (
        "dof",
        int,
        {
            "argstr": "-dof {dof}",
            "help_string": "number of transform degrees of freedom",
        },
    ),
    (
        "no_resample",
        bool,
        {"argstr": "-noresample", "help_string": "do not change input sampling"},
    ),
    (
        "force_scaling",
        bool,
        {
            "argstr": "-forcescaling",
            "help_string": "force rescaling even for low-res images",
        },
    ),
    (
        "min_sampling",
        float,
        {
            "argstr": "-minsampling {min_sampling}",
            "help_string": "set minimum voxel dimension for sampling",
        },
    ),
    (
        "padding_size",
        int,
        {
            "argstr": "-paddingsize {padding_size}",
            "help_string": "for applyxfm: interpolates outside image by size",
        },
    ),
    (
        "searchr_x",
        list,
        {
            "argstr": "-searchrx {searchr_x}",
            "help_string": "search angles along x-axis, in degrees",
        },
    ),
    (
        "searchr_y",
        list,
        {
            "argstr": "-searchry {searchr_y}",
            "help_string": "search angles along y-axis, in degrees",
        },
    ),
    (
        "searchr_z",
        list,
        {
            "argstr": "-searchrz {searchr_z}",
            "help_string": "search angles along z-axis, in degrees",
        },
    ),
    (
        "no_search",
        bool,
        {
            "argstr": "-nosearch",
            "help_string": "set all angular searches to ranges 0 to 0",
        },
    ),
    (
        "coarse_search",
        int,
        {
            "argstr": "-coarsesearch {coarse_search}",
            "help_string": "coarse search delta angle",
        },
    ),
    (
        "fine_search",
        int,
        {
            "argstr": "-finesearch {fine_search}",
            "help_string": "fine search delta angle",
        },
    ),
    (
        "schedule",
        specs.File,
        {"argstr": "-schedule {schedule}", "help_string": "replaces default schedule"},
    ),
    (
        "ref_weight",
        specs.File,
        {
            "argstr": "-refweight {ref_weight}",
            "help_string": "File for reference weighting volume",
        },
    ),
    (
        "in_weight",
        specs.File,
        {
            "argstr": "-inweight {in_weight}",
            "help_string": "File for input weighting volume",
        },
    ),
    (
        "no_clamp",
        bool,
        {"argstr": "-noclamp", "help_string": "do not use intensity clamping"},
    ),
    (
        "no_resample_blur",
        bool,
        {
            "argstr": "-noresampblur",
            "help_string": "do not use blurring on downsampling",
        },
    ),
    (
        "rigid2D",
        bool,
        {"argstr": "-2D", "help_string": "use 2D rigid body mode - ignores dof"},
    ),
    ("save_log", bool, {"help_string": "save to log file"}),
    (
        "verbose",
        int,
        {"argstr": "-verbose {verbose}", "help_string": "verbose mode, 0 is least"},
    ),
    (
        "bgvalue",
        float,
        {
            "argstr": "-setbackground {bgvalue}",
            "help_string": "use specified background value for points outside FOV",
        },
    ),
    (
        "wm_seg",
        str,
        {
            "argstr": "-wmseg {wm_seg}",
            "help_string": "white matter segmentation volume needed by BBR cost function",
        },
    ),
    (
        "wmcoords",
        str,
        {
            "argstr": "-wmcoords {wmcoords}",
            "help_string": "white matter boundary coordinates for BBR cost function",
        },
    ),
    (
        "wmnorms",
        str,
        {
            "argstr": "-wmnorms {wmnorms}",
            "help_string": "white matter boundary normals for BBR cost function",
        },
    ),
    (
        "fieldmap",
        str,
        {
            "argstr": "-fieldmap {fieldmap}",
            "help_string": "fieldmap image in rads/s - must be already registered to the reference image",
        },
    ),
    (
        "fieldmapmask",
        str,
        {
            "argstr": "-fieldmapmask {fieldmapmask}",
            "help_string": "mask for fieldmap image",
        },
    ),
    (
        "pedir",
        int,
        {
            "argstr": "-pedir {pedir}",
            "help_string": "phase encode direction of EPI - 1/2/3=x/y/z & -1/-2/-3=-x/-y/-z",
        },
    ),
    (
        "echospacing",
        float,
        {
            "argstr": "-echospacing {echospacing}",
            "help_string": "value of EPI echo spacing - units of seconds",
        },
    ),
    (
        "bbrtype",
        ty.Any,
        {
            "argstr": "-bbrtype {bbrtype}",
            "help_string": "type of bbr cost function: signed [default], global_abs, local_abs",
        },
    ),
    (
        "bbrslope",
        float,
        {"argstr": "-bbrslope {bbrslope}", "help_string": "value of bbr slope"},
    ),
]
FLIRT_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
FLIRT_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FLIRT(ShellCommandTask):
    input_spec = FLIRT_input_spec
    output_spec = FLIRT_output_spec
    executable = "flirt"
