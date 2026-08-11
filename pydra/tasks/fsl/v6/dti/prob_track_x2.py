import attrs
from fileformats.generic import File
from fileformats.medimage import NiftiGz
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

    if inputs["out_dir"] is attrs.NOTHING:
        out_dir = os.getcwd()
    else:
        out_dir = inputs["out_dir"]

    outputs["way_total"] = os.path.abspath(os.path.join(out_dir, "waytotal"))

    if inputs["omatrix1"] is not attrs.NOTHING:
        outputs["network_matrix"] = os.path.abspath(
            os.path.join(out_dir, "matrix_seeds_to_all_targets")
        )
        outputs["matrix1_dot"] = os.path.abspath(
            os.path.join(out_dir, "fdt_matrix1.dot")
        )

    if inputs["omatrix2"] is not attrs.NOTHING:
        outputs["lookup_tractspace"] = os.path.abspath(
            os.path.join(out_dir, "lookup_tractspace_fdt_matrix2.nii.gz")
        )
        outputs["matrix2_dot"] = os.path.abspath(
            os.path.join(out_dir, "fdt_matrix2.dot")
        )

    if inputs["omatrix3"] is not attrs.NOTHING:
        outputs["matrix3_dot"] = os.path.abspath(
            os.path.join(out_dir, "fdt_matrix3.dot")
        )
    return outputs


def network_matrix_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("network_matrix")


def matrix1_dot_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("matrix1_dot")


def lookup_tractspace_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("lookup_tractspace")


def matrix2_dot_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("matrix2_dot")


def matrix3_dot_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("matrix3_dot")


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


def out_dir_default(inputs):
    return _gen_filename("out_dir", inputs=inputs)


