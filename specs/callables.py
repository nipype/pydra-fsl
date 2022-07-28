def Cluster_output(field, inputs):
    import os, attr
    from pydra.engine.helpers_file import split_filename

    in_file = inputs.in_file
    name = field.name
    pth, fname, ext = split_filename(in_file)
    
    if name == "index_file":
        return os.path.join(pth, f"{fname}_index{ext}")
    elif name == "localmax_txt_file":
        return os.path.join(pth, f"{fname}_localmax.txt")
    elif name == "localmax_vol_file":
        return os.path.join(pth, f"{fname}_localmax{ext}")
    elif name == "max_file":
        return os.path.join(pth, f"{fname}_max{ext}")
    elif name == "mean_file":
        return os.path.join(pth, f"{fname}_mean{ext}")
    elif name == "pval_file":
        return os.path.join(pth, f"{fname}_pval{ext}")
    elif name == "size_file":
        return os.path.join(pth, f"{fname}_size{ext}")
    elif name == "threshold_file":
        return os.path.join(pth, f"{fname}_threshold{ext}")

    else:
        raise Exception(f"this function should be run only for index_file, localmax_txt_file, localmax_vol_file, max_file, mean_file, pval_file, size_file, or threshold_file not {name}")


def Complex_output(inputs):
    import attr

    if inputs.complex_cartesian:
        in_file = inputs.real_in_file
    elif inputs.complex_polar:
        in_file = inputs.magnitude_in_file
    elif inputs.complex_split or inputs.complex_merge:
        in_file = inputs.complex_in_file
    else:
        return None
    return f"{in_file}_cplx"


def ConvertXFM_output(inputs):
    import attr

    in_file = inputs.in_file
    if inputs.invert_xfm:
        return f"{in_file}_inv"
    elif inputs.concat_xfm:
        if inputs.in_file2.exists():
            in_file2 = inputs.in_file2
            return f"{in_file}_{in_file2}"
        else:
            raise Exception("in_file2 is needed to use concat_xfm")

    elif inputs.fix_scale_skew:
        return f"{in_file}_fix"
    else:
        raise Exception("this function requires invert_xfm, or concat_xfm," "or fix_scale_skew")


def FAST_output(field, in_files, out_basename):
    import attr

    if out_basename in [None, attr.NOTHING]:
        out_basename = in_files[-1]
    name = field.name
    if name == "tissue_class_map":
        return f"{out_basename}_seg"
    elif name == "mixeltype":
        return f"{out_basename}_mixeltype"
    elif name == "partial_volume_map":
        return f"{out_basename}_pveseg"
    else:
        raise Exception(
            f"this function should be run only for issue_class_map, "
            f"or mixeltype, not for {name}"
        )

    outputs = []
    if len(in_files) > 1:
        # for multi-image segmentation there is one corrected image
        # per input
        for val, f in enumerate(in_files):
            # image numbering is 1-based
            outputs.append(f"{out_basename}_restore_{val+1}")
    else:
        # single image segmentation has unnumbered output image
        outputs.append(f"{out_basename}_restore")
    return outputs


def FAST_output_nclass(field, in_files, nclasses, out_basename):
    import attr

    if out_basename in [None, attr.NOTHING]:
        out_basename = in_files[-1]
    name = field.name

    if name == "tissue_class_files":
        suffix = "seg"
    elif name == "partial_volume_files":
        suffix = "pve"
    elif name == "probability_maps":
        suffix = "prob"
    else:
        raise Exception(
            f"this function should be run only for tissue_class_files, "
            f"partial_volume_files or probability_maps, not for {name}"
        )

    outputs = []
    for ii in range(nclasses):
        outputs.append(f"{out_basename}_{suffix}_{ii}")
    return outputs


def FAST_output_infile(field, in_files, out_basename):
    import attr

    if out_basename in [None, attr.NOTHING]:
        out_basename = in_files[-1]
    name = field.name
    if name == "restored_image":
        suffix = "restore"
    elif name == "bias_field":
        suffix = "bias"
    else:
        raise Exception(
            f"this function should be run only for restored_image, "
            f"or bias_field, not for {name}"
        )

    outputs = []
    if len(in_files) > 1:
        # for multi-image segmentation there is one corrected image
        # per input
        for val, f in enumerate(in_files):
            # image numbering is 1-based
            outputs.append(f"{out_basename}_{suffix}_{val+1}")
    else:
        # single image segmentation has unnumbered output image
        outputs.append(f"{out_basename}_{suffix}")
    return outputs


