# -*- coding: utf-8 -*-
from unittest.mock import patch

from props import Ini

from bb.auth import setup


@patch("bb.auth.typer.prompt")
@patch("bb.auth.typer.echo")
@patch("bb.auth.console.print")
@patch("bb.auth.is_config_present")
@patch("bb.auth.auth_setup")
def test_setup(
    mock_auth_setup, mock_is_config_present, mock_print, mock_echo, mock_prompt
):
    property: Ini = Ini()
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
    mock_echo.assert_called_once_with(
        f"Configuration written at '{property.BB_CONFIG_FILE}',"
        + "Please re-run 'bb auth test' to validate"
    )
