# -*- coding: utf-8 -*-

import subprocess
from unittest.mock import MagicMock, patch

import pytest
from props import Cmnd

from bb.utils import cmnd

property = Cmnd()


@patch("bb.utils.cmnd.subprocess_run")
def test_base_repo(mock_subprocess_run):
    mock_subprocess_run.return_value = "origin\thttps://bitbucket.org/myproject/myrepo.git (fetch)\norigin\thttps://bitbucket.org/myproject/myrepo.git (push)"
    assert cmnd.base_repo() == ["myproject", "myrepo"]


@patch("bb.utils.cmnd.subprocess_run")
def test_from_branch(mock_subprocess_run):
    mock_subprocess_run.return_value = "main"
    assert cmnd.from_branch() == "main"


@patch("bb.utils.cmnd.subprocess_run")
def test_git_rebase(mock_subprocess_run):
    cmnd.git_rebase("main")
    assert mock_subprocess_run.call_count == 2
    mock_subprocess_run.assert_any_call("git pull --rebase origin main")
    mock_subprocess_run.assert_any_call("git push --force-with-lease")


@patch("bb.utils.cmnd.subprocess_run")
def test_title_and_description(mock_subprocess_run):
    mock_subprocess_run.return_value = "My Title\n\nMy Description\nLine 2"
    assert cmnd.title_and_description() == ["My Title", "My Description\nLine 2"]


@patch("bb.utils.cmnd.subprocess_run")
def test_is_git_repo(mock_subprocess_run):
    mock_subprocess_run.return_value = "true"
    assert cmnd.is_git_repo() is True


@patch("bb.utils.cmnd.subprocess_run")
def test_is_git_repo_false(mock_subprocess_run):
    mock_subprocess_run.return_value = "false"
    assert cmnd.is_git_repo() is False


@patch("bb.utils.cmnd.subprocess.run")
def test_subprocess_run(mock_run):
    mock_process = MagicMock()
    mock_process.stdout = b"output\n"
    mock_run.return_value = mock_process
    assert cmnd.subprocess_run("ls") == "output"


@patch("bb.utils.cmnd.console.print")
@patch("bb.utils.cmnd.subprocess.run")
def test_subprocess_run_error(mock_run, mock_print):
    mock_run.side_effect = subprocess.CalledProcessError(
        1, "cmd", output=b"", stderr=b"error output"
    )
    with pytest.raises(ValueError):
        cmnd.subprocess_run("ls")


@patch("bb.utils.cmnd.subprocess_run")
def test_cp_to_clipboard(mock_subprocess_run):
    # This is a bit tricky to test across platforms, but we can verify subprocess_run is called
    cmnd.cp_to_clipboard("test text")
    mock_subprocess_run.assert_called()


@patch("bb.utils.cmnd.subprocess.check_call")
def test_show_git_diff(mock_check_call):
    cmnd.show_git_diff("source", "target")
    mock_check_call.assert_called_once_with(["git", "diff", "target", "source"])


@patch("bb.utils.cmnd.subprocess.check_call")
def test_clone_repo(mock_check_call):
    cmnd.clone_repo("myproject/myrepo", "https://bitbucket.org")
    mock_check_call.assert_called_once_with(
        ["git", "clone", "https://bitbucket.org/scm/myproject/myrepo.git", "myrepo"]
    )


@patch("bb.utils.cmnd.subprocess.check_call")
@patch("bb.utils.cmnd.from_branch", return_value="main")
def test_delete_local_branch(mock_from_branch, mock_check_call):
    cmnd.delete_local_branch("feature-branch")
    mock_check_call.assert_called_once_with(["git", "branch", "-D", "feature-branch"])


@patch("bb.utils.cmnd.from_branch", return_value="main")
def test_delete_local_branch_active(mock_from_branch):
    with pytest.raises(ValueError, match="Cannot delete active branch 'main'"):
        cmnd.delete_local_branch("main")


@patch("bb.utils.cmnd.subprocess.check_call")
@patch("bb.utils.cmnd.subprocess_run", return_value="")
def test_checkout_and_pull(mock_subprocess_run, mock_check_call):
    cmnd.checkout_and_pull("main")
    assert mock_check_call.call_count == 2
    mock_check_call.assert_any_call(["git", "checkout", "main"])
    mock_check_call.assert_any_call(["git", "pull", "--no-edit"])


@patch("bb.utils.cmnd.subprocess_run", return_value="file1.txt\nfile2.txt")
def test_checkout_and_pull_modified(mock_subprocess_run):
    with pytest.raises(ValueError, match="modified files"):
        cmnd.checkout_and_pull("main")
