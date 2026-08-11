import attrs
from fileformats.generic import File
import logging
import os
from pydra.compose import python
import typing as ty


logger = logging.getLogger(__name__)


@python.define
class L2Model(python.Task["L2Model.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fsl.v6.model.l2_model import L2Model

    """

    num_copes: ty.Any

    class Outputs(python.Outputs):
        design_mat: File
        design_con: File
        design_grp: File

    @staticmethod
    def function(num_copes: ty.Any) -> tuple[File, File, File]:
        design_mat = attrs.NOTHING
        design_con = attrs.NOTHING
        design_grp = attrs.NOTHING
        cwd = os.getcwd()
        mat_txt = [
            "/NumWaves   1",
            f"/NumPoints  {num_copes:d}",
            "/PPheights  1",
            "",
            "/Matrix",
        ]
        for i in range(num_copes):
            mat_txt += ["1"]
        mat_txt = "\n".join(mat_txt)

        con_txt = [
            "/ContrastName1  group mean",
            "/NumWaves   1",
            "/NumContrasts   1",
            "/PPheights  1",
            "/RequiredEffect     100",  # XX where does this
            "",
            "/Matrix",
            "1",
        ]
        con_txt = "\n".join(con_txt)

        grp_txt = [
            "/NumWaves   1",
            f"/NumPoints  {num_copes:d}",
            "",
            "/Matrix",
        ]
        for i in range(num_copes):
            grp_txt += ["1"]
        grp_txt = "\n".join(grp_txt)

        txt = {"design.mat": mat_txt, "design.con": con_txt, "design.grp": grp_txt}

        for i, name in enumerate(["design.mat", "design.con", "design.grp"]):
            with open(os.path.join(cwd, name), "w") as f:
                f.write(txt[name])

        outputs = {}
        for field in list(outputs["keys"]()):
            outputs[field] = os.path.join(os.getcwd(), field.replace("_", "."))

        return design_mat, design_con, design_grp
