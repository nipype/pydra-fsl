import attrs
from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name in ("in_intensitymap_file", "out_intensitymap_file"):
        if name == "out_intensitymap_file":
            value = _list_outputs(
                in_file=inputs["in_file"], output_type=inputs["output_type"]
            )[name]
        value = [FNIRT.intensitymap_file_basename(v) for v in value]
        assert len(set(value)) == 1, "Found different basenames for {}: {}".format(
            name, value
        )
        return argstr.format(**{name: value[0]})
    if name in list(parsed_inputs["filemap"].keys()):
        return argstr.format(
            **{
                name: _list_outputs(
                    in_file=inputs["in_file"], output_type=inputs["output_type"]
                )[name]
            }
        )

    return argstr.format(**inputs)


def out_intensitymap_file_formatter(field, inputs):
    return _format_arg(
        "out_intensitymap_file",
        field,
        inputs,
        argstr="--intout={out_intensitymap_file}",
    )


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)
    self_dict = {}

    outputs = {}
    for key, suffix in list(parsed_inputs["filemap"].items()):
        inval = getattr(self_dict["inputs"], key)
        change_ext = True
        if key in ["warped_file", "log_file"]:
            if suffix.endswith(".txt"):
                change_ext = False
            if inval is not attrs.NOTHING:
                outputs[key] = os.path.abspath(inval)
            else:
                outputs[key] = _gen_fname(
                    inputs["in_file"],
                    suffix="_" + suffix,
                    change_ext=change_ext,
                    output_type=inputs["output_type"],
                    inputs=inputs["inputs"],
                    output_dir=inputs["output_dir"],
                    stderr=inputs["stderr"],
                    stdout=inputs["stdout"],
                )
        elif inval is not attrs.NOTHING:
            if isinstance(inval, bool):
                if inval:
                    outputs[key] = _gen_fname(
                        inputs["in_file"],
                        suffix="_" + suffix,
                        change_ext=change_ext,
                        output_type=inputs["output_type"],
                        inputs=inputs["inputs"],
                        output_dir=inputs["output_dir"],
                        stderr=inputs["stderr"],
                        stdout=inputs["stdout"],
                    )
            else:
                outputs[key] = os.path.abspath(inval)

        if key == "out_intensitymap_file" and (outputs[key] is not attrs.NOTHING):
            basename = FNIRT.intensitymap_file_basename(outputs[key])
            outputs[key] = [outputs[key], "%s.txt" % basename]
    return outputs


def fieldcoeff_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("fieldcoeff_file")


def field_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("field_file")


def jacobian_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("jacobian_file")


def modulatedref_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("modulatedref_file")


def out_intensitymap_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_intensitymap_file")


def _gen_filename(name, inputs):
    if name in ["warped_file", "log_file"]:
        return _list_outputs(
            in_file=inputs["in_file"], output_type=inputs["output_type"]
        )[name]
    return None


def log_file_default(inputs):
    return _gen_filename("log_file", inputs=inputs)


def warped_file_default(inputs):
    return _gen_filename("warped_file", inputs=inputs)


