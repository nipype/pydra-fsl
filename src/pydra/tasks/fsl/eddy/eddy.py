"""
Eddy
====

Correct for artifacts induced by Eddy currents and subject motion.

Examples
--------

>>> task = Eddy(
...     input_image="input.nii",
...     brain_mask="brain.nii",
...     encoding_file="params.txt",
...     index_file="index.txt",
...     bvec_file="input.bvec",
...     bval_file="input.bval",
...     fieldmap_image="fieldmap.nii",
... )
>>> task.cmdline    # doctest: +ELLIPSIS
'eddy --imain=input.nii --mask=brain.nii --acqp=params.txt --index=index.txt \
--bvecs=input.bvec --bvals=input.bval --field=fieldmap.nii --out=eddy ...'
"""

__all__ = ["Eddy"]

from os import PathLike
from pathlib import PurePath

from attrs import define, field
from pydra.engine.specs import File, ShellOutSpec, ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(slots=False, kw_only=True)
class EddySpec(ShellSpec):
    """Specifications for eddy."""

    # Parameters that specify input files.
    input_image: PathLike = field(
        metadata={
            "help_string": "input image as a 4D volume",
            "mandatory": True,
            "argstr": "--imain={input_image}",
        }
    )

    brain_mask: PathLike = field(
        metadata={
            "help_string": "brain mask as a single volume image",
            "mandatory": True,
            "argstr": "--mask={brain_mask}",
        }
    )

    encoding_file: PathLike = field(
        metadata={
            "help_string": "acquisition parameters for the diffusion protocol",
            "mandatory": True,
            "argstr": "--acqp={encoding_file}",
        }
    )

    index_file: PathLike = field(
        metadata={
            "help_string": "mapping from volume index to encoding parameters",
            "mandatory": True,
            "argstr": "--index={index_file}",
        }
    )

    bvec_file: PathLike = field(
        metadata={
            "help_string": "diffusion directions",
            "mandatory": True,
            "argstr": "--bvecs={bvec_file}",
        }
    )

    bval_file: PathLike = field(
        metadata={
            "help_string": "diffusion weighting",
            "mandatory": True,
            "argstr": "--bvals={bval_file}",
        }
    )

    fieldmap_image: PathLike = field(metadata={"help_string": "fieldmap image", "argstr": "--field={fieldmap_image}"})

    fieldmap_matrix: PathLike = field(
        metadata={
            "help_string": "rigid-body transformation matrix from fieldmap to first input volume",
            "argstr": "--field_mat={fieldmap_matrix}",
            "requires": {"fieldmap_image"},
        }
    )

    no_peas: bool = field(
        metadata={"help_string": "do not perform post-Eddy alignment of shells", "argstr": "--dont_peas"}
    )

    # Parameters specifying names of output-files.
    output_basename: str = field(
        default="eddy",
        metadata={
            "help_string": "basename for output files",
            "argstr": "--out={output_basename}",
        },
    )

    # Parameters specifying how eddy should be run.
    first_level_model: str = field(
        default="quadratic",
        metadata={
            "help_string": "model for the magnetic field generated by Eddy currents",
            "argstr": "--flm={first_level_model}",
            "allowed_values": {"movement", "linear", "quadratic", "cubic"},
        },
    )

    second_level_model: str = field(
        default="none",
        metadata={
            "help_string": "model for how diffusion gradients generate Eddy currents",
            "argstr": "--slm={second_level_model}",
            "allowed_values": {"none", "linear", "quadratic"},
        },
    )

    fwhm: float = field(
        default=0,
        metadata={
            "help_string": "filter width used for pre-conditioning data prior to estimating distortions",
            "argstr": "--fwhm={fwhm}",
        },
    )

    num_iterations: int = field(
        default=5,
        metadata={
            "help_string": "number of iterations for eddy",
            "argstr": "--niter={num_iterations}",
        },
    )

    fill_empty_planes: bool = field(metadata={"help_string": "detect and fill empty planes", "argstr": "--fep"})

    interpolation: str = field(
        default="spline",
        metadata={
            "help_string": "interpolation method for the estimation phase",
            "argstr": "--interp={interpolation}",
            "allowed_values": {"spline", "trilinear"},
        },
    )

    resampling: str = field(
        default="jac",
        metadata={
            "help_string": "final resampling strategy",
            "argstr": "--resamp={resampling}",
            "allowed_values": {"jac", "lsr"},
        },
    )

    num_voxels: int = field(
        default=1000,
        metadata={
            "help_string": "number of voxels to use for GP hyperparameter estimation",
            "argstr": "--nvoxhp={num_voxels}",
        },
    )

    fudge_factor: int = field(
        default=10,
        metadata={
            "help_string": "fudge factor for Q-space smoothing during estimation",
            "argstr": "--ff={fudge_factor}",
        },
    )

    # Parameters for outlier replacement (ol)
    replace_outliers: bool = field(metadata={"help_string": "replace outliers", "argstr": "--repol"})

    outlier_num_stdevs: int = field(
        metadata={
            "help_string": "number of times off the standard deviation to qualify as outlier",
            "argstr": "--ol_nstd={outlier_num_stdevs}",
            "requires": {"replace_outliers"},
        }
    )

    outlier_num_voxels: int = field(
        metadata={
            "help_string": "minimum number of voxels in a slice to qualify for outlier detection",
            "argstr": "--ol_nvox={outlier_num_voxels}",
            "requires": {"replace_outliers"},
        }
    )

    outlier_type: str = field(
        metadata={
            "help_string": "type of outliers detected",
            "argstr": "--ol_type={outlier_type}",
            "allowed_values": {"both", "gw", "sw"},
            "requires": {"replace_outliers"},
        }
    )

    multiband_factor: int = field(metadata={"help_string": "multiband factor", "argstr": "--mb={multiband_factor}"})

    multiband_offset: int = field(
        metadata={
            "help_string": "multiband slice offset",
            "argstr": "--mb_offs={multiband_offset}",
            "requires": {"multiband_factor"},
        }
    )

    # Parameters for intra-volume movement correction (s2v)
    movement_prediction_order: int = field(
        default=0,
        metadata={
            "help_string": "order of movement prediction model",
            "argstr": "--mporder={movement_prediction_order}",
        },
    )

    s2v_num_iterations: int = field(
        metadata={
            "help_string": "number of iterations for s2v movement estimation",
            "argstr": "--s2v_niter={s2v_num_iterations}",
        }
    )

    s2v_lambda: float = field(
        metadata={
            "help_string": "weighting of regularization for s2v movement estimation",
            "argstr": "--s2v_lambda={s2v_lambda}",
        }
    )

    s2v_interpolation: str = field(
        metadata={
            "help_string": "interpolation method for s2v movement estimation.",
            "argstr": "--s2v_interp={s2v_interpolation}",
            "allowed_values": {"spline", "trilinear"},
        }
    )

    slice_grouping_file: PathLike = field(
        metadata={
            "help_string": "file containing slice grouping information",
            "argstr": "--slspec={slice_grouping_file}",
            "xor": {"slice_timing_file"},
        }
    )

    slice_timing_file: PathLike = field(
        metadata={
            "help_string": "file containing slice timing information",
            "argstr": "--json={slice_timing_file}",
            "xor": {"slice_grouping_file"},
        }
    )

    # Parameters for move-by-susceptibility correction (mbs)
    estimate_move_by_susceptibility: bool = field(
        metadata={
            "help_string": "estimate susceptibility-induced field changes due to subject motion",
            "argstr": "--estimate_move_by_susceptibility",
        }
    )

    mbs_num_iterations: int = field(
        metadata={
            "help_string": "number of iterations for MBS field estimation",
            "argstr": "--mbs_niter={mbs_num_iterations}",
            "requires": {"estimate_move_by_susceptibility"},
        }
    )

    mbs_lambda: int = field(
        metadata={
            "help_string": "weighting of regularization for MBS field estimation",
            "argstr": "--mbs_lambda={mbs_lambda}",
            "requires": {"estimate_move_by_susceptibility"},
        }
    )

    mbs_knot_spacing: int = field(
        metadata={
            "help_string": "knot-spacing for MBS field estimation",
            "argstr": "--mbs_ksp={mbs_knot_spacing}",
            "requires": {"estimate_move_by_susceptibility"},
        }
    )

    # Miscellaneous parameters.
    data_is_shelled: bool = field(
        metadata={"help_string": "bypass checks for data shelling", "argstr": "--data_is_shelled"}
    )

    random_seed: int = field(
        metadata={"help_string": "random seed for voxel selection", "argstr": "--initrand={random_seed}"}
    )

    save_cnr_maps: bool = field(metadata={"help_string": "save shell-wise CNR maps", "argstr": "--cnr_maps"})

    save_residuals: bool = field(metadata={"help_string": "save residuals for all scans", "argstr": "--residuals"})

    verbose: bool = field(metadata={"help_string": "enable verbose logging", "argstr": "--verbose"})


