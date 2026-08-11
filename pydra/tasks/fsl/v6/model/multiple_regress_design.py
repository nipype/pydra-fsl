import attrs
from fileformats.generic import File
import logging
import numpy as np
import os
from pydra.compose import python
import typing as ty


logger = logging.getLogger(__name__)


@python.define
class MultipleRegressDesign(python.Task["MultipleRegressDesign.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fsl.v6.model.multiple_regress_design import MultipleRegressDesign

    """

    contrasts: list[ty.Any]
    regressors: dict
    groups: list[int]

    class Outputs(python.Outputs):
        design_mat: File
        design_con: File
        design_fts: File
        design_grp: File

    @staticmethod
    def function(
        contrasts: list[ty.Any], regressors: dict, groups: list[int]
    ) -> tuple[File, File, File, File]:
        design_mat = attrs.NOTHING
        design_con = attrs.NOTHING
        design_fts = attrs.NOTHING
        design_grp = attrs.NOTHING
        cwd = os.getcwd()
        regs = sorted(regressors.keys())
        nwaves = len(regs)
        npoints = len(regressors[regs[0]])
        ntcons = sum(1 for con in contrasts if con[1] == "T")
        nfcons = sum(1 for con in contrasts if con[1] == "F")

        mat_txt = ["/NumWaves       %d" % nwaves, "/NumPoints      %d" % npoints]
        ppheights = []
        for reg in regs:
            maxreg = np.max(regressors[reg])
            minreg = np.min(regressors[reg])
            if np.sign(maxreg) == np.sign(minreg):
                regheight = max([abs(minreg), abs(maxreg)])
            else:
                regheight = abs(maxreg - minreg)
            ppheights.append("%e" % regheight)
        mat_txt += ["/PPheights      " + " ".join(ppheights)]
        mat_txt += ["", "/Matrix"]
        for cidx in range(npoints):
            mat_txt.append(" ".join(["%e" % regressors[key][cidx] for key in regs]))
        mat_txt = "\n".join(mat_txt) + "\n"

        con_txt = []
        counter = 0
        tconmap = {}
        for conidx, con in enumerate(contrasts):
            if con[1] == "T":
                tconmap[conidx] = counter
                counter += 1
                con_txt += ["/ContrastName%d   %s" % (counter, con[0])]
        con_txt += [
            "/NumWaves       %d" % nwaves,
            "/NumContrasts   %d" % ntcons,
            "/PPheights          %s" % " ".join(["%e" % 1 for i in range(counter)]),
            "/RequiredEffect     %s" % " ".join(["%.3f" % 100 for i in range(counter)]),
            "",
            "/Matrix",
        ]
        for idx in sorted(tconmap.keys()):
            convals = np.zeros((nwaves, 1))
            for regidx, reg in enumerate(contrasts[idx][2]):
                convals[regs.index(reg)] = contrasts[idx][3][regidx]
            con_txt.append(" ".join(["%e" % val for val in convals]))
        con_txt = "\n".join(con_txt) + "\n"

        fcon_txt = ""
        if nfcons:
            fcon_txt = [
                "/NumWaves       %d" % ntcons,
                "/NumContrasts   %d" % nfcons,
                "",
                "/Matrix",
            ]
            for conidx, con in enumerate(contrasts):
                if con[1] == "F":
                    convals = np.zeros((ntcons, 1))
                    for tcon in con[2]:
                        convals[tconmap[contrasts.index(tcon)]] = 1
                    fcon_txt.append(" ".join(["%d" % val for val in convals]))
            fcon_txt = "\n".join(fcon_txt) + "\n"

        grp_txt = ["/NumWaves       1", "/NumPoints      %d" % npoints, "", "/Matrix"]
        for i in range(npoints):
            if groups is not attrs.NOTHING:
                grp_txt += ["%d" % groups[i]]
            else:
                grp_txt += ["1"]
        grp_txt = "\n".join(grp_txt) + "\n"

        txt = {
            "design.mat": mat_txt,
            "design.con": con_txt,
            "design.fts": fcon_txt,
            "design.grp": grp_txt,
        }

        for key, val in list(txt.items()):
            if ("fts" in key) and (nfcons == 0):
                continue
            filename = key.replace("_", ".")
            with open(os.path.join(cwd, filename), "w") as f:
                f.write(val)

        outputs = {}
        nfcons = sum(1 for con in contrasts if con[1] == "F")
        for field in list(outputs["keys"]()):
            if ("fts" in field) and (nfcons == 0):
                continue
            outputs[field] = os.path.join(os.getcwd(), field.replace("_", "."))

        return design_mat, design_con, design_fts, design_grp
