import attrs
from fileformats.datascience import TextMatrix
from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "target_masks" and (value is not attrs.NOTHING):
        fname = "targets.txt"
        pass
    elif name == "seed" and isinstance(value, list):
        fname = "seeds.txt"
        pass
    else:
        pass

    return argstr.format(**inputs)


def target_masks_formatter(field, inputs):
    return _format_arg(
        "target_masks", field, inputs, argstr="--targetmasks={target_masks}"
    )


def seed_formatter(field, inputs):
    return _format_arg("seed", field, inputs, argstr="--seed={seed}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    if inputs["out_dir"] is attrs.NOTHING:
        out_dir = _gen_filename(
            "out_dir",
            seed=inputs["seed"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    else:
        out_dir = inputs["out_dir"]

    outputs["log"] = os.path.abspath(os.path.join(out_dir, "probtrackx.log"))

    if inputs["opd"] is True is not attrs.NOTHING:
        if isinstance(inputs["seed"], list) and isinstance(inputs["seed"][0], list):
            outputs["fdt_paths"] = []
            for seed in inputs["seed"]:
                outputs["fdt_paths"].append(
                    os.path.abspath(
                        _gen_fname(
                            ("fdt_paths_%s" % ("_".join([str(s) for s in seed]))),
                            cwd=out_dir,
                            suffix="",
                            output_type=inputs["output_type"],
                            inputs=inputs["inputs"],
                            output_dir=inputs["output_dir"],
                            stderr=inputs["stderr"],
                            stdout=inputs["stdout"],
                        )
                    )
                )
        else:
            outputs["fdt_paths"] = os.path.abspath(
                _gen_fname(
                    "fdt_paths",
                    cwd=out_dir,
                    suffix="",
                    output_type=inputs["output_type"],
                    inputs=inputs["inputs"],
                    output_dir=inputs["output_dir"],
                    stderr=inputs["stderr"],
                    stdout=inputs["stdout"],
                )
            )

    if inputs["target_masks"] is not attrs.NOTHING:
        outputs["targets"] = []
        for target in inputs["target_masks"]:
            outputs["targets"].append(
                os.path.abspath(
                    _gen_fname(
                        "seeds_to_" + os.path.split(target)[1],
                        cwd=out_dir,
                        suffix="",
                        output_type=inputs["output_type"],
                        inputs=inputs["inputs"],
                        output_dir=inputs["output_dir"],
                        stderr=inputs["stderr"],
                        stdout=inputs["stdout"],
                    )
                )
            )
    if (inputs["verbose"] is not attrs.NOTHING) and inputs["verbose"] == 2:
        outputs["particle_files"] = [
            os.path.abspath(os.path.join(out_dir, "particle%d" % i))
            for i in range(inputs["n_samples"])
        ]
    return outputs


def log_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("log")


def fdt_paths_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("fdt_paths")


def way_total_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("way_total")


def targets_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("targets")


def particle_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("particle_files")


def _gen_filename(name, inputs):
    if name == "out_dir":
        return os.getcwd()
    elif name == "mode":
        if isinstance(inputs["seed"], list) and isinstance(inputs["seed"][0], list):
            return "simple"
        else:
            return "seedmask"


def mode_default(inputs):
    return _gen_filename("mode", inputs=inputs)


def out_dir_default(inputs):
    return _gen_filename("out_dir", inputs=inputs)


@shell.define
class ProbTrackX(shell.Task["ProbTrackX.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.fsl.v6.dti.prob_track_x import ProbTrackX

    >>> task = ProbTrackX()
    >>> task.mode = "seedmask"
    >>> task.mask2 = File.mock()
    >>> task.mesh = File.mock()
    >>> task.thsamples = [Nifti1.mock("m"), Nifti1.mock("e"), Nifti1.mock("r"), Nifti1.mock("g"), Nifti1.mock("e"), Nifti1.mock("d"), Nifti1.mock("_"), Nifti1.mock("t"), Nifti1.mock("h"), Nifti1.mock("s"), Nifti1.mock("a"), Nifti1.mock("m"), Nifti1.mock("p"), Nifti1.mock("l"), Nifti1.mock("e"), Nifti1.mock("s"), Nifti1.mock("."), Nifti1.mock("n"), Nifti1.mock("i"), Nifti1.mock("i")]
    >>> task.phsamples = [Nifti1.mock("m"), Nifti1.mock("e"), Nifti1.mock("r"), Nifti1.mock("g"), Nifti1.mock("e"), Nifti1.mock("d"), Nifti1.mock("_"), Nifti1.mock("p"), Nifti1.mock("h"), Nifti1.mock("s"), Nifti1.mock("a"), Nifti1.mock("m"), Nifti1.mock("p"), Nifti1.mock("l"), Nifti1.mock("e"), Nifti1.mock("s"), Nifti1.mock("."), Nifti1.mock("n"), Nifti1.mock("i"), Nifti1.mock("i")]
    >>> task.fsamples = [Nifti1.mock("m"), Nifti1.mock("e"), Nifti1.mock("r"), Nifti1.mock("g"), Nifti1.mock("e"), Nifti1.mock("d"), Nifti1.mock("_"), Nifti1.mock("f"), Nifti1.mock("s"), Nifti1.mock("a"), Nifti1.mock("m"), Nifti1.mock("p"), Nifti1.mock("l"), Nifti1.mock("e"), Nifti1.mock("s"), Nifti1.mock("."), Nifti1.mock("n"), Nifti1.mock("i"), Nifti1.mock("i")]
    >>> task.samples_base_name = "merged"
    >>> task.mask = Nifti1.mock("mask.nii")
    >>> task.seed = "MASK_average_thal_right.nii"
    >>> task.target_masks = [Nifti1.mock("targets_MASK1.nii"), Nifti1.mock("targets_MASK2.nii")]
    >>> task.waypoints = File.mock()
    >>> task.seed_ref = File.mock()
    >>> task.out_dir = "."
    >>> task.force_dir = True
    >>> task.opd = True
    >>> task.os2t = True
    >>> task.avoid_mp = File.mock()
    >>> task.stop_mask = File.mock()
    >>> task.xfm = TextMatrix.mock("trans.mat")
    >>> task.inv_xfm = File.mock()
    >>> task.n_samples = 3
    >>> task.n_steps = 10
    >>> task.cmdline
    'probtrackx --forcedir -m mask.nii --mode=seedmask --nsamples=3 --nsteps=10 --opd --os2t --dir=. --samples=merged --seed=MASK_average_thal_right.nii --targetmasks=targets.txt --xfm=trans.mat'


    """

    executable = "probtrackx"
    mode: ty.Any = shell.arg(
        help="options: simple (single seed voxel), seedmask (mask of seed voxels), twomask_symm (two bet binary masks)",
        argstr="--mode={mode}",
    )
    mask2: File = shell.arg(
        help="second bet binary mask (in diffusion space) in twomask_symm mode",
        argstr="--mask2={mask2}",
    )
    mesh: File = shell.arg(
        help="Freesurfer-type surface descriptor (in ascii format)",
        argstr="--mesh={mesh}",
    )
    thsamples: list[Nifti1] = shell.arg(help="")
    phsamples: list[Nifti1] = shell.arg(help="")
    fsamples: list[Nifti1] = shell.arg(help="")
    samples_base_name: str = shell.arg(
        help="the rootname/base_name for samples files",
        argstr="--samples={samples_base_name}",
        default="merged",
    )
    mask: Nifti1 = shell.arg(
        help="bet binary mask file in diffusion space", argstr="-m {mask}"
    )
    seed: ty.Any = shell.arg(
        help="seed volume(s), or voxel(s) or freesurfer label file",
        formatter=seed_formatter,
    )
    target_masks: list[Nifti1] = shell.arg(
        help="list of target masks - required for seeds_to_targets classification",
        formatter=target_masks_formatter,
    )
    waypoints: File = shell.arg(
        help="waypoint mask or ascii list of waypoint masks - only keep paths going through ALL the masks",
        argstr="--waypoints={waypoints}",
    )
    network: bool = shell.arg(
        help="activate network mode - only keep paths going through at least one seed mask (required if multiple seed masks)",
        argstr="--network",
    )
    seed_ref: File = shell.arg(
        help="reference vol to define seed space in simple mode - diffusion space assumed if absent",
        argstr="--seedref={seed_ref}",
    )
    out_dir: ty.Any = shell.arg(
        help="directory to put the final volumes in", argstr="--dir={out_dir}"
    )
    force_dir: bool = shell.arg(
        help="use the actual directory name given - i.e. do not add + to make a new directory",
        argstr="--forcedir",
        default=True,
    )
    opd: bool = shell.arg(
        help="outputs path distributions", argstr="--opd", default=True
    )
    correct_path_distribution: bool = shell.arg(
        help="correct path distribution for the length of the pathways", argstr="--pd"
    )
    os2t: bool = shell.arg(help="Outputs seeds to targets", argstr="--os2t")
    avoid_mp: File = shell.arg(
        help="reject pathways passing through locations given by this mask",
        argstr="--avoid={avoid_mp}",
    )
    stop_mask: File = shell.arg(
        help="stop tracking at locations given by this mask file",
        argstr="--stop={stop_mask}",
    )
    xfm: TextMatrix = shell.arg(
        help="transformation matrix taking seed space to DTI space (either FLIRT matrix or FNIRT warp_field) - default is identity",
        argstr="--xfm={xfm}",
    )
    inv_xfm: File = shell.arg(
        help="transformation matrix taking DTI space to seed space (compulsory when using a warp_field for seeds_to_dti)",
        argstr="--invxfm={inv_xfm}",
    )
    n_samples: int = shell.arg(
        help="number of samples - default=5000",
        argstr="--nsamples={n_samples}",
        default=5000,
    )
    n_steps: int = shell.arg(
        help="number of steps per sample - default=2000", argstr="--nsteps={n_steps}"
    )
    dist_thresh: float = shell.arg(
        help="discards samples shorter than this threshold (in mm - default=0)",
        argstr="--distthresh={dist_thresh:.3}",
    )
    c_thresh: float = shell.arg(
        help="curvature threshold - default=0.2", argstr="--cthr={c_thresh:.3}"
    )
    sample_random_points: float = shell.arg(
        help="sample random points within seed voxels",
        argstr="--sampvox={sample_random_points:.3}",
    )
    step_length: float = shell.arg(
        help="step_length in mm - default=0.5", argstr="--steplength={step_length:.3}"
    )
    loop_check: bool = shell.arg(
        help="perform loop_checks on paths - slower, but allows lower curvature threshold",
        argstr="--loopcheck",
    )
    use_anisotropy: bool = shell.arg(
        help="use anisotropy to constrain tracking", argstr="--usef"
    )
    rand_fib: ty.Any = shell.arg(
        help="options: 0 - default, 1 - to randomly sample initial fibres (with f > fibthresh), 2 - to sample in proportion fibres (with f>fibthresh) to f, 3 - to sample ALL populations at random (even if f<fibthresh)",
        argstr="--randfib={rand_fib}",
    )
    fibst: int = shell.arg(
        help="force a starting fibre for tracking - default=1, i.e. first fibre orientation. Only works if randfib==0",
        argstr="--fibst={fibst}",
    )
    mod_euler: bool = shell.arg(
        help="use modified euler streamlining", argstr="--modeuler"
    )
    random_seed: int = shell.arg(help="random seed", argstr="--rseed={random_seed}")
    s2tastext: bool = shell.arg(
        help="output seed-to-target counts as a text file (useful when seeding from a mesh)",
        argstr="--s2tastext",
    )
    verbose: ty.Any = shell.arg(
        help="Verbose level, [0-2]. Level 2 is required to output particle files.",
        argstr="--verbose={verbose}",
    )

    class Outputs(shell.Outputs):
        log: File | None = shell.out(
            help="path/name of a text record of the command that was run",
            callable=log_callable,
        )
        fdt_paths: list[File] | None = shell.out(
            help="path/name of a 3D image file containing the output connectivity distribution to the seed mask",
            callable=fdt_paths_callable,
        )
        way_total: File | None = shell.out(
            help="path/name of a text file containing a single number corresponding to the total number of generated tracts that have not been rejected by inclusion/exclusion mask criteria",
            callable=way_total_callable,
        )
        targets: list[File] | None = shell.out(
            help="a list with all generated seeds_to_target files",
            callable=targets_callable,
        )
        particle_files: list[File] | None = shell.out(
            help="Files describing all of the tract samples. Generated only if verbose is set to 2",
            callable=particle_files_callable,
        )


def _gen_fname(
    basename,
    cwd=None,
    suffix=None,
    change_ext=True,
    ext=None,
    output_type=None,
    inputs=None,
    output_dir=None,
    stderr=None,
    stdout=None,
):
    """Generate a filename based on the given parameters.

    The filename will take the form: cwd/basename<suffix><ext>.
    If change_ext is True, it will use the extensions specified in
    <instance>inputs.output_type.

    Parameters
    ----------
    basename : str
        Filename to base the new filename on.
    cwd : str
        Path to prefix to the new filename. (default is output_dir)
    suffix : str
        Suffix to add to the `basename`.  (defaults is '' )
    change_ext : bool
        Flag to change the filename extension to the FSL output type.
        (default True)

    Returns
    -------
    fname : str
        New filename based on given parameters.

    """

    if basename == "":
        msg = "Unable to generate filename for command %s. " % "probtrackx"
        msg += "basename is not set!"
        raise ValueError(msg)
    if cwd is None:
        cwd = output_dir
    if ext is None:
        ext = Info.output_type_to_ext(output_type)
    if change_ext:
        if suffix:
            suffix = f"{suffix}{ext}"
        else:
            suffix = ext
    if suffix is None:
        suffix = ""
    fname = fname_presuffix(basename, suffix=suffix, use_ext=False, newpath=cwd)
    return fname


IFLOGGER = logging.getLogger("nipype.interface")
