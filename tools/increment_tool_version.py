#!/usr/bin/env python3
from pathlib import Path
import inspect
from importlib import import_module
import click
from looseversion import LooseVersion
from pydra.engine.core import TaskBase


PKG_DIR = Path(__file__).parent.parent
TASKS_DIR = PKG_DIR / "pydra" / "tasks" / "ants"
VERSION_GRANULARITY = (
    2  # Number of version parts to include: 1 - major, 2 - minor, 3 - micro
)


@click.command(
    help="""Increment the latest version or create a new sub-package for interfaces for
a new release of AFNI depending on whether one already exists or not.

NEW_VERSION the version of AFNI to create a new sub-package for
"""
)
@click.argument("new_version", type=LooseVersion)
def increment_tool_version(new_version: LooseVersion):

    # Get the name of the sub-package, e.g. "v2_5"
    new_subpkg_name = "_".join(str(p) for p in new_version.version[:VERSION_GRANULARITY])  # type: ignore
    if not new_subpkg_name.startswith("v"):
        new_subpkg_name = "v" + new_subpkg_name
    sub_pkg_dir = TASKS_DIR / new_subpkg_name
    if not sub_pkg_dir.exists():

        prev_version = sorted(
            (
                p.name
                for p in TASKS_DIR.iterdir()
                if p.is_dir() and p.name.startswith("v")
            ),
            key=lambda x: LooseVersion(".".join(x.split("_"))).version,
        )[-1]
        prev_ver_mod = import_module(f"pydra.tasks.ants.{prev_version}")

        mod_attrs = [getattr(prev_ver_mod, a) for a in dir(prev_ver_mod)]
        task_classes = [
            a for a in mod_attrs if inspect.isclass(a) and issubclass(a, TaskBase)
        ]

        code_str = (
            f"from pydra.tasks.ants import {prev_version}\n"
            "from . import _tool_version\n"
        )

        for task_cls in task_classes:
            code_str += (
                f"\n\nclass {task_cls.__name__}({prev_version}.{task_cls.__name__}):\n"
                "    TOOL_VERSION = _tool_version.TOOL_VERSION\n"
            )

        sub_pkg_dir.mkdir(exist_ok=True)
        with open(sub_pkg_dir / "__init__.py", "w") as f:
            f.write(code_str)

    with open(sub_pkg_dir / "_tool_version.py", "w") as f:
        f.write(f'TOOL_VERSION = "{new_version}"\n')


if __name__ == "__main__":
    increment_tool_version()