@shell.define(
    xor=[
        ["apply_inmask", "skip_inmask"],
        ["apply_intensity_mapping", "skip_intensity_mapping"],
        ["apply_refmask", "skip_refmask"],
    ]
)
class FNIRT(shell.Task["FNIRT.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.preprocess.fnirt import FNIRT

    >>> task = FNIRT()
    >>> task.ref_file = File.mock()
    >>> task.in_file = File.mock()
    >>> task.affine_file = File.mock()
    >>> task.inwarp_file = File.mock()
    >>> task.refmask_file = File.mock()
    >>> task.inmask_file = File.mock()
    >>> task.warp_resolution = (6, 6, 6)
    >>> task.in_fwhm = [8, 4, 2, 2]
    >>> task.cmdline
    'None'


    """

    executable = "fnirt"
    ref_file: File = shell.arg(
        help="name of reference image", argstr="--ref={ref_file}"
    )
    in_file: File = shell.arg(help="name of input image", argstr="--in={in_file}")
    affine_file: File = shell.arg(
        help="name of file containing affine transform", argstr="--aff={affine_file}"
    )
    inwarp_file: File = shell.arg(
        help="name of file containing initial non-linear warps",
        argstr="--inwarp={inwarp_file}",
    )
    in_intensitymap_file: list[File] = shell.arg(
        help="name of file/files containing initial intensity mapping usually generated by previous fnirt run",
        argstr="--intin={in_intensitymap_file}",
    )
    fieldcoeff_file: ty.Any = shell.arg(
        help="name of output file with field coefficients or true",
        argstr="--cout={fieldcoeff_file}",
    )
    field_file: ty.Any = shell.arg(
        help="name of output file with field or true", argstr="--fout={field_file}"
    )
    jacobian_file: ty.Any = shell.arg(
        help="name of file for writing out the Jacobian of the field (for diagnostic or VBM purposes)",
        argstr="--jout={jacobian_file}",
    )
    modulatedref_file: ty.Any = shell.arg(
        help="name of file for writing out intensity modulated --ref (for diagnostic purposes)",
        argstr="--refout={modulatedref_file}",
    )
    out_intensitymap_file: ty.Any = shell.arg(
        help="name of files for writing information pertaining to intensity mapping",
        formatter=out_intensitymap_file_formatter,
    )
    config_file: ty.Any = shell.arg(
        help="Name of config file specifying command line arguments",
        argstr="--config={config_file}",
    )
    refmask_file: File = shell.arg(
        help="name of file with mask in reference space",
        argstr="--refmask={refmask_file}",
    )
    inmask_file: File = shell.arg(
        help="name of file with mask in input image space",
        argstr="--inmask={inmask_file}",
    )
    skip_refmask: bool = shell.arg(
        help="Skip specified refmask if set, default false", argstr="--applyrefmask=0"
    )
    skip_inmask: bool = shell.arg(
        help="skip specified inmask if set, default false", argstr="--applyinmask=0"
    )
    apply_refmask: list[ty.Any] = shell.arg(
        help="list of iterations to use reference mask on (1 to use, 0 to skip)",
        argstr="--applyrefmask={apply_refmask}",
        sep=",",
    )
    apply_inmask: list[ty.Any] = shell.arg(
        help="list of iterations to use input mask on (1 to use, 0 to skip)",
        argstr="--applyinmask={apply_inmask}",
        sep=",",
    )
    skip_implicit_ref_masking: bool = shell.arg(
        help="skip implicit masking  based on value in --ref image. Default = 0",
        argstr="--imprefm=0",
    )
    skip_implicit_in_masking: bool = shell.arg(
        help="skip implicit masking  based on value in --in image. Default = 0",
        argstr="--impinm=0",
    )
    refmask_val: float = shell.arg(
        help="Value to mask out in --ref image. Default =0.0",
        argstr="--imprefval={refmask_val}",
    )
    inmask_val: float = shell.arg(
        help="Value to mask out in --in image. Default =0.0",
        argstr="--impinval={inmask_val}",
    )
    max_nonlin_iter: list[int] = shell.arg(
        help="Max # of non-linear iterations list, default [5, 5, 5, 5]",
        argstr="--miter={max_nonlin_iter}",
        sep=",",
    )
    subsampling_scheme: list[int] = shell.arg(
        help="sub-sampling scheme, list, default [4, 2, 1, 1]",
        argstr="--subsamp={subsampling_scheme}",
        sep=",",
    )
    warp_resolution: ty.Any = shell.arg(
        help="(approximate) resolution (in mm) of warp basis in x-, y- and z-direction, default 10, 10, 10",
        argstr="--warpres={warp_resolution[0]},{warp_resolution[1]},{warp_resolution[2]}",
    )
    spline_order: int = shell.arg(
        help="Order of spline, 2->Qadratic spline, 3->Cubic spline. Default=3",
        argstr="--splineorder={spline_order}",
    )
    in_fwhm: list[int] = shell.arg(
        help="FWHM (in mm) of gaussian smoothing kernel for input volume, default [6, 4, 2, 2]",
        argstr="--infwhm={in_fwhm}",
        sep=",",
    )
    ref_fwhm: list[int] = shell.arg(
        help="FWHM (in mm) of gaussian smoothing kernel for ref volume, default [4, 2, 0, 0]",
        argstr="--reffwhm={ref_fwhm}",
        sep=",",
    )
    regularization_model: ty.Any = shell.arg(
        help="Model for regularisation of warp-field [membrane_energy bending_energy], default bending_energy",
        argstr="--regmod={regularization_model}",
    )
    regularization_lambda: list[float] = shell.arg(
        help="Weight of regularisation, default depending on --ssqlambda and --regmod switches. See user documentation.",
        argstr="--lambda={regularization_lambda}",
        sep=",",
    )
    skip_lambda_ssq: bool = shell.arg(
        help="If true, lambda is not weighted by current ssq, default false",
        argstr="--ssqlambda=0",
    )
    jacobian_range: ty.Any = shell.arg(
        help="Allowed range of Jacobian determinants, default 0.01, 100.0",
        argstr="--jacrange={jacobian_range[0]},{jacobian_range[1]}",
    )
    derive_from_ref: bool = shell.arg(
        help="If true, ref image is used to calculate derivatives. Default false",
        argstr="--refderiv",
    )
    intensity_mapping_model: ty.Any = shell.arg(
        help="Model for intensity-mapping", argstr="--intmod={intensity_mapping_model}"
    )
    intensity_mapping_order: int = shell.arg(
        help="Order of poynomial for mapping intensities, default 5",
        argstr="--intorder={intensity_mapping_order}",
    )
    biasfield_resolution: ty.Any = shell.arg(
        help="Resolution (in mm) of bias-field modelling local intensities, default 50, 50, 50",
        argstr="--biasres={biasfield_resolution[0]},{biasfield_resolution[1]},{biasfield_resolution[2]}",
    )
    bias_regularization_lambda: float = shell.arg(
        help="Weight of regularisation for bias-field, default 10000",
        argstr="--biaslambda={bias_regularization_lambda}",
    )
    skip_intensity_mapping: bool = shell.arg(
        help="Skip estimate intensity-mapping default false", argstr="--estint=0"
    )
    apply_intensity_mapping: list[ty.Any] = shell.arg(
        help="List of subsampling levels to apply intensity mapping for (0 to skip, 1 to apply)",
        argstr="--estint={apply_intensity_mapping}",
        sep=",",
    )
    hessian_precision: ty.Any = shell.arg(
        help="Precision for representing Hessian, double or float. Default double",
        argstr="--numprec={hessian_precision}",
    )

    class Outputs(shell.Outputs):
        warped_file: Path = shell.outarg(
            help="name of output image",
            argstr="--iout={warped_file}",
            path_template="warped_file",
        )
        log_file: Path = shell.outarg(
            help="Name of log-file",
            argstr="--logout={log_file}",
            path_template="log_file",
        )
        fieldcoeff_file: File | None = shell.out(
            help="file with field coefficients", callable=fieldcoeff_file_callable
        )
        field_file: File | None = shell.out(
            help="file with warp field", callable=field_file_callable
        )
        jacobian_file: File | None = shell.out(
            help="file containing Jacobian of the field",
            callable=jacobian_file_callable,
        )
        modulatedref_file: File | None = shell.out(
            help="file containing intensity modulated --ref",
            callable=modulatedref_file_callable,
        )
        out_intensitymap_file: list[File] | None = shell.out(
            help="files containing info pertaining to intensity mapping",
            callable=out_intensitymap_file_callable,
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
        msg = "Unable to generate filename for command %s. " % "fnirt"
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
