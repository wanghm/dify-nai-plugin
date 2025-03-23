import pytest
from dify_nai_plugin import DifyNaiPluginModelProvider
from dify_plugin.errors.model import CredentialsValidateFailedError

@pytest.fixture
def provider():
    return DifyNaiPluginModelProvider()

def test_validate_provider_credentials_valid(provider):
    # 正しい認証情報を渡した場合のテスト
    valid_credentials = {"api_key": "valid_api_key"}
    try:
        provider.validate_provider_credentials(valid_credentials)
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")

def test_validate_provider_credentials_invalid(provider):
    # 無効な認証情報を渡した場合のテスト
    invalid_credentials = {"api_key": ""}
    with pytest.raises(CredentialsValidateFailedError):
        provider.validate_provider_credentials(invalid_credentials)

def test_invoke_model(provider):
    # モデル呼び出しのテスト
    model = "test-model"
    credentials = {"api_key": "valid_api_key"}
    prompt_messages = [{"role": "user", "content": "Hello, world!"}]
    model_parameters = {"temperature": 0.7}

    result = provider._invoke(
        model=model,
        credentials=credentials,
        prompt_messages=prompt_messages,
        model_parameters=model_parameters
    )

    assert result is not None
    # 必要に応じて、結果の詳細を検証