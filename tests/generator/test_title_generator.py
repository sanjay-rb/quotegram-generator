# tests/generator/test_generate_title.py

import re
import pytest
from generator.text_generator import generate_title


@pytest.fixture
def sample_quote_data():
    return {"q": "Be yourself; everyone else is already taken.", "a": "Oscar Wilde"}


def test_generate_title_with_marker_success(mocker, sample_quote_data):
    """
    Test that generate_title returns the expected content when API succeeds.
    """
    # Aggrange: Mock load_dotenv, OpenAI client, and completion response
    # Mock load_dotenv so it doesn't read .env
    mocker.patch("generator.title_generator.load_dotenv")

    # Create a fake completion response
    mock_completion = mocker.Mock()
    mock_completion.choices = [
        mocker.Mock(message=mocker.Mock(content="---Awesome YouTube Title---"))
    ]

    # Mock the OpenAI client and its chat.completions.create method
    mock_client = mocker.Mock()
    mock_client.chat.completions.create.return_value = mock_completion
    mocker.patch("generator.title_generator.OpenAI", return_value=mock_client)

    # Act: Call the function under test
    title = generate_title(sample_quote_data)

    # Assert: Check that the title is extracted correctly and meets criteria
    assert isinstance(title, str)
    assert title == "Awesome YouTube Title"
    assert len(title) <= 100


def test_generate_title_without_markers(mocker, sample_quote_data):
    """
    Test that function returns full content if --- markers are missing.
    """
    mocker.patch("generator.title_generator.load_dotenv")

    # Mock completion without --- markers
    mock_completion = mocker.Mock()
    mock_completion.choices = [
        mocker.Mock(message=mocker.Mock(content="Just a title without markers"))
    ]

    mock_client = mocker.Mock()
    mock_client.chat.completions.create.return_value = mock_completion
    mocker.patch("generator.title_generator.OpenAI", return_value=mock_client)

    title = generate_title(sample_quote_data)

    assert title == "Just a title without markers"


def test_generate_title_api_error(mocker, sample_quote_data):
    """
    Test that function returns None if the OpenAI client raises an exception.
    """
    mocker.patch("generator.title_generator.load_dotenv")

    # Simulate API raising an exception
    mock_client = mocker.Mock()
    mock_client.chat.completions.create.side_effect = Exception("API Error")
    mocker.patch("generator.title_generator.OpenAI", return_value=mock_client)

    title = generate_title(sample_quote_data)

    assert title is None
