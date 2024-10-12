# -*- coding: utf-8 -*-

############################################################################
# Bitbucket CLI (bb): Work seamlessly with Bitbucket from the command line
#
# Copyright (C) 2022  P S, Adithya (psadi) (ps.adithya@icloud.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

from unittest.mock import patch

from typer.testing import CliRunner

from bb.auth import _auth, setup

runner = CliRunner()


@patch("bb.auth.typer.prompt")
@patch("bb.auth.is_config_present")
@patch("bb.auth.auth_setup")
def test_mock_setup(mock_auth_setup, mock_is_config_present, mock_prompt):
    # Arrange
    mock_is_config_present.return_value = False
    mock_prompt.side_effect = ["host", "username", "token"]

    # Act
    setup()

    # Assert
    mock_is_config_present.assert_called_once()
    mock_prompt.assert_any_call("> bitbucket_host")
    mock_prompt.assert_any_call("> username")
    mock_prompt.assert_any_call("> token", hide_input=True)
    mock_auth_setup.assert_called_once_with("host", "username", "token")


def test_invalid_setup():
    result = runner.invoke(_auth, ["setup", "--token"])
    assert result.exit_code != 0


def test_invalid_test():
    result = runner.invoke(_auth, ["test", "--token"])
    assert result.exit_code != 0


def test_invalid_reset():
    result = runner.invoke(_auth, ["reset", "--token"])
    assert result.exit_code != 0


def test_setup():
    result = runner.invoke(_auth, ["setup"])
    assert result.exit_code == 0
    result = runner.invoke(_auth, ["setup", "--token"])
    assert result.exit_code != 0


def test_status():
    result = runner.invoke(_auth, ["status"])
    assert result.exit_code == 0
    result = runner.invoke(_auth, ["status", "--token"])
    assert result.exit_code == 0


def test_test():
    result = runner.invoke(_auth, ["test"])
    assert result.exit_code == 0
    result = runner.invoke(_auth, ["test", "--token"])
    assert result.exit_code != 0


def test_reset():
    result = runner.invoke(_auth, ["reset"])
    assert result.exit_code == 0
    result = runner.invoke(_auth, ["reset", "--token"])
    assert result.exit_code != 0
