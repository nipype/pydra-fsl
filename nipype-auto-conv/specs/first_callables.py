"""Module to put any functions that are referred to in the "callables" section of FIRST.yaml"""

import attrs
import os.path as op


def bvars_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["bvars"]


def original_segmentations_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["original_segmentations"]


def segmentation_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["segmentation_file"]


def vtk_surfaces_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["vtk_surfaces"]


# Original source at L885 of <nipype-install>/interfaces/base/core.py
def _gen_filename(name, inputs=None, stdout=None, stderr=None, output_dir=None):
    raise NotImplementedError


# Original source at L2259 of <nipype-install>/interfaces/fsl/preprocess.py
def _gen_fname(basename, inputs=None, stdout=None, stderr=None, output_dir=None):
    path, outname, ext = split_filename(inputs.out_file)

    method = "none"
    if (inputs.method is not attrs.NOTHING) and inputs.method != "none":
        method = "fast"
        if inputs.list_of_specific_structures and inputs.method == "auto":
            method = "none"

    if inputs.method_as_numerical_threshold is not attrs.NOTHING:
        thres = "%.4f" % inputs.method_as_numerical_threshold
        method = thres.replace(".", "")

    if basename == "original_segmentations":
        return op.abspath("%s_all_%s_origsegs.nii.gz" % (outname, method))
    if basename == "segmentation_file":
        return op.abspath("%s_all_%s_firstseg.nii.gz" % (outname, method))

    return None


# Original source at L2279 of <nipype-install>/interfaces/fsl/preprocess.py
def _gen_mesh_names(
    name, structures, inputs=None, stdout=None, stderr=None, output_dir=None
):
    path, prefix, ext = split_filename(inputs.out_file)
    if name == "vtk_surfaces":
        vtks = list()
        for struct in structures:
            vtk = prefix + "-" + struct + "_first.vtk"
            vtks.append(op.abspath(vtk))
        return vtks
    if name == "bvars":
        bvars = list()
        for struct in structures:
            bvar = prefix + "-" + struct + "_first.bvars"
            bvars.append(op.abspath(bvar))
        return bvars
    return None


# Original source at L2230 of <nipype-install>/interfaces/fsl/preprocess.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    outputs = {}

    if inputs.list_of_specific_structures is not attrs.NOTHING:
        structures = inputs.list_of_specific_structures
    else:
        structures = [
            "L_Hipp",
            "R_Hipp",
            "L_Accu",
            "R_Accu",
            "L_Amyg",
            "R_Amyg",
            "L_Caud",
            "R_Caud",
            "L_Pall",
            "R_Pall",
            "L_Puta",
            "R_Puta",
            "L_Thal",
            "R_Thal",
            "BrStem",
        ]
    outputs["original_segmentations"] = _gen_fname(
        "original_segmentations",
        inputs=inputs,
        stdout=stdout,
        stderr=stderr,
        output_dir=output_dir,
    )
    outputs["segmentation_file"] = _gen_fname(
        "segmentation_file",
        inputs=inputs,
        stdout=stdout,
        stderr=stderr,
        output_dir=output_dir,
    )
    outputs["vtk_surfaces"] = _gen_mesh_names(
        "vtk_surfaces",
        structures,
        inputs=inputs,
        stdout=stdout,
        stderr=stderr,
        output_dir=output_dir,
    )
    outputs["bvars"] = _gen_mesh_names(
        "bvars",
        structures,
        inputs=inputs,
        stdout=stdout,
        stderr=stderr,
        output_dir=output_dir,
    )
    return outputs


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