@shell.define
class ProbTrackX2(shell.Task["ProbTrackX2.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import NiftiGz
    >>> from pydra.tasks.fsl.v6.dti.prob_track_x2 import ProbTrackX2

    >>> task = ProbTrackX2()
    >>> task.fopd = File.mock()
    >>> task.target2 = File.mock()
    >>> task.target3 = File.mock()
    >>> task.lrtarget3 = File.mock()
    >>> task.colmask4 = File.mock()
    >>> task.target4 = File.mock()
    >>> task.fsamples = [NiftiGz.mock("m"), NiftiGz.mock("e"), NiftiGz.mock("r"), NiftiGz.mock("g"), NiftiGz.mock("e"), NiftiGz.mock("d"), NiftiGz.mock("_"), NiftiGz.mock("f"), NiftiGz.mock("1"), NiftiGz.mock("s"), NiftiGz.mock("a"), NiftiGz.mock("m"), NiftiGz.mock("p"), NiftiGz.mock("l"), NiftiGz.mock("e"), NiftiGz.mock("s"), NiftiGz.mock("."), NiftiGz.mock("n"), NiftiGz.mock("i"), NiftiGz.mock("i"), NiftiGz.mock("."), NiftiGz.mock("g"), NiftiGz.mock("z")]
    >>> task.mask = NiftiGz.mock("nodif_brain_mask.nii.gz")
    >>> task.seed = "seed_source.nii.gz"
    >>> task.waypoints = File.mock()
    >>> task.seed_ref = File.mock()
    >>> task.avoid_mp = File.mock()
    >>> task.stop_mask = File.mock()
    >>> task.xfm = File.mock()
    >>> task.inv_xfm = File.mock()
    >>> task.n_samples = 3
    >>> task.cmdline
    'probtrackx2 --forcedir -m nodif_brain_mask.nii.gz --nsamples=3 --nsteps=10 --opd --dir=. --samples=merged --seed=seed_source.nii.gz'


    """

    executable = "probtrackx2"
    simple: bool = shell.arg(
        help="rack from a list of voxels (seed must be a ASCII list of coordinates)",
        argstr="--simple",
    )
    fopd: File = shell.arg(
        help="Other mask for binning tract distribution", argstr="--fopd={fopd}"
    )
    waycond: ty.Any = shell.arg(
        help='Waypoint condition. Either "AND" (default) or "OR"',
        argstr="--waycond={waycond}",
    )
    wayorder: bool = shell.arg(
        help="Reject streamlines that do not hit waypoints in given order. Only valid if waycond=AND",
        argstr="--wayorder",
    )
    onewaycondition: bool = shell.arg(
        help="Apply waypoint conditions to each half tract separately",
        argstr="--onewaycondition",
    )
    omatrix1: bool = shell.arg(
        help="Output matrix1 - SeedToSeed Connectivity", argstr="--omatrix1"
    )
    distthresh1: float = shell.arg(
        help="Discards samples (in matrix1) shorter than this threshold (in mm - default=0)",
        argstr="--distthresh1={distthresh1:.3}",
    )
    omatrix2: bool = shell.arg(
        help="Output matrix2 - SeedToLowResMask",
        argstr="--omatrix2",
        requires=["target2"],
    )
    target2: File = shell.arg(
        help="Low resolution binary brain mask for storing connectivity distribution in matrix2 mode",
        argstr="--target2={target2}",
    )
    omatrix3: bool = shell.arg(
        help="Output matrix3 (NxN connectivity matrix)",
        argstr="--omatrix3",
        requires=["target3", "lrtarget3"],
    )
    target3: File = shell.arg(
        help="Mask used for NxN connectivity matrix (or Nxn if lrtarget3 is set)",
        argstr="--target3={target3}",
    )
    lrtarget3: File = shell.arg(
        help="Column-space mask used for Nxn connectivity matrix",
        argstr="--lrtarget3={lrtarget3}",
    )
    distthresh3: float = shell.arg(
        help="Discards samples (in matrix3) shorter than this threshold (in mm - default=0)",
        argstr="--distthresh3={distthresh3:.3}",
    )
    omatrix4: bool = shell.arg(
        help="Output matrix4 - DtiMaskToSeed (special Oxford Sparse Format)",
        argstr="--omatrix4",
    )
    colmask4: File = shell.arg(
        help="Mask for columns of matrix4 (default=seed mask)",
        argstr="--colmask4={colmask4}",
    )
    target4: File = shell.arg(
        help="Brain mask in DTI space", argstr="--target4={target4}"
    )
    meshspace: ty.Any = shell.arg(
        help='Mesh reference space - either "caret" (default) or "freesurfer" or "first" or "vox"',
        argstr="--meshspace={meshspace}",
    )
    thsamples: list[File] = shell.arg(help="")
    phsamples: list[File] = shell.arg(help="")
    fsamples: list[NiftiGz] = shell.arg(help="")
    samples_base_name: str = shell.arg(
        help="the rootname/base_name for samples files",
        argstr="--samples={samples_base_name}",
        default="merged",
    )
    mask: NiftiGz = shell.arg(
        help="bet binary mask file in diffusion space", argstr="-m {mask}"
    )
    seed: ty.Any = shell.arg(
        help="seed volume(s), or voxel(s) or freesurfer label file",
        formatter=seed_formatter,
    )
    target_masks: list[File] = shell.arg(
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
    xfm: File = shell.arg(
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
        network_matrix: File | None = shell.out(
            help="the network matrix generated by --omatrix1 option",
            callable=network_matrix_callable,
        )
        matrix1_dot: File | None = shell.out(
            help="Output matrix1.dot - SeedToSeed Connectivity",
            callable=matrix1_dot_callable,
        )
        lookup_tractspace: File | None = shell.out(
            help="lookup_tractspace generated by --omatrix2 option",
            callable=lookup_tractspace_callable,
        )
        matrix2_dot: File | None = shell.out(
            help="Output matrix2.dot - SeedToLowResMask", callable=matrix2_dot_callable
        )
        matrix3_dot: File | None = shell.out(
            help="Output matrix3 - NxN connectivity matrix",
            callable=matrix3_dot_callable,
        )
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
        msg = "Unable to generate filename for command %s. " % "probtrackx2"
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
