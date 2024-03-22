#!/usr/bin/env python3
from pathlib import Path
import json
import yaml
import click


@click.command
@click.argument(
    "out_json_path",
    type=click.Path(path_type=Path),
    help="The output path to save the report",
)
def report_progress(out_json_path: Path):

    out_json_path.parent.mkdir(exist_ok=True, parents=True)

    SPECS_DIR = Path(__file__).parent / "nipype-auto-conv" / "specs"

    report = {}

    for spec_path in SPECS_DIR.glob("*.yaml"):
        with open(spec_path) as f:
            spec = yaml.load(f, Loader=yaml.SafeLoader)

        report[spec["task_name"]] = {
            n: not s["xfail"] for n, s in spec["tests"].items()
        }

    with open(out_json_path, "w") as f:
        json.dump(report, f)
