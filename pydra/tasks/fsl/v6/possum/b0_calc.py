from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


@shell.define(
    xor=[
        ["x_b0", "xyz_b0"],
        ["x_b0", "xyz_b0", "y_b0", "z_b0"],
        ["xyz_b0", "y_b0"],
        ["xyz_b0", "z_b0"],
    ]
)
class B0Calc(shell.Task["B0Calc.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.possum.b0_calc import B0Calc

    >>> task = B0Calc()
    >>> task.in_file = Nifti1.mock("tissue+air_map.nii")
    >>> task.cmdline
    'b0calc -i tissue+air_map.nii -o tissue+air_map_b0field.nii.gz --chi0=4.000000e-07 -d -9.450000e-06 --extendboundary=1.00 --b0x=0.00 --gx=0.0000 --b0y=0.00 --gy=0.0000 --b0=3.00 --gz=0.0000'


    """

    executable = "b0calc"
    in_file: Nifti1 = shell.arg(
        help="filename of input image (usually a tissue/air segmentation)",
        argstr="-i {in_file}",
        position=1,
    )
    x_grad: float = shell.arg(
        help="Value for zeroth-order x-gradient field (per mm)",
        argstr="--gx={x_grad:0.4}",
        default=0.0,
    )
    y_grad: float = shell.arg(
        help="Value for zeroth-order y-gradient field (per mm)",
        argstr="--gy={y_grad:0.4}",
        default=0.0,
    )
    z_grad: float = shell.arg(
        help="Value for zeroth-order z-gradient field (per mm)",
        argstr="--gz={z_grad:0.4}",
        default=0.0,
    )
    x_b0: float | None = shell.arg(
        help="Value for zeroth-order b0 field (x-component), in Tesla",
        argstr="--b0x={x_b0:0.2}",
        default=0.0,
    )
    y_b0: float | None = shell.arg(
        help="Value for zeroth-order b0 field (y-component), in Tesla",
        argstr="--b0y={y_b0:0.2}",
        default=0.0,
    )
    z_b0: float | None = shell.arg(
        help="Value for zeroth-order b0 field (z-component), in Tesla",
        argstr="--b0={z_b0:0.2}",
        default=1.0,
    )
    xyz_b0: ty.Any | None = shell.arg(
        help="Zeroth-order B0 field in Tesla",
        argstr="--b0x={xyz_b0[0]:0.2} --b0y={xyz_b0[1]:0.2} --b0={xyz_b0[2]:0.2}",
    )
    delta: float = shell.arg(
        help="Delta value (chi_tissue - chi_air)", argstr="-d %e", default=-9.45e-06
    )
    chi_air: float = shell.arg(
        help="susceptibility of air", argstr="--chi0=%e", default=4e-07
    )
    compute_xyz: bool = shell.arg(
        help="calculate and save all 3 field components (i.e. x,y,z)",
        argstr="--xyz",
        default=False,
    )
    extendboundary: float = shell.arg(
        help="Relative proportion to extend voxels at boundary",
        argstr="--extendboundary={extendboundary:0.2}",
        default=1.0,
    )
    directconv: bool = shell.arg(
        help="use direct (image space) convolution, not FFT",
        argstr="--directconv",
        default=False,
    )

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="filename of B0 output volume",
            argstr="-o {out_file}",
            path_template="{in_file}_b0field",
            position=2,
        )
