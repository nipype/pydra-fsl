from pathlib import Path
from click.testing import CliRunner
from nipype2pydra.utils import show_cli_trace
from nipype2pydra.cli import convert

PKG_PATH = Path(__file__).parent.parent.absolute()

runner = CliRunner()


result = runner.invoke(
    convert,
    [
        str(PKG_PATH / "nipype-auto-conv" / "specs"),
        str(PKG_PATH),
    ],
    catch_exceptions=False,
)

assert not result.exit_code, show_cli_trace(result)
