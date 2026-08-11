from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _gen_filename(name, inputs):
    if name == "out_dir":
        return os.getcwd()


def out_dir_default(inputs):
    return _gen_filename("out_dir", inputs=inputs)


@shell.define(xor=[["one_sample_group_mean", "design_file"]])
class DualRegression(shell.Task["DualRegression.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.fsl.v6.model.dual_regression import DualRegression

    >>> task = DualRegression()
    >>> task.in_files = [Nifti1.mock("functional.nii"), Nifti1.mock("functional2.nii"), Nifti1.mock("functional3.nii")]
    >>> task.group_IC_maps_4D = File.mock()
    >>> task.des_norm = False
    >>> task.design_file = File.mock()
    >>> task.con_file = File.mock()
    >>> task.n_perm = 10
    >>> task.cmdline
    'dual_regression allFA.nii 0 -1 10 my_output_directory functional.nii functional2.nii functional3.nii'


    """

    executable = "dual_regression"
    in_files: list[Nifti1] = shell.arg(
        help="List all subjects' preprocessed, standard-space 4D datasets",
        argstr="{in_files}",
        position=-1,
        sep=" ",
    )
    group_IC_maps_4D: File = shell.arg(
        help="4D image containing spatial IC maps (melodic_IC) from the whole-group ICA analysis",
        argstr="{group_IC_maps_4D}",
        position=1,
    )
    des_norm: bool = shell.arg(
        help="Whether to variance-normalise the timecourses used as the stage-2 regressors; True is default and recommended",
        argstr="{des_norm:d}",
        position=2,
        default=True,
    )
    one_sample_group_mean: bool = shell.arg(
        help="perform 1-sample group-mean test instead of generic permutation test",
        argstr="-1",
        position=3,
    )
    design_file: File | None = shell.arg(
        help="Design matrix for final cross-subject modelling with randomise",
        argstr="{design_file}",
        position=3,
    )
    con_file: File = shell.arg(
        help="Design contrasts for final cross-subject modelling with randomise",
        argstr="{con_file}",
        position=4,
    )
    n_perm: int = shell.arg(
        help="Number of permutations for randomise; set to 1 for just raw tstat output, set to 0 to not run randomise at all.",
        argstr="{n_perm}",
        position=5,
    )

    class Outputs(shell.Outputs):
        out_dir: ty.Any = shell.outarg(
            help="This directory will be created to hold all output and logfiles",
            argstr="{out_dir}",
            position=6,
            path_template="out_dir",
        )