def FEAT_output(fsf_file):
    is_ica = False
    with open(fsf_file, "rt") as fp:
        text = fp.read()
        if "set fmri(inmelodic) 1" in text:
            is_ica = True
        for line in text.split("\n"):
            if line.find("set fmri(outputdir)") > -1:
                try:
                    outputdir_spec = line.split('"')[-2]
                    if os.path.exists(outputdir_spec):
                        outputs = outputdir_spec
                except:
                    pass

    if not outputs:
        if is_ica:
            outputs = glob(os.path.join(os.getcwd(), "*ica"))[0]
        else:
            outputs = glob(os.path.join(os.getcwd(), "*feat"))[0]
    print("Outputs from FEATmodel:", outputs)
    return outputs


def FEATModel_output(field, fsf_file):
    import os

    # TODO: figure out file names and get rid off the globs
    outputs = {}
    _, fname = os.path.split(fsf_file)
    root = fname.split(".")[0]
    name = field.name
    if name == "design_file":
        design_file = glob(os.path.join(os.getcwd(), "%s*.mat" % root))
        assert len(design_file) == 1, "No mat file generated by FEAT Model"
        outputs = design_file[0]
    elif name == "design_image":
        design_image = glob(os.path.join(os.getcwd(), "%s.png" % root))
        assert len(design_image) == 1, "No design image generated by FEAT Model"
        outputs = design_image[0]
    elif name == "design_cov":
        design_cov = glob(os.path.join(os.getcwd(), "%s_cov.png" % root))
        assert len(design_cov) == 1, "No covariance image generated by FEAT Model"
        outputs = design_cov[0]
    elif name == "con_file":
        con_file = glob(os.path.join(os.getcwd(), "%s*.con" % root))
        assert len(con_file) == 1, "No con file generated by FEAT Model"
        outputs = con_file[0]
    elif name == "fcon_file":
        fcon_file = glob(os.path.join(os.getcwd(), "%s*.fts" % root))
        if fcon_file:
            assert len(fcon_file) == 1, "No fts file generated by FEAT Model"
            outputs = fcon_file[0]
    else:
        raise Exception(
            f"this function should be run only for design_file, design_image"
            f"design_cov, con_file, or fcon_file, not for {name}"
        )
    return outputs


def FILMGLS_output(field, inputs):
    import os, attr

    def _get_pe_files(design_file, pth):
        files = None
        if design_file not in [None, attr.NOTHING]:
            fp = open(design_file, "rt")
            for line in fp.readlines():
                if line.startswith("/NumWaves"):
                    numpes = int(line.split()[-1])
                    files = []
                    for i in range(numpes):
                        files.append(os.path.join(pth, ("pe%d.nii.gz" % (i + 1))))
                    break
            fp.close()
        return files

    def _get_numcons(inputs):
        numtcons = 0
        numfcons = 0
        if inputs.tcon_file not in [None, attr.NOTHING]:
            fp = open(inputs.tcon_file, "rt")
            for line in fp.readlines():
                if line.startswith("/NumContrasts"):
                    numtcons = int(line.split()[-1])
                    break
            fp.close()
        if inputs.fcon_file not in [None, attr.NOTHING]:
            fp = open(inputs.fcon_file, "rt")
            for line in fp.readlines():
                if line.startswith("/NumContrasts"):
                    numfcons = int(line.split()[-1])
                    break
            fp.close()
        return numtcons, numfcons

    name = field.name
    pth = inputs.results_dir
    if name == "results_dir":
        return pth
    elif name == "param_estimates":
        design_file = inputs.design_file
        pe_files = _get_pe_files(design_file, pth)
        if pe_files:
            return pe_files
    elif name == "residual4d":
        return os.path.join(pth, "res4d.nii.gz")
    elif name == "dof_file":
        return os.path.join(pth, "dof")
    elif name == "sigmasquareds":
        return os.path.join(pth, "sigmasquareds.nii.gz")
    elif name == "thresholdac":
        return os.path.join(pth, "threshac1.nii.gz")
    elif name == "logfile":
        return os.path.join(pth, "logfile")

    numtcons, numfcons = _get_numcons(inputs)
    base_contrast = 1
    copes = []
    varcopes = []
    zstats = []
    tstats = []
    for i in range(numtcons):
        copes.append(os.path.join(pth, ("cope%d.nii.gz" % (base_contrast + i))))
        varcopes.append(os.path.join(pth, ("varcope%d.nii.gz" % (base_contrast + i))))
        zstats.append(os.path.join(pth, ("zstat%d.nii.gz" % (base_contrast + i))))
        tstats.append(os.path.join(pth, ("tstat%d.nii.gz" % (base_contrast + i))))
    if copes:
        if name == "copes":
            return copes
        elif name == "varcopes":
            return varcopes
        elif name == "zstats":
            return zstats
        elif name == "tstats":
            return tstats
    fstats = []
    zfstats = []
    for i in range(numfcons):
        fstats.append(os.path.join(pth, ("fstat%d.nii.gz" % (base_contrast + i))))
        zfstats.append(os.path.join(pth, ("zfstat%d.nii.gz" % (base_contrast + i))))
    if fstats:
        if name == "fstats":
            return fstats
        elif name == "zfstats":
            return


