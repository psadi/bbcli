# -*- coding: utf-8 -*-

from unittest.mock import patch

from typer.testing import CliRunner

from bb.auth import _auth

runner = CliRunner()


@patch("bb.auth.typer.prompt")
@patch("bb.auth.is_config_present", return_value=False)
@patch("bb.auth.auth_setup")
def test_setup(mock_auth_setup, mock_is_config_present, mock_prompt):
    mock_prompt.side_effect = ["host", "username", "token"]
    result = runner.invoke(_auth, ["setup"])
    assert result.exit_code == 0
    mock_auth_setup.assert_called_once_with("host", "username", "token")

    result = runner.invoke(_auth, ["setup", "--token"])
    assert result.exit_code != 0


@patch("bb.auth.is_config_present", return_value=True)
@patch("bb.auth.parse", return_value=("user", "token", "host"))
def test_status(mock_parse, mock_is_config):
    result = runner.invoke(_auth, ["status"])
    assert result.exit_code == 0
    result = runner.invoke(_auth, ["status", "--token"])
    assert result.exit_code == 0


@patch("bb.auth.validate_config")
@patch("bb.auth.is_config_present", return_value=True)
def test_test(mock_is_config, mock_validate):
    result = runner.invoke(_auth, ["test"])
    assert result.exit_code == 0
    mock_validate.assert_called_once()

    result = runner.invoke(_auth, ["test", "--token"])
    assert result.exit_code != 0


@patch("bb.auth.is_config_present", return_value=True)
@patch("os.path.exists", return_value=True)
@patch("os.remove")
@patch("os.rmdir")
@patch("bb.auth.typer.prompt", return_value="y")
def test_reset(mock_prompt, mock_rmdir, mock_remove, mock_exists, mock_is_config):
    result = runner.invoke(_auth, ["reset"])
    assert result.exit_code == 0
    mock_remove.assert_called_once()
    mock_rmdir.assert_called_once()

    result = runner.invoke(_auth, ["reset", "--token"])
    assert result.exit_code != 0


def test_invalid_setup():
    result = runner.invoke(_auth, ["setup", "--token"])
    assert result.exit_code != 0


def test_invalid_test():
    result = runner.invoke(_auth, ["test", "--token"])
    assert result.exit_code != 0


def test_invalid_reset():
    result = runner.invoke(_auth, ["reset", "--token"])
    assert result.exit_code != 0
