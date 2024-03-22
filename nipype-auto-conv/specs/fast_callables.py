"""Module to put any functions that are referred to in the "callables" section of FAST.yaml"""

import attrs
import logging
import os
import os.path as op
from glob import glob
from pathlib import Path


def bias_field_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["bias_field"]


def mixeltype_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["mixeltype"]


def partial_volume_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["partial_volume_files"]


def partial_volume_map_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["partial_volume_map"]


def probability_maps_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["probability_maps"]


def restored_image_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["restored_image"]


def tissue_class_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["tissue_class_files"]


def tissue_class_map_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["tissue_class_map"]


IFLOGGER = logging.getLogger("nipype.interface")


# Original source at L885 of <nipype-install>/interfaces/base/core.py
def _gen_filename(name, inputs=None, stdout=None, stderr=None, output_dir=None):
    raise NotImplementedError


# Original source at L205 of <nipype-install>/interfaces/fsl/base.py
def _gen_fname(
    basename,
    cwd=None,
    suffix=None,
    change_ext=True,
    ext=None,
    inputs=None,
    stdout=None,
    stderr=None,
    output_dir=None,
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
        msg = "Unable to generate filename for command %s. " % "fast"
        msg += "basename is not set!"
        raise ValueError(msg)
    if cwd is None:
        cwd = output_dir
    if ext is None:
        ext = Info.output_type_to_ext(inputs.output_type)
    if change_ext:
        if suffix:
            suffix = "".join((suffix, ext))
        else:
            suffix = ext
    if suffix is None:
        suffix = ""
    fname = fname_presuffix(basename, suffix=suffix, use_ext=False, newpath=cwd)
    return fname


# Original source at L401 of <nipype-install>/interfaces/fsl/preprocess.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    outputs = {}
    if inputs.number_classes is attrs.NOTHING:
        nclasses = 3
    else:
        nclasses = inputs.number_classes
    # when using multichannel, results basename is based on last
    # input filename
    _gen_fname_opts = {}
    if inputs.out_basename is not attrs.NOTHING:
        _gen_fname_opts["basename"] = inputs.out_basename
        _gen_fname_opts["cwd"] = output_dir
    else:
        _gen_fname_opts["basename"] = inputs.in_files[-1]
        _gen_fname_opts["cwd"], _, _ = split_filename(_gen_fname_opts["basename"])

    outputs["tissue_class_map"] = _gen_fname(
        suffix="_seg",
        **_gen_fname_opts,
        inputs=inputs,
        stdout=stdout,
        stderr=stderr,
        output_dir=output_dir
    )
    if inputs.segments:
        outputs["tissue_class_files"] = []
        for i in range(nclasses):
            outputs["tissue_class_files"].append(
                _gen_fname(
                    suffix="_seg_%d" % i,
                    **_gen_fname_opts,
                    inputs=inputs,
                    stdout=stdout,
                    stderr=stderr,
                    output_dir=output_dir
                )
            )
    if inputs.output_biascorrected is not attrs.NOTHING:
        outputs["restored_image"] = []
        if len(inputs.in_files) > 1:
            # for multi-image segmentation there is one corrected image
            # per input
            for val, f in enumerate(inputs.in_files):
                # image numbering is 1-based
                outputs["restored_image"].append(
                    _gen_fname(
                        suffix="_restore_%d" % (val + 1),
                        **_gen_fname_opts,
                        inputs=inputs,
                        stdout=stdout,
                        stderr=stderr,
                        output_dir=output_dir
                    )
                )
        else:
            # single image segmentation has unnumbered output image
            outputs["restored_image"].append(
                _gen_fname(
                    suffix="_restore",
                    **_gen_fname_opts,
                    inputs=inputs,
                    stdout=stdout,
                    stderr=stderr,
                    output_dir=output_dir
                )
            )

    outputs["mixeltype"] = _gen_fname(
        suffix="_mixeltype",
        **_gen_fname_opts,
        inputs=inputs,
        stdout=stdout,
        stderr=stderr,
        output_dir=output_dir
    )
    if not inputs.no_pve:
        outputs["partial_volume_map"] = _gen_fname(
            suffix="_pveseg",
            **_gen_fname_opts,
            inputs=inputs,
            stdout=stdout,
            stderr=stderr,
            output_dir=output_dir
        )
        outputs["partial_volume_files"] = []
        for i in range(nclasses):
            outputs["partial_volume_files"].append(
                _gen_fname(
                    suffix="_pve_%d" % i,
                    **_gen_fname_opts,
                    inputs=inputs,
                    stdout=stdout,
                    stderr=stderr,
                    output_dir=output_dir
                )
            )
    if inputs.output_biasfield:
        outputs["bias_field"] = []
        if len(inputs.in_files) > 1:
            # for multi-image segmentation there is one bias field image
            # per input
            for val, f in enumerate(inputs.in_files):
                # image numbering is 1-based
                outputs["bias_field"].append(
                    _gen_fname(
                        suffix="_bias_%d" % (val + 1),
                        **_gen_fname_opts,
                        inputs=inputs,
                        stdout=stdout,
                        stderr=stderr,
                        output_dir=output_dir
                    )
                )
        else:
            # single image segmentation has unnumbered output image
            outputs["bias_field"].append(
                _gen_fname(
                    suffix="_bias",
                    **_gen_fname_opts,
                    inputs=inputs,
                    stdout=stdout,
                    stderr=stderr,
                    output_dir=output_dir
                )
            )

    if inputs.probability_maps:
        outputs["probability_maps"] = []
        for i in range(nclasses):
            outputs["probability_maps"].append(
                _gen_fname(
                    suffix="_prob_%d" % i,
                    **_gen_fname_opts,
                    inputs=inputs,
                    stdout=stdout,
                    stderr=stderr,
                    output_dir=output_dir
                )
            )
    return outputs


# Original source at L108 of <nipype-install>/utils/filemanip.py
def fname_presuffix(fname, prefix="", suffix="", newpath=None, use_ext=True):
    """Manipulates path and name of input filename

    Parameters
    ----------
    fname : string
        A filename (may or may not include path)
    prefix : string
        Characters to prepend to the filename
    suffix : string
        Characters to append to the filename
    newpath : string
        Path to replace the path of the input fname
    use_ext : boolean
        If True (default), appends the extension of the original file
        to the output name.

    Returns
    -------
    Absolute path of the modified filename

    >>> from nipype.utils.filemanip import fname_presuffix
    >>> fname = 'foo.nii.gz'
    >>> fname_presuffix(fname,'pre','post','/tmp')
    '/tmp/prefoopost.nii.gz'

    >>> from nipype.interfaces.base import attrs.NOTHING
    >>> fname_presuffix(fname, 'pre', 'post', attrs.NOTHING) == \
            fname_presuffix(fname, 'pre', 'post')
    True

    """
    pth, fname, ext = split_filename(fname)
    if not use_ext:
        ext = ""

    # No need for : bool(attrs.NOTHING is not attrs.NOTHING) evaluates to False
    if newpath:
        pth = op.abspath(newpath)
    return op.join(pth, prefix + fname + suffix + ext)


# Original source at L58 of <nipype-install>/utils/filemanip.py
def split_filename(fname):
    """Split a filename into parts: path, base filename and extension.

    Parameters
    ----------
    fname : str
        file or path name

    Returns
    -------
    pth : str
        base path from fname
    fname : str
        filename from fname, without extension
    ext : str
        file extension from fname

    Examples
    --------
    >>> from nipype.utils.filemanip import split_filename
    >>> pth, fname, ext = split_filename('/home/data/subject.nii.gz')
    >>> pth
    '/home/data'

    >>> fname
    'subject'

    >>> ext
    '.nii.gz'

    """

    special_extensions = [".nii.gz", ".tar.gz", ".niml.dset"]

    pth = op.dirname(fname)
    fname = op.basename(fname)

    ext = None
    for special_ext in special_extensions:
        ext_len = len(special_ext)
        if (len(fname) > ext_len) and (fname[-ext_len:].lower() == special_ext.lower()):
            ext = fname[-ext_len:]
            fname = fname[:-ext_len]
            break
    if not ext:
        fname, ext = op.splitext(fname)

    return pth, fname, ext


# Original source at L1069 of <nipype-install>/interfaces/base/core.py
class PackageInfo(object):
    _version = None
    version_cmd = None
    version_file = None

    @classmethod
    def version(klass):
        if klass._version is None:
            if klass.version_cmd is not None:
                try:
                    clout = CommandLine(
                        command=klass.version_cmd,
                        resource_monitor=False,
                        terminal_output="allatonce",
                    ).run()
                except IOError:
                    return None

                raw_info = clout.runtime.stdout
            elif klass.version_file is not None:
                try:
                    with open(klass.version_file, "rt") as fobj:
                        raw_info = fobj.read()
                except OSError:
                    return None
            else:
                return None

            klass._version = klass.parse_version(raw_info)

        return klass._version

    @staticmethod
    def parse_version(raw_info):
        raise NotImplementedError


# Original source at L40 of <nipype-install>/interfaces/fsl/base.py
class Info(PackageInfo):
    """
    Handle FSL ``output_type`` and version information.

    output type refers to the type of file fsl defaults to writing
    eg, NIFTI, NIFTI_GZ

    Examples
    --------

    >>> from nipype.interfaces.fsl import Info
    >>> Info.version()  # doctest: +SKIP
    >>> Info.output_type()  # doctest: +SKIP

    """

    ftypes = {
        "NIFTI": ".nii",
        "NIFTI_PAIR": ".img",
        "NIFTI_GZ": ".nii.gz",
        "NIFTI_PAIR_GZ": ".img.gz",
    }

    if os.getenv("FSLDIR"):
        version_file = os.path.join(os.getenv("FSLDIR"), "etc", "fslversion")

    @staticmethod
    def parse_version(raw_info):
        return raw_info.splitlines()[0]

    @classmethod
    def output_type_to_ext(cls, output_type):
        """Get the file extension for the given output type.

        Parameters
        ----------
        output_type : {'NIFTI', 'NIFTI_GZ', 'NIFTI_PAIR', 'NIFTI_PAIR_GZ'}
            String specifying the output type.

        Returns
        -------
        extension : str
            The file extension for the output type.
        """

        try:
            return cls.ftypes[output_type]
        except KeyError:
            msg = "Invalid FSLOUTPUTTYPE: ", output_type
            raise KeyError(msg)

    @classmethod
    def output_type(cls):
        """Get the global FSL output file type FSLOUTPUTTYPE.

        This returns the value of the environment variable
        FSLOUTPUTTYPE.  An exception is raised if it is not defined.

        Returns
        -------
        fsl_ftype : string
            Represents the current environment setting of FSLOUTPUTTYPE
        """
        try:
            return os.environ["FSLOUTPUTTYPE"]
        except KeyError:
            IFLOGGER.warning(
                "FSLOUTPUTTYPE environment variable is not set. "
                "Setting FSLOUTPUTTYPE=NIFTI"
            )
            return "NIFTI"

    @staticmethod
    def standard_image(img_name=None):
        """Grab an image from the standard location.

        Returns a list of standard images if called without arguments.

        Could be made more fancy to allow for more relocatability"""
        try:
            fsldir = os.environ["FSLDIR"]
        except KeyError:
            raise Exception("FSL environment variables not set")
        stdpath = os.path.join(fsldir, "data", "standard")
        if img_name is None:
            return [
                filename.replace(stdpath + "/", "")
                for filename in glob(os.path.join(stdpath, "*nii*"))
            ]
        return os.path.join(stdpath, img_name)
