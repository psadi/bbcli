# -*- coding: utf-8 -*-

import toml
from typer.testing import CliRunner
from bb.main import _bb

runner = CliRunner()


def version() -> str:
    return toml.load("pyproject.toml")["tool"]["poetry"]["version"]


def test_version():
    result = runner.invoke(_bb, ["--version"])
    assert result.exit_code == 0
    test_list: list = ["psadi", "adithya3494@gmail.com", "MIT"]
    for item in test_list:
        assert item in result.stdout
