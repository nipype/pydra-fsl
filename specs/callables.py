
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
        raise Exception(f"this function should be run only for issue_class_map, "
                        f"or mixeltype, not for {name}")

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
        raise Exception(f"this function should be run only for tissue_class_files, "
                        f"partial_volume_files or probability_maps, not for {name}")


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
        raise Exception(f"this function should be run only for restored_image, "
                        f"or bias_field, not for {name}")



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
