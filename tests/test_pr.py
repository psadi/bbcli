# -*- coding: utf-8 -*-

from typer.testing import CliRunner

from bb.pr import _pr

runner = CliRunner()


def test_create():
    result = runner.invoke(_pr, ["create", "--target", "main", "--yes"])
    assert result.exit_code == 0
    result = runner.invoke(
        _pr, ["create", "--target", "main", "--yes", "--diff", "--rebase"]
    )
    assert result.exit_code == 0


def test_delete():
    result = runner.invoke(_pr, ["delete", "--id", "0", "--yes"])
    assert result.exit_code == 0


def test_copy():
    result = runner.invoke(_pr, ["copy", "--id", "0"])
    assert result.exit_code == 0


def test_diff():
    result = runner.invoke(_pr, ["diff", "--id", "0"])
    assert result.exit_code == 0


def test_list():
    result = runner.invoke(_pr, ["list"])
    assert result.exit_code == 0


def test_merge():
    result = runner.invoke(_pr, ["merge", "--id", "0", "--yes"])
    assert result.exit_code == 0


def test_review():
    result = runner.invoke(_pr, ["review", "--id", "0"])
    assert result.exit_code == 0


def test_view():
    result = runner.invoke(_pr, ["view", "--id", "0"])
    assert result.exit_code == 0
