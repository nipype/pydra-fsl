"""Module to put any functions that are referred to in the "callables" section of Level1Design.yaml"""

import os


def ev_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["ev_files"]


def fsf_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["fsf_files"]


# Original source at L343 of <nipype-install>/interfaces/fsl/model.py
def _format_session_info(
    session_info, inputs=None, stdout=None, stderr=None, output_dir=None
):
    if isinstance(session_info, dict):
        session_info = [session_info]
    return session_info


# Original source at L414 of <nipype-install>/interfaces/fsl/model.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    outputs = {}
    cwd = output_dir
    outputs["fsf_files"] = []
    outputs["ev_files"] = []
    basis_key = list(inputs.bases.keys())[0]
    ev_parameters = dict(inputs.bases[basis_key])
    for runno, runinfo in enumerate(
        _format_session_info(
            inputs.session_info,
            inputs=inputs,
            stdout=stdout,
            stderr=stderr,
            output_dir=output_dir,
        )
    ):
        outputs["fsf_files"].append(os.path.join(cwd, "run%d.fsf" % runno))
        outputs["ev_files"].insert(runno, [])
        evname = []
        for field in ["cond", "regress"]:
            for i, cond in enumerate(runinfo[field]):
                name = cond["name"]
                evname.append(name)
                evfname = os.path.join(
                    cwd, "ev_%s_%d_%d.txt" % (name, runno, len(evname))
                )
                if field == "cond":
                    ev_parameters["temporalderiv"] = int(
                        bool(ev_parameters.get("derivs", False))
                    )
                    if ev_parameters["temporalderiv"]:
                        evname.append(name + "TD")
                outputs["ev_files"][runno].append(os.path.join(cwd, evfname))
    return outputs
