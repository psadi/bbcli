# -*- coding: utf-8 -*-

from unittest.mock import patch

import pytest
from typer import Exit

from bb.utils.helper import error_handler, error_tip, validate_config, validate_input


def test_validate_input():
    # Test case 1: Valid input
    assert validate_input("hello", "Enter a string", "Invalid input") == "hello"

    # Test case 2: Invalid input
    with pytest.raises(ValueError, match="Invalid input"):
        validate_input(123, "Enter a string", "Invalid input")

    # Test case 4: None input
    with pytest.raises(ValueError, match="Invalid input"):
        validate_input(None, "Enter a string", "Invalid input")

    # Test case 5: Valid input with different prompt and error message
    assert (
        validate_input("test", "Enter another string", "Different error message")
        == "test"
    )

    # Test case 6: Input with leading and trailing spaces
    assert validate_input(" hello ", "Enter a string", "Invalid input") == " hello "

    # Test case 7: Input with special characters
    assert validate_input("@#$$%", "Enter a string", "Invalid input") == "@#$$%"

    # Test case 8: Numeric string input
    assert validate_input("12345", "Enter a string", "Invalid input") == "12345"

    # Test case 9: Input is a boolean
    with pytest.raises(ValueError, match="Invalid input"):
        validate_input(True, "Enter a string", "Invalid input")

    # Test case 10: Input is a list
    with pytest.raises(ValueError, match="Invalid input"):
        validate_input(["hello"], "Enter a string", "Invalid input")


@patch("bb.utils.helper.request.get")
@patch("bb.utils.helper.richprint.console.print")
def test_validate_config_success(mock_print, mock_get):
    mock_get.return_value = [200, "OK"]
    validate_config()
    mock_print.assert_called_once_with("OK", style="bold green")


@patch("bb.utils.helper.request.get")
def test_validate_config_error(mock_get):
    mock_get.side_effect = Exception("API error")
    with pytest.raises(ValueError, match="API error"):
        validate_config()


@patch("bb.utils.helper.prompt")
def test_validate_input_with_prompt(mock_prompt):
    mock_prompt.return_value = "user input"
    assert (
        validate_input("", "Enter a string", "Invalid input", default="")
        == "user input"
    )
    mock_prompt.assert_called_once_with(
        "? Enter a string", default="", show_default=False
    )


@patch("bb.utils.helper.prompt")
def test_validate_input_optional(mock_prompt):
    assert (
        validate_input(
            "", "Enter a string", "Invalid input", default="def", optional=True
        )
        == "def"
    )
    mock_prompt.assert_not_called()


@patch("bb.utils.constants.common_vars.state", {"verbose": False})
@patch("bb.utils.helper.richprint.console.print")
@patch("bb.utils.helper.error_tip")
def test_error_handler_value_error(mock_error_tip, mock_print):
    @error_handler
    def my_func():
        raise ValueError("my value error")

    with pytest.raises(Exit) as exc_info:
        my_func()

    assert exc_info.value.exit_code == 1
    mock_print.assert_called_once_with("my value error", style="bold red")
    mock_error_tip.assert_called_once()


@patch("bb.utils.constants.common_vars.state", {"verbose": False})
@patch("bb.utils.helper.richprint.console.print")
@patch("bb.utils.helper.error_tip")
def test_error_handler_exception_non_verbose(mock_error_tip, mock_print):
    @error_handler
    def my_func():
        raise Exception("my generic error")

    with pytest.raises(Exit) as exc_info:
        my_func()

    assert exc_info.value.exit_code == 1
    mock_print.assert_called_once_with("my generic error", style="bold red")
    mock_error_tip.assert_called_once()


@patch("bb.utils.constants.common_vars.state", {"verbose": True})
@patch("bb.utils.helper.richprint.console.print")
@patch("bb.utils.helper.richprint.traceback_to_console")
def test_error_handler_value_error_verbose(mock_traceback, mock_print):
    @error_handler
    def my_func():
        raise ValueError("my value error")

    with pytest.raises(Exit) as exc_info:
        my_func()

    assert exc_info.value.exit_code == 1
    mock_print.assert_called_once_with("my value error", style="bold red")
    mock_traceback.assert_called_once()


def test_error_handler_success():
    @error_handler
    def my_func():
        return "success"

    result = my_func()
    assert result == "success"


@patch("bb.utils.constants.common_vars.state", {"verbose": True})
@patch("bb.utils.helper.richprint.console.print")
@patch("bb.utils.helper.richprint.traceback_to_console")
def test_error_handler_verbose(mock_traceback, mock_print):
    @error_handler
    def my_func():
        raise Exception("my generic error")

    with pytest.raises(Exit) as exc_info:
        my_func()

    assert exc_info.value.exit_code == 1
    mock_print.assert_called_once_with("my generic error", style="bold red")
    mock_traceback.assert_called_once()


@patch("bb.utils.helper.richprint.console.print")
def test_error_tip(mock_print):
    error_tip()
    mock_print.assert_called_once()
