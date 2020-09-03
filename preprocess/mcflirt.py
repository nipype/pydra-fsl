from pydra.engine import specs
from pydra import ShellCommandTask
from pydra.utils.messenger import AuditFlag
import traits
import attr
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "argstr": "-in {in_file}",
            "help_string": "timeseries to motion-correct",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "out_file",
        str,
        {
            "argstr": "-out {out_file}",
            "help_string": "file to write",
            "output_file_template": "{in_file}_mcf",
        },
    ),
    (
        "cost",
        ty.Any,
        {"argstr": "-cost {cost}", "help_string": "cost function to optimize"},
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
            "help_string": "degrees of freedom for the transformation",
        },
    ),
    (
        "ref_vol",
        int,
        {"argstr": "-refvol {ref_vol}", "help_string": "volume to align frames to"},
    ),
    (
        "scaling",
        float,
        {"argstr": "-scaling {scaling}", "help_string": "scaling factor to use"},
    ),
    (
        "smooth",
        float,
        {
            "argstr": "-smooth {smooth}",
            "help_string": "smoothing factor for the cost function",
        },
    ),
    (
        "rotation",
        int,
        {
            "argstr": "-rotation {rotation}",
            "help_string": "scaling factor for rotation tolerances",
        },
    ),
    (
        "stages",
        int,
        {
            "argstr": "-stages {stages}",
            "help_string": "stages (if 4, perform final search with sinc interpolation",
        },
    ),
    (
        "init",
        specs.File,
        {"argstr": "-init {init}", "help_string": "inital transformation matrix"},
    ),
    (
        "interpolation",
        ty.Any,
        {
            "argstr": "{interpolation}",
            "help_string": "interpolation method for transformation",
        },
    ),
    (
        "use_gradient",
        bool,
        {"argstr": "-gdt", "help_string": "run search on gradient images"},
    ),
    (
        "use_contour",
        bool,
        {"argstr": "-edge", "help_string": "run search on contour images"},
    ),
    (
        "mean_vol",
        bool,
        {"argstr": "-meanvol", "help_string": "register to mean volume"},
    ),
    (
        "stats_imgs",
        bool,
        {"argstr": "-stats", "help_string": "produce variance and std. dev. images"},
    ),
    (
        "save_mats",
        bool,
        {"argstr": "-mats", "help_string": "save transformation matrices"},
    ),
    (
        "save_plots",
        bool,
        {"argstr": "-plots", "help_string": "save transformation parameters"},
    ),
    (
        "save_rms",
        bool,
        {
            "argstr": "-rmsabs -rmsrel",
            "help_string": "save rms displacement parameters",
        },
    ),
    (
        "ref_file",
        specs.File,
        {
            "argstr": "-reffile {ref_file}",
            "help_string": "target image for motion correction",
        },
    ),
]
bet_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_file",
        specs.File,
        {
            "help_string": "motion-corrected timeseries",
            "requires": ["in_file"],
            "output_file_template": "{in_file}_mcf",
        },
    ),
    (
        "variance_img",
        specs.File,
        {
            "help_string": "variance image",
            "requires": ["in_file", ("stats_imgs", True)],
            "output_file_template": "{out_file}_variance.ext",
        },
    ),
    (
        "std_img",
        specs.File,
        {
            "help_string": "standard deviation image",
            "requires": ["in_file", ("stats_imgs", True)],
            "output_file_template": "{out_file}_sigma.ext",
        },
    ),
    (
        "mean_img",
        specs.File,
        {
            "help_string": "mean timeseries image (if mean_vol=True)",
            "requires": ["in_file", ("mean_vol", True)],
            "output_file_template": "{out_file}_mean_reg.ext",
        },
    ),
    (
        "par_file",
        specs.File,
        {
            "help_string": "text-file with motion parameters",
            "requires": ["save_plots"],
            "output_file_template": "{out_file}.par",
        },
    ),
]
bet_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MCFLIRT(ShellCommandTask):
    def __init__(
        self,
        audit_flags: AuditFlag = AuditFlag.NONE,
        cache_dir=None,
        input_spec=None,
        messenger_args=None,
        messengers=None,
        name=None,
        output_spec=None,
        rerun=False,
        strip=False,
        **kwargs
    ):
        if input_spec is None:
            input_spec = bet_input_spec
        if output_spec is None:
            output_spec = bet_output_spec
        if name is None:
            name = "MCFLIRT"
        super().__init__(
            name="MCFLIRT",
            input_spec=input_spec,
            output_spec=output_spec,
            audit_flags=audit_flags,
            messengers=messengers,
            messenger_args=messenger_args,
            cache_dir=cache_dir,
            strip=strip,
            rerun=rerun,
            executable="mcflirt",
            **kwargs
        )
