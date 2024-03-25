"""Module to put any functions that are referred to in the "callables" section of WarpPoints.yaml"""

import attrs
import logging
import os
import os.path as op


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_file"]


iflogger = logging.getLogger("nipype.interface")


# Original source at L809 of <nipype-install>/interfaces/base/core.py
def _filename_from_source(
    name, chain=None, inputs=None, stdout=None, stderr=None, output_dir=None
):
    if chain is None:
        chain = []

    trait_spec = inputs.trait(name)
    retval = getattr(inputs, name)
    source_ext = None
    if (retval is attrs.NOTHING) or "%s" in retval:
        if not trait_spec.name_source:
            return retval

        # Do not generate filename when excluded by other inputs
        if any(
            (getattr(inputs, field) is not attrs.NOTHING)
            for field in trait_spec.xor or ()
        ):
            return retval

        # Do not generate filename when required fields are missing
        if not all(
            (getattr(inputs, field) is not attrs.NOTHING)
            for field in trait_spec.requires or ()
        ):
            return retval

        if (retval is not attrs.NOTHING) and "%s" in retval:
            name_template = retval
        else:
            name_template = trait_spec.name_template
        if not name_template:
            name_template = "%s_generated"

        ns = trait_spec.name_source
        while isinstance(ns, (list, tuple)):
            if len(ns) > 1:
                iflogger.warning("Only one name_source per trait is allowed")
            ns = ns[0]

        if not isinstance(ns, (str, bytes)):
            raise ValueError(
                "name_source of '{}' trait should be an input trait "
                "name, but a type {} object was found".format(name, type(ns))
            )

        if getattr(inputs, ns) is not attrs.NOTHING:
            name_source = ns
            source = getattr(inputs, name_source)
            while isinstance(source, list):
                source = source[0]

            # special treatment for files
            try:
                _, base, source_ext = split_filename(source)
            except (AttributeError, TypeError):
                base = source
        else:
            if name in chain:
                raise NipypeInterfaceError("Mutually pointing name_sources")

            chain.append(name)
            base = _filename_from_source(
                ns,
                chain,
                inputs=inputs,
                stdout=stdout,
                stderr=stderr,
                output_dir=output_dir,
            )
            if base is not attrs.NOTHING:
                _, _, source_ext = split_filename(base)
            else:
                # Do not generate filename when required fields are missing
                return retval

        chain = None
        retval = name_template % base
        _, _, ext = split_filename(retval)
        if trait_spec.keep_extension and (ext or source_ext):
            if (ext is None or not ext) and source_ext:
                retval = retval + source_ext
        else:
            retval = _overload_extension(
                retval,
                name,
                inputs=inputs,
                stdout=stdout,
                stderr=stderr,
                output_dir=output_dir,
            )
    return retval


# Original source at L885 of <nipype-install>/interfaces/base/core.py
def _gen_filename(name, inputs=None, stdout=None, stderr=None, output_dir=None):
    raise NotImplementedError


# Original source at L891 of <nipype-install>/interfaces/base/core.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    metadata = dict(name_source=lambda t: t is not None)
    traits = inputs.traits(**metadata)
    if traits:
        outputs = {}
        for name, trait_spec in list(traits.items()):
            out_name = name
            if trait_spec.output_name is not None:
                out_name = trait_spec.output_name
            fname = _filename_from_source(
                name, inputs=inputs, stdout=stdout, stderr=stderr, output_dir=output_dir
            )
            if fname is not attrs.NOTHING:
                outputs[out_name] = os.path.abspath(fname)
        return outputs


# Original source at L2585 of <nipype-install>/interfaces/fsl/utils.py
def _overload_extension(
    value, name, inputs=None, stdout=None, stderr=None, output_dir=None
):
    if name == "out_file":
        return "%s.%s" % (value, getattr(self, "_outformat"))


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


# Original source at L125 of <nipype-install>/interfaces/base/support.py
class NipypeInterfaceError(Exception):
    """Custom error for interfaces"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "{}".format(self.value)
