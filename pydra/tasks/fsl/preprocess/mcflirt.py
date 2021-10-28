from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "help_string": "timeseries to motion-correct",
            "argstr": "-in {in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        str,
        {
            "help_string": "file to write",
            "argstr": "-out {out_file}",
            "output_file_template": "{in_file}_mcf",
        },
    ),
    (
        "cost",
        ty.Any,
        {"help_string": "cost function to optimize", "argstr": "-cost {cost}"},
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
            "help_string": "degrees of freedom for the transformation",
            "argstr": "-dof {dof}",
        },
    ),
    (
        "ref_vol",
        int,
        {"help_string": "volume to align frames to", "argstr": "-refvol {ref_vol}"},
    ),
    (
        "scaling",
        float,
        {"help_string": "scaling factor to use", "argstr": "-scaling {scaling:.2f}"},
    ),
    (
        "smooth",
        float,
        {
            "help_string": "smoothing factor for the cost function",
            "argstr": "-smooth {smooth:.2f}",
        },
    ),
    (
        "rotation",
        int,
        {
            "help_string": "scaling factor for rotation tolerances",
            "argstr": "-rotation {rotation}",
        },
    ),
    (
        "stages",
        int,
        {
            "help_string": "stages (if 4, perform final search with sinc interpolation",
            "argstr": "-stages {stages}",
        },
    ),
    (
        "init",
        specs.File,
        {"help_string": "inital transformation matrix", "argstr": "-init {init}"},
    ),
    (
        "interpolation",
        ty.Any,
        {
            "help_string": "interpolation method for transformation",
            "argstr": "-{interpolation}_final",
        },
    ),
    (
        "use_gradient",
        bool,
        {"help_string": "run search on gradient images", "argstr": "-gdt"},
    ),
    (
        "use_contour",
        bool,
        {"help_string": "run search on contour images", "argstr": "-edge"},
    ),
    (
        "mean_vol",
        bool,
        {"help_string": "register to mean volume", "argstr": "-meanvol"},
    ),
    (
        "stats_imgs",
        bool,
        {"help_string": "produce variance and std. dev. images", "argstr": "-stats"},
    ),
    (
        "save_mats",
        bool,
        {"help_string": "save transformation matrices", "argstr": "-mats"},
    ),
    (
        "save_plots",
        bool,
        {"help_string": "save transformation parameters", "argstr": "-plots"},
    ),
    (
        "save_rms",
        bool,
        {
            "help_string": "save rms displacement parameters",
            "argstr": "-rmsabs -rmsrel",
        },
    ),
    (
        "ref_file",
        specs.File,
        {
            "help_string": "target image for motion correction",
            "argstr": "-reffile {ref_file}",
        },
    ),
]
MCFLIRT_input_spec = specs.SpecInfo(name="Input", fields=input_fields, bases=(specs.ShellSpec,))

output_fields = [
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
MCFLIRT_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MCFLIRT(ShellCommandTask):
    input_spec = MCFLIRT_input_spec
    output_spec = MCFLIRT_output_spec
    executable = "mcflirt"
