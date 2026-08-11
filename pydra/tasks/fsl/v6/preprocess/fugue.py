import attrs
from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _parse_inputs(inputs, output_dir=None):
    if not output_dir:
        output_dir = os.getcwd()
    parsed_inputs = {}
    skip = []
    self_dict = {}

    if skip is None:
        skip = []

    input_phase = inputs["phasemap_in_file"] is not attrs.NOTHING
    input_vsm = inputs["shift_in_file"] is not attrs.NOTHING
    input_fmap = inputs["fmap_in_file"] is not attrs.NOTHING

    if not input_phase and not input_vsm and not input_fmap:
        raise RuntimeError(
            "Either phasemap_in_file, shift_in_file or fmap_in_file must be set."
        )

    if inputs["in_file"] is attrs.NOTHING:
        skip += ["unwarped_file", "warped_file"]
    else:
        if inputs["forward_warping"]:
            skip += ["unwarped_file"]
            trait_spec = self_dict["inputs"].trait("warped_file")
            trait_spec.name_template = "%s_warped"
            trait_spec.name_source = "in_file"
            trait_spec.output_name = "warped_file"
        else:
            skip += ["warped_file"]
            trait_spec = self_dict["inputs"].trait("unwarped_file")
            trait_spec.name_template = "%s_unwarped"
            trait_spec.name_source = "in_file"
            trait_spec.output_name = "unwarped_file"

    if inputs["shift_out_file"] is attrs.NOTHING:
        vsm_save_masked = (inputs["save_shift"] is not attrs.NOTHING) and inputs[
            "save_shift"
        ]
        vsm_save_unmasked = (
            inputs["save_unmasked_shift"] is not attrs.NOTHING
        ) and inputs["save_unmasked_shift"]

        if vsm_save_masked or vsm_save_unmasked:
            trait_spec = self_dict["inputs"].trait("shift_out_file")
            trait_spec.output_name = "shift_out_file"

            if input_fmap:
                trait_spec.name_source = "fmap_in_file"
            elif input_phase:
                trait_spec.name_source = "phasemap_in_file"
            elif input_vsm:
                trait_spec.name_source = "shift_in_file"
            else:
                raise RuntimeError(
                    "Either phasemap_in_file, shift_in_file or "
                    "fmap_in_file must be set."
                )

            if vsm_save_unmasked:
                trait_spec.name_template = "%s_vsm_unmasked"
            else:
                trait_spec.name_template = "%s_vsm"
        else:
            skip += ["save_shift", "save_unmasked_shift", "shift_out_file"]

    if inputs["fmap_out_file"] is attrs.NOTHING:
        fmap_save_masked = (inputs["save_fmap"] is not attrs.NOTHING) and inputs[
            "save_fmap"
        ]
        fmap_save_unmasked = (
            inputs["save_unmasked_fmap"] is not attrs.NOTHING
        ) and inputs["save_unmasked_fmap"]

        if fmap_save_masked or fmap_save_unmasked:
            trait_spec = self_dict["inputs"].trait("fmap_out_file")
            trait_spec.output_name = "fmap_out_file"

            if input_vsm:
                trait_spec.name_source = "shift_in_file"
            elif input_phase:
                trait_spec.name_source = "phasemap_in_file"
            elif input_fmap:
                trait_spec.name_source = "fmap_in_file"
            else:
                raise RuntimeError(
                    "Either phasemap_in_file, shift_in_file or "
                    "fmap_in_file must be set."
                )

            if fmap_save_unmasked:
                trait_spec.name_template = "%s_fieldmap_unmasked"
            else:
                trait_spec.name_template = "%s_fieldmap"
        else:
            skip += ["save_fmap", "save_unmasked_fmap", "fmap_out_file"]

    return parsed_inputs


def unwarped_file_callable(output_dir, inputs, stdout, stderr):
    parsed_inputs = _parse_inputs(inputs)
    return parsed_inputs.get("unwarped_file", attrs.NOTHING)


