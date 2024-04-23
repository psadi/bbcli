# -*- coding: utf-8 -*-

from typer.testing import CliRunner

from bb.repo import _repo

runner = CliRunner()


def test_archive():
    result = runner.invoke(_repo, ["archive", "--project", "demo", "--repo", "test"])
    assert result.exit_code == 0


def test_clone():
    result = runner.invoke(_repo, ["clone", "demo/test"])
    assert result.exit_code == 0


def test_create():
    result = runner.invoke(_repo, ["create", "--project", "demo", "--repo", "test"])
    assert result.exit_code == 0


def test_delete():
    result = runner.invoke(_repo, ["create", "--project", "demo", "--repo", "test"])
    assert result.exit_code == 0


def test_unarchive():
    result = runner.invoke(_repo, ["unarchive", "--project", "demo", "--repo", "test"])
    assert result.exit_code == 0
