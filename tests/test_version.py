# -*- coding: utf-8 -*-

import toml
from typer.testing import CliRunner
from bb import _bb

runner = CliRunner()


def version() -> str:
    return toml.load("pyproject.toml")["tool"]["poetry"]["version"]


def test_version():
    result = runner.invoke(_bb, ["--version"])
    assert result.exit_code == 0
    assert version() in result.stdout
