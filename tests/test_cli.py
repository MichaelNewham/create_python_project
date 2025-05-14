"""
Tests for the cli module.
"""

from unittest.mock import patch

from create_python_project.utils.cli import confirm, enhanced_input, select_from_list


class TestEnhancedInput:
    """Tests for the enhanced_input function."""

    @patch("builtins.input", return_value="test input")
    def test_enhanced_input_simple(self, mock_input) -> None:
        """Test enhanced input with simple prompt."""
        # Execute
        result = enhanced_input("Enter value: ")

        # Assert
        assert result == "test input", "Input value is incorrect"
        mock_input.assert_called_once_with("Enter value: ")

    @patch("builtins.input", return_value="")
    def test_enhanced_input_with_default(self, mock_input) -> None:
        """Test enhanced input with default value."""
        # Execute
        result = enhanced_input("Enter value: ", default="default value")

        # Assert
        assert result == "default value", "Default value was not used"
        mock_input.assert_called_once_with("Enter value:  [default value]: ")

    @patch("builtins.input", return_value="custom value")
    def test_enhanced_input_override_default(self, mock_input) -> None:
        """Test enhanced input overriding default value."""
        # Execute
        result = enhanced_input("Enter value: ", default="default value")

        # Assert
        assert result == "custom value", "Custom value was not used"
        mock_input.assert_called_once_with("Enter value:  [default value]: ")


class TestSelectFromList:
    """Tests for the select_from_list function."""

    @patch("builtins.input", return_value="1")
    def test_select_from_list_valid(self, mock_input) -> None:
        """Test selecting a valid item from a list."""
        # Setup
        items = ["Item 1", "Item 2", "Item 3"]

        # Execute
        success, result = select_from_list(items, "Select an item: ")

        # Assert
        assert success, "Selection was not successful"
        assert result == "Item 1", "Selected item is incorrect"

    @patch("builtins.input", return_value="custom")
    def test_select_from_list_custom(self, mock_input) -> None:
        """Test selecting a custom item not in the list."""
        # Setup
        items = ["Item 1", "Item 2", "Item 3"]

        # Execute
        success, result = select_from_list(items, "Select an item: ", allow_custom=True)

        # Assert
        assert success, "Selection was not successful"
        assert result == "custom", "Custom value was not used"


class TestConfirm:
    """Tests for the confirm function."""

    @patch("builtins.input", return_value="y")
    def test_confirm_yes(self, mock_input) -> None:
        """Test confirmation with 'y' input."""
        # Execute
        result = confirm("Confirm? ")

        # Assert
        assert result is True, "Confirmation should be True"

    @patch("builtins.input", return_value="n")
    def test_confirm_no(self, mock_input) -> None:
        """Test confirmation with 'n' input."""
        # Execute
        result = confirm("Confirm? ")

        # Assert
        assert result is False, "Confirmation should be False"

    @patch("builtins.input", return_value="")
    def test_confirm_default_true(self, mock_input) -> None:
        """Test confirmation with default=True."""
        # Execute
        result = confirm("Confirm? ", default=True)

        # Assert
        assert result is True, "Default confirmation should be True"

    @patch("builtins.input", return_value="")
    def test_confirm_default_false(self, mock_input) -> None:
        """Test confirmation with default=False."""
        # Execute
        result = confirm("Confirm? ", default=False)

        # Assert
        assert result is False, "Default confirmation should be False"
        # Assert
        assert result is False, "Default confirmation should be False"
