from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty


def FAST_output(field, in_files, out_basename):
    import attr

    if out_basename in [None, attr.NOTHING]:
        out_basename = in_files[-1]
    name = field.name
    if name == "tissue_class_map":
        return f"{out_basename}_seg"
    elif name == "mixeltype":
        return f"{out_basename}_mixeltype"
    elif name == "partial_volume_map":
        return f"{out_basename}_pveseg"
    else:
        raise Exception(
            f"this function should be run only for issue_class_map, "
            f"or mixeltype, not for {name}"
        )

    outputs = []
    if len(in_files) > 1:
        # for multi-image segmentation there is one corrected image
        # per input
        for val, f in enumerate(in_files):
            # image numbering is 1-based
            outputs.append(f"{out_basename}_restore_{val+1}")
    else:
        # single image segmentation has unnumbered output image
        outputs.append(f"{out_basename}_restore")
    return outputs


def FAST_output_infile(field, in_files, out_basename):
    import attr

    if out_basename in [None, attr.NOTHING]:
        out_basename = in_files[-1]
    name = field.name
    if name == "restored_image":
        suffix = "restore"
    elif name == "bias_field":
        suffix = "bias"
    else:
        raise Exception(
            f"this function should be run only for restored_image, "
            f"or bias_field, not for {name}"
        )

    outputs = []
    if len(in_files) > 1:
        # for multi-image segmentation there is one corrected image
        # per input
        for val, f in enumerate(in_files):
            # image numbering is 1-based
            outputs.append(f"{out_basename}_{suffix}_{val+1}")
    else:
        # single image segmentation has unnumbered output image
        outputs.append(f"{out_basename}_{suffix}")
    return outputs


def FAST_output_nclass(field, in_files, nclasses, out_basename):
    import attr

    if out_basename in [None, attr.NOTHING]:
        out_basename = in_files[-1]
    name = field.name

    if name == "tissue_class_files":
        suffix = "seg"
    elif name == "partial_volume_files":
        suffix = "pve"
    elif name == "probability_maps":
        suffix = "prob"
    else:
        raise Exception(
            f"this function should be run only for tissue_class_files, "
            f"partial_volume_files or probability_maps, not for {name}"
        )

    outputs = []
    for ii in range(nclasses):
        outputs.append(f"{out_basename}_{suffix}_{ii}")
    return outputs


input_fields = [
    (
        "in_files",
        specs.MultiInputFile,
        {
            "help_string": "image, or multi-channel set of images, to be segmented",
            "argstr": "{in_files}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_basename",
        str,
        {"help_string": "base name of output files", "argstr": "-o {out_basename}"},
    ),
    (
        "number_classes",
        ty.Any,
        3,
        {
            "help_string": "number of tissue-type classes",
            "argstr": "-n {number_classes}",
        },
    ),
    (
        "output_biasfield",
        bool,
        {"help_string": "output estimated bias field", "argstr": "-b"},
    ),
    (
        "output_biascorrected",
        bool,
        {"help_string": "output restored image (bias-corrected image)", "argstr": "-B"},
    ),
    (
        "img_type",
        ty.Any,
        {
            "help_string": "int specifying type of image: (1 = T1, 2 = T2, 3 = PD)",
            "argstr": "-t {img_type}",
        },
    ),
    (
        "bias_iters",
        ty.Any,
        {
            "help_string": "number of main-loop iterations during bias-field removal",
            "argstr": "-I {bias_iters}",
        },
    ),
    (
        "bias_lowpass",
        ty.Any,
        {
            "help_string": "bias field smoothing extent (FWHM) in mm",
            "argstr": "-l {bias_lowpass}",
        },
    ),
    (
        "init_seg_smooth",
        ty.Any,
        {
            "help_string": "initial segmentation spatial smoothness (during bias field estimation)",
            "argstr": "-f {init_seg_smooth:.3f}",
        },
    ),
    (
        "segments",
        bool,
        {
            "help_string": "outputs a separate binary image for each tissue type",
            "argstr": "-g",
        },
    ),
    (
        "init_transform",
        specs.File,
        {
            "help_string": "<standard2input.mat> initialise using priors",
            "argstr": "-a {init_transform}",
        },
    ),
    (
        "other_priors",
        specs.MultiInputFile,
        {"help_string": "alternative prior images", "argstr": "-A {other_priors}"},
    ),
    (
        "no_pve",
        bool,
        {
            "help_string": "turn off PVE (partial volume estimation)",
            "argstr": "--nopve",
        },
    ),
    ("no_bias", bool, {"help_string": "do not remove bias field", "argstr": "-N"}),
    ("use_priors", bool, {"help_string": "use priors throughout", "argstr": "-P"}),
    (
        "segment_iters",
        ty.Any,
        {
            "help_string": "number of segmentation-initialisation iterations",
            "argstr": "-W {segment_iters}",
        },
    ),
    (
        "mixel_smooth",
        ty.Any,
        {
            "help_string": "spatial smoothness for mixeltype",
            "argstr": "-R {mixel_smooth:.2f}",
        },
    ),
    (
        "iters_afterbias",
        ty.Any,
        {
            "help_string": "number of main-loop iterations after bias-field removal",
            "argstr": "-O {iters_afterbias}",
        },
    ),
    (
        "hyper",
        ty.Any,
        {"help_string": "segmentation spatial smoothness", "argstr": "-H {hyper:.2f}"},
    ),
    ("verbose", bool, {"help_string": "switch on diagnostic messages", "argstr": "-v"}),
    (
        "manual_seg",
        specs.File,
        {"help_string": "Filename containing intensities", "argstr": "-s {manual_seg}"},
    ),
    (
        "probability_maps",
        bool,
        {"help_string": "outputs individual probability maps", "argstr": "-p"},
    ),
]
FAST_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "tissue_class_files",
        specs.MultiOutputFile,
        {"requires": [("segments", True)], "callable": "FAST_output_nclass"},
    ),
    (
        "partial_volume_map",
        specs.File,
        {
            "help_string": "path/name of partial volume file _pveseg",
            "requires": [("no_pve", False)],
            "callable": "FAST_output",
        },
    ),
    (
        "partial_volume_files",
        specs.MultiOutputFile,
        {"requires": [("no_pve", False)], "callable": "FAST_output_nclass"},
    ),
    (
        "bias_field",
        specs.MultiOutputFile,
        {"requires": [("output_biasfield", True)], "callable": "FAST_output_infile"},
    ),
    (
        "probability_maps",
        specs.MultiOutputFile,
        {"requires": [("probability_maps", True)], "callable": "FAST_output_nclass"},
    ),
]
FAST_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FAST(ShellCommandTask):
    """
    Example
    -------
    >>> task = FAST()
    >>> task.inputs.in_files = "test.nii.gz"
    >>> task.inputs.out_basename = "fast_"
    >>> task.cmdline
    'fast -o fast_ -S 1 test.nii.gz'
    """

    input_spec = FAST_input_spec
    output_spec = FAST_output_spec
    executable = "fast"