def FLAMEO_output(field, inputs):
    import os, glob, attr

    def human_order_sorted(l):
        """
        Sorts string in human order (i.e. 'stat10' will go after 'stat2')
        """

        def atoi(text):
            return int(text) if text.isdigit() else text

        def natural_keys(text):
            import re

            if isinstance(text, tuple):
                text = text[0]
            return [atoi(c) for c in re.split(r"(\d+)", text)]

        return sorted(l, key=natural_keys)

    pth = inputs.log_dir
    name = field.name

    if name == "pes":
        pes = human_order_sorted(glob.glob(os.path.join(pth, "pe[0-9]*.*")))
        if len(pes) >= 1:
            return pes
    elif name == "res4d":
        res4d = human_order_sorted(glob.glob(os.path.join(pth, "res4d.*")))
        if len(res4d) == 1:
            return res4d[0]
    elif name == "copes":
        copes = human_order_sorted(glob.glob(os.path.join(pth, "cope[0-9]*.*")))
        if len(copes) >= 1:
            return copes
    elif name == "var_copes":
        var_copes = human_order_sorted(glob.glob(os.path.join(pth, "varcope[0-9]*.*")))
        if len(var_copes) >= 1:
            return var_copes
    elif name == "zstats":
        zstats = human_order_sorted(glob.glob(os.path.join(pth, "zstat[0-9]*.*")))
        if len(zstats) >= 1:
            return zstats
    elif name == "tstats":
        tstats = human_order_sorted(glob.glob(os.path.join(pth, "tstat[0-9]*.*")))
        if len(tstats) >= 1:
            return tstats
    elif name == "mrefvars":
        mrefs = human_order_sorted(glob.glob(os.path.join(pth, "mean_random_effects_var[0-9]*.*")))
        if len(mrefs) >= 1:
            return mrefs
    elif name == "tdof":
        tdof = human_order_sorted(glob.glob(os.path.join(pth, "tdof_t[0-9]*.*")))
        if len(tdof) >= 1:
            return tdof
    elif name == "weights":
        weights = human_order_sorted(glob.glob(os.path.join(pth, "weights[0-9]*.*")))
        if len(weights) >= 1:
            return weights
    elif name == "stats_dir":
        return pth
    elif inputs.f_con_file not in [None, attr.NOTHING]:
        if name == "zfstats":
            zfstats = human_order_sorted(glob.glob(os.path.join(pth, "zfstat[0-9]*.*")))
            if len(zfstats) >= 1:
                return zfstats
        elif name == "fstats":
            fstats = human_order_sorted(glob.glob(os.path.join(pth, "fstat[0-9]*.*")))
            if len(fstats) >= 1:
                return fstats
    else:
        raise Exception(
            f"this function should be run only for pes, res4d, copes, var_copes, zfstats,"
            f"fstats, zstats, tstats, mrefs, tdof, weights, or stats_dir, not for {name}"
        )


def MELODIC_output(field, inputs):
    import os, attr

    name = field.name
    if name == "out_dir":
        if inputs.out_dir not in [None, attr.NOTHING]:
            outputs = inputs.out_dir
        else:
            outputs = os.getcwd()
    elif name == "report_dir":
        if inputs.report not in [None, attr.NOTHING]:
            if inputs.out_dir not in [None, attr.NOTHING]:
                out_dir = inputs.out_dir
            else:
                out_dir = os.getcwd()
            outputs = os.path.join(out_dir, "report")
    return outputs


def SLICE_output(inputs):
    import glob

    suffix = "slice_*"
    if inputs.out_base_name:
        fname_template = f"{inputs.out_base_name}_{suffix}"
    else:
        fname_template = f"{inputs.in_file}_{suffix}"

    return sorted(glob(fname_template))