@define(slots=False, kw_only=True)
class EddyOutSpec(ShellOutSpec):
    """Output specification for eddy."""

    corrected_image: File = field(
        metadata={
            "help_string": "input image corrected for distortions",
            "output_file_template": "{output_basename}.nii.gz",
        }
    )

    parameters_file: File = field(
        metadata={
            "help_string": "registration parameters for movement and EC",
            "output_file_template": "{output_basename}.eddy_parameters",
        }
    )

    rotated_bvec_file: File = field(
        metadata={
            "help_string": "rotated b-vecs",
            "output_file_template": "{output_basename}.eddy_rotated_bvecs",
        }
    )

    movement_rms_matrix: File = field(
        metadata={
            "help_string": "movement induced RMS",
            "output_file_template": "{output_basename}.eddy_movement_rms",
        }
    )

    restricted_movement_rms_matrix: File = field(
        metadata={
            "help_string": "movement induced RMS without translation in the PE direction",
            "output_file_template": "{output_basename}.eddy_restricted_movement_rms",
        }
    )

    displacement_fields_image: File = field(
        metadata={
            "help_string": "displacement fields in millimeters",
            "output_file_template": "{output_basename}.eddy_displacement_fields",
        }
    )

    outlier_free_image: File = field(
        metadata={
            "help_string": "input image with outliers replaced by predictions",
            "output_file_template": "{output_basename}.eddy_outlier_free_data",
            "requires": ["replace_outliers"],
        }
    )

    movement_over_time_file: File = field(
        metadata={
            "help_string": "movement parameters per time-point (slice or group)",
            "output_file_template": "{output_basename}.eddy_movement_over_time",
            "requires": ["movement_prediction_order"],
        }
    )

    cnr_maps_image: File = field(
        metadata={
            "help_string": "path to optional CNR maps image",
            "output_file_template": "{output_basename}.eddy_cnr_maps",
            "requires": ["save_cnr_maps"],
        }
    )

    residuals_image: File = field(
        metadata={
            "help_string": "path to optional residuals image",
            "output_file_template": "{output_basename}.eddy_residuals",
            "requires": ["save_residuals"],
        }
    )


class Eddy(ShellCommandTask):
    """Task definition for eddy."""

    executable = "eddy"

    input_spec = SpecInfo(name="Input", bases=(EddySpec,))

    output_spec = SpecInfo(name="Output", bases=(EddyOutSpec,))
