"""Module to put any functions that are referred to in the "callables" section of TractSkeleton.yaml"""

import attrs
import os.path as op
from pathlib import Path


def projected_data_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["projected_data"]


def skeleton_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["skeleton_file"]


# Original source at L885 of <nipype-install>/interfaces/base/core.py
def _gen_filename(name, inputs=None, stdout=None, stderr=None, output_dir=None):
    raise NotImplementedError


# Original source at L1445 of <nipype-install>/interfaces/fsl/dti.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    outputs = {}
    _si = inputs
    if (_si.project_data is not attrs.NOTHING) and _si.project_data:
        proj_data = _si.projected_data
        outputs["projected_data"] = proj_data
        if proj_data is attrs.NOTHING:
            stem = _si.data_file
            if _si.alt_data_file is not attrs.NOTHING:
                stem = _si.alt_data_file
            outputs["projected_data"] = fname_presuffix(
                stem, suffix="_skeletonised", newpath=output_dir, use_ext=True
            )
    if (_si.skeleton_file is not attrs.NOTHING) and _si.skeleton_file:
        outputs["skeleton_file"] = _si.skeleton_file
        if isinstance(_si.skeleton_file, bool):
            outputs["skeleton_file"] = fname_presuffix(
                _si.in_file, suffix="_skeleton", newpath=output_dir, use_ext=True
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
