from generator.quote_generator import generate_quote


def test_generate_quote_success(mocker):
    """Test generate_quote returns the API data when the request succeeds."""
    mock_data = [
        {
            "q": "Be yourself.",
            "a": "Oscar Wilde",
            "h": "<blockquote>Be yourself.</blockquote>",
        }
    ]

    # Mock requests.get to return a controlled response
    mock_response = mocker.Mock()
    mock_response.json.return_value = mock_data
    mock_response.raise_for_status.return_value = None
    mocker.patch("generator.quote_generator.requests.get", return_value=mock_response)

    quote = generate_quote()

    assert isinstance(quote, dict)
    assert quote == mock_data[0]
    assert "q" in quote
    assert "a" in quote
    assert "h" in quote


def test_generate_quote_fallback_on_error(mocker):
    """Test generate_quote returns fallback quote when the request fails."""
    # Mock requests.get to raise an exception
    mocker.patch(
        "generator.quote_generator.requests.get", side_effect=Exception("Network error")
    )

    quote = generate_quote()

    assert isinstance(quote, dict)
    assert quote["q"] == "Create each day anew."
    assert quote["a"] == "Morihei Ueshiba"
    assert (
        quote["h"]
        == "<blockquote>&ldquo;Create each day anew.&rdquo; &mdash; <footer>Morihei Ueshiba</footer></blockquote>"
    )
