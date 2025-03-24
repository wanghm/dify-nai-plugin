import pytest
from dify_nai_plugin import NAIPluginProvider
from dify_plugin.errors.model import CredentialsValidateFailedError

@pytest.fixture
def provider():
    """Fixture to initialize the NAIPluginProvider."""
    return NAIPluginProvider()

def test_validate_provider_credentials_valid(provider):
    """Test valid provider credentials."""
    valid_credentials = {"api_key": "valid_api_key", "api_url": "https://api.example.com"}
    try:
        provider.validate_provider_credentials(valid_credentials)
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")

def test_validate_provider_credentials_invalid(provider):
    """Test invalid provider credentials."""
    invalid_credentials = {"api_key": "", "api_url": ""}
    with pytest.raises(CredentialsValidateFailedError):
        provider.validate_provider_credentials(invalid_credentials)

def test_invoke_model(provider):
    """Test invoking the model with valid inputs."""
    model = "test-model"
    credentials = {"api_key": "valid_api_key", "api_url": "https://api.example.com"}
    prompt_messages = [{"role": "user", "content": "Hello, world!"}]
    model_parameters = {"temperature": 0.7}

    result = provider._invoke(
        model=model,
        credentials=credentials,
        prompt_messages=prompt_messages,
        model_parameters=model_parameters
    )

    assert result is not None
    assert isinstance(result, dict)  # Assuming the result is a dictionary
    assert "choices" in result  # Assuming the result contains a "choices" key

def test_invoke_model_invalid_credentials(provider):
    """Test invoking the model with invalid credentials."""
    model = "test-model"
    credentials = {"api_key": "", "api_url": ""}
    prompt_messages = [{"role": "user", "content": "Hello, world!"}]
    model_parameters = {"temperature": 0.7}

    with pytest.raises(CredentialsValidateFailedError):
        provider._invoke(
            model=model,
            credentials=credentials,
            prompt_messages=prompt_messages,
            model_parameters=model_parameters
        )