def warped_file_callable(output_dir, inputs, stdout, stderr):
    parsed_inputs = _parse_inputs(inputs)
    return parsed_inputs.get("warped_file", attrs.NOTHING)


def shift_out_file_callable(output_dir, inputs, stdout, stderr):
    parsed_inputs = _parse_inputs(inputs)
    return parsed_inputs.get("shift_out_file", attrs.NOTHING)


def fmap_out_file_callable(output_dir, inputs, stdout, stderr):
    parsed_inputs = _parse_inputs(inputs)
    return parsed_inputs.get("fmap_out_file", attrs.NOTHING)


@shell.define(
    xor=[
        ["save_fmap", "save_unmasked_fmap"],
        ["save_shift", "save_unmasked_shift"],
        ["unwarped_file", "warped_file"],
    ]
)
class FUGUE(shell.Task["FUGUE.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.preprocess.fugue import FUGUE

    >>> task = FUGUE()
    >>> task.in_file = Nifti1.mock("epi.nii")
    >>> task.shift_in_file = Nifti1.mock("vsm.nii"  # Previously computed with fugue as well)
    >>> task.phasemap_in_file = Nifti1.mock()
    >>> task.fmap_in_file = File.mock()
    >>> task.mask_file = Nifti1.mock()
    >>> task.cmdline
    'fugue --in=epi.nii --mask=epi_mask.nii --loadshift=vsm.nii --unwarpdir=y --unwarp=epi_unwarped.nii.gz'


    >>> task = FUGUE()
    >>> task.in_file = Nifti1.mock("epi.nii")
    >>> task.shift_in_file = Nifti1.mock()
    >>> task.phasemap_in_file = Nifti1.mock()
    >>> task.fmap_in_file = File.mock()
    >>> task.unwarp_direction = "y"
    >>> task.mask_file = Nifti1.mock("epi_mask.nii")
    >>> task.cmdline
    'fugue --in=epi.nii --mask=epi_mask.nii --loadshift=vsm.nii --unwarpdir=y --warp=epi_warped.nii.gz'


    >>> task = FUGUE()
    >>> task.in_file = Nifti1.mock()
    >>> task.shift_in_file = Nifti1.mock()
    >>> task.phasemap_in_file = Nifti1.mock("epi_phasediff.nii")
    >>> task.fmap_in_file = File.mock()
    >>> task.dwell_to_asym_ratio = (0.77e-3 * 3) / 2.46e-3
    >>> task.mask_file = Nifti1.mock()
    >>> task.save_shift = True
    >>> task.cmdline
    'fugue --dwelltoasym=0.9390243902 --mask=epi_mask.nii --phasemap=epi_phasediff.nii --saveshift=epi_phasediff_vsm.nii.gz --unwarpdir=y'


    """

    executable = "fugue"
    in_file: Nifti1 = shell.arg(
        help="filename of input volume", argstr="--in={in_file}"
    )
    shift_in_file: Nifti1 = shell.arg(
        help="filename for reading pixel shift volume",
        argstr="--loadshift={shift_in_file}",
    )
    phasemap_in_file: Nifti1 = shell.arg(
        help="filename for input phase image", argstr="--phasemap={phasemap_in_file}"
    )
    fmap_in_file: File = shell.arg(
        help="filename for loading fieldmap (rad/s)", argstr="--loadfmap={fmap_in_file}"
    )
    unwarped_file: Path | None = shell.arg(
        help="apply unwarping and save as filename",
        argstr="--unwarp={unwarped_file}",
        requires=["in_file"],
    )
    warped_file: Path | None = shell.arg(
        help="apply forward warping and save as filename",
        argstr="--warp={warped_file}",
        requires=["in_file"],
    )
    forward_warping: bool = shell.arg(
        help="apply forward warping instead of unwarping", default=False
    )
    dwell_to_asym_ratio: float = shell.arg(
        help="set the dwell to asym time ratio",
        argstr="--dwelltoasym={dwell_to_asym_ratio:.10}",
    )
    dwell_time: float = shell.arg(
        help="set the EPI dwell time per phase-encode line - same as echo spacing - (sec)",
        argstr="--dwell={dwell_time:.10}",
    )
    asym_se_time: float = shell.arg(
        help="set the fieldmap asymmetric spin echo time (sec)",
        argstr="--asym={asym_se_time:.10}",
    )
    median_2dfilter: bool = shell.arg(
        help="apply 2D median filtering", argstr="--median"
    )
    despike_2dfilter: bool = shell.arg(
        help="apply a 2D de-spiking filter", argstr="--despike"
    )
    no_gap_fill: bool = shell.arg(
        help="do not apply gap-filling measure to the fieldmap", argstr="--nofill"
    )
    no_extend: bool = shell.arg(
        help="do not apply rigid-body extrapolation to the fieldmap",
        argstr="--noextend",
    )
    smooth2d: float = shell.arg(
        help="apply 2D Gaussian smoothing of sigma N (in mm)",
        argstr="--smooth2={smooth2d:.2}",
    )
    smooth3d: float = shell.arg(
        help="apply 3D Gaussian smoothing of sigma N (in mm)",
        argstr="--smooth3={smooth3d:.2}",
    )
    poly_order: int = shell.arg(
        help="apply polynomial fitting of order N", argstr="--poly={poly_order}"
    )
    fourier_order: int = shell.arg(
        help="apply Fourier (sinusoidal) fitting of order N",
        argstr="--fourier={fourier_order}",
    )
    pava: bool = shell.arg(help="apply monotonic enforcement via PAVA", argstr="--pava")
    despike_threshold: float = shell.arg(
        help="specify the threshold for de-spiking (default=3.0)",
        argstr="--despikethreshold={despike_threshold}",
    )
    unwarp_direction: ty.Any = shell.arg(
        help="specifies direction of warping (default y)",
        argstr="--unwarpdir={unwarp_direction}",
    )
    phase_conjugate: bool = shell.arg(
        help="apply phase conjugate method of unwarping", argstr="--phaseconj"
    )
    icorr: bool = shell.arg(
        help="apply intensity correction to unwarping (pixel shift method only)",
        argstr="--icorr",
        requires=["shift_in_file"],
    )
    icorr_only: bool = shell.arg(
        help="apply intensity correction only",
        argstr="--icorronly",
        requires=["unwarped_file"],
    )
    mask_file: Nifti1 = shell.arg(
        help="filename for loading valid mask", argstr="--mask={mask_file}"
    )
    nokspace: bool = shell.arg(
        help="do not use k-space forward warping", argstr="--nokspace"
    )
    save_shift: bool = shell.arg(help="write pixel shift volume")
    shift_out_file: Path = shell.arg(
        help="filename for saving pixel shift volume",
        argstr="--saveshift={shift_out_file}",
    )
    save_unmasked_shift: bool = shell.arg(
        help="saves the unmasked shiftmap when using --saveshift",
        argstr="--unmaskshift",
    )
    save_fmap: bool = shell.arg(help="write field map volume")
    fmap_out_file: Path = shell.arg(
        help="filename for saving fieldmap (rad/s)", argstr="--savefmap={fmap_out_file}"
    )
    save_unmasked_fmap: bool = shell.arg(
        help="saves the unmasked fieldmap when using --savefmap", argstr="--unmaskfmap"
    )

    class Outputs(shell.Outputs):
        unwarped_file: File | None = shell.out(
            help="unwarped file", callable=unwarped_file_callable
        )
        warped_file: File | None = shell.out(
            help="forward warped file", callable=warped_file_callable
        )
        shift_out_file: File | None = shell.out(
            help="voxel shift map file", callable=shift_out_file_callable
        )
        fmap_out_file: File | None = shell.out(
            help="fieldmap file", callable=fmap_out_file_callable
        )
