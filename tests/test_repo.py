# -*- coding: utf-8 -*-

from unittest.mock import patch

import pytest
from typer import Exit
from typer.testing import CliRunner

from bb.repo import _repo
from bb.repo.archive import archive_repository
from bb.repo.create import create_repository
from bb.repo.delete import delete_repository

runner = CliRunner()


def test_archive_repository_success():
    with patch("bb.repo.archive.confirm", return_value=True):
        with patch("bb.repo.archive.put", return_value=[200, "OK"]):
            with patch("bb.repo.archive.live_progress") as mock_live:
                mock_live.return_value.__enter__ = mock_live
                mock_live.return_value.__exit__ = lambda *args: None
                archive_repository("proj", "repo", True)


def test_archive_repository_conflict():
    with patch("bb.repo.archive.confirm", return_value=True):
        with patch(
            "bb.repo.archive.put",
            return_value=[409, {"errors": [{"message": "conflict"}]}],
        ):
            with patch("bb.repo.archive.live_progress") as mock_live:
                mock_live.return_value.__enter__ = mock_live
                mock_live.return_value.__exit__ = lambda *args: None
                archive_repository("proj", "repo", True)


def test_archive_repository_cancelled():
    with patch("bb.repo.archive.confirm", return_value=False):
        with pytest.raises(Exit):
            archive_repository("proj", "repo", True)


def test_create_repository_success():
    with patch("bb.repo.create.post", return_value=[200, "OK"]):
        with patch("bb.repo.create.live_progress") as mock_live:
            mock_live.return_value.__enter__ = mock_live
            mock_live.return_value.__exit__ = lambda *args: None
            create_repository("proj", "repo", False, "main")


def test_create_repository_conflict():
    with patch(
        "bb.repo.create.post", return_value=[409, {"errors": [{"message": "conflict"}]}]
    ):
        with patch("bb.repo.create.live_progress") as mock_live:
            mock_live.return_value.__enter__ = mock_live
            mock_live.return_value.__exit__ = lambda *args: None
            create_repository("proj", "repo", False, "main")


def test_delete_repository_success():
    with patch("bb.repo.delete.prompt", return_value="proj/repo"):
        with patch("bb.repo.delete.confirm", return_value=True):
            with patch("bb.repo.delete.delete_request", return_value=202):
                with patch("bb.repo.delete.live_progress") as mock_live:
                    mock_live.return_value.__enter__ = mock_live
                    mock_live.return_value.__exit__ = lambda *args: None
                    delete_repository("proj", "repo")


def test_delete_repository_cancelled():
    with patch("bb.repo.delete.prompt", return_value="wrong"):
        with pytest.raises(Exit):
            delete_repository("proj", "repo")


@patch("bb.utils.helper.prompt", return_value="test")
@patch("bb.repo.archive_repository")
def test_archive(mock_archive, mock_prompt):
    result = runner.invoke(_repo, ["archive", "--project", "demo", "--repo", "test"])
    assert result.exit_code == 0
    mock_archive.assert_called_once_with("demo", "test", True)


@patch("bb.repo.parse", return_value=["u", "t", "host"])
@patch("bb.repo.clone_repo")
def test_clone(mock_clone, mock_parse):
    result = runner.invoke(_repo, ["clone", "demo/test"])
    assert result.exit_code == 0
    mock_clone.assert_called_once_with("demo/test", "host")


@patch("bb.utils.helper.prompt", return_value="test")
@patch("bb.repo.create_repository")
def test_create(mock_create, mock_prompt):
    result = runner.invoke(_repo, ["create", "--project", "demo", "--repo", "test"])
    assert result.exit_code == 0
    mock_create.assert_called_once_with("demo", "test", False, "master")


@patch("bb.utils.helper.prompt", return_value="test")
@patch("bb.repo.delete_repository")
def test_delete(mock_delete, mock_prompt):
    result = runner.invoke(_repo, ["delete", "--project", "demo", "--repo", "test"])
    assert result.exit_code == 0
    mock_delete.assert_called_once_with("demo", "test")


@patch("bb.utils.helper.prompt", return_value="test")
@patch("bb.repo.archive_repository")
def test_unarchive(mock_archive, mock_prompt):
    result = runner.invoke(_repo, ["unarchive", "--project", "demo", "--repo", "test"])
    assert result.exit_code == 0
    mock_archive.assert_called_once_with("demo", "test", False)
