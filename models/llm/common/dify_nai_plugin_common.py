import logging
from collections.abc import Generator
from typing import Optional, Union
import requests

from dify_plugin import LargeLanguageModel
from dify_plugin.entities import I18nObject
from dify_plugin.errors.model import (
    CredentialsValidateFailedError,
)
from dify_plugin.entities.model import (
    AIModelEntity,
    FetchFrom,
    ModelType,
)
from dify_plugin.entities.model.llm import (
    LLMResult,
)
from dify_plugin.entities.model.message import (
    PromptMessage,
    PromptMessageTool,
)

from core.model_runtime.errors.invoke import (
    InvokeError,
    InvokeServerUnavailableError,
    InvokeRateLimitError,
    InvokeAuthorizationError,
    InvokeBadRequestError
)

logger = logging.getLogger(__name__)

class DifyNaiPluginLargeLanguageModel(LargeLanguageModel):
    """
    Model class for dify-nai-plugin large language model.
    """

    def _invoke(
        self,
        model: str,
        credentials: dict,
        prompt_messages: list[PromptMessage],
        model_parameters: dict,
        tools: Optional[list[PromptMessageTool]] = None,
        stop: Optional[list[str]] = None,
        stream: bool = True,
        user: Optional[str] = None,
    ) -> Union[LLMResult, Generator]:
        """
        Invoke large language model

        :param model: model name
        :param credentials: model credentials
        :param prompt_messages: prompt messages
        :param model_parameters: model parameters
        :param tools: tools for tool calling
        :param stop: stop words
        :param stream: is stream response
        :param user: unique user id
        :return: full response or stream response chunk generator result
        """
        # エンドポイントの処理
        api_endpoint = credentials.get('api_endpoint', '').rstrip('/')
        if not api_endpoint:
            raise ValueError("API Endpoint is required")
    
        headers = {
            "Authorization": f"Bearer {credentials['api_key']}",
            "Content-Type": "application/json"
        }
        #data = {
        #    "model": model,
        #    "messages": [message.to_dict() for message in prompt_messages],
        #    "parameters": model_parameters,
        #    "tools": [tool.to_dict() for tool in tools] if tools else None,
        #    "stop": stop,
        #    "stream": stream,
        #    "user": user
        #}
        #response = requests.post(f"{credentials['api_url']}/v1/chat/completions", headers=headers, json=data)
        #response.raise_for_status()
        #result = response.json()
        #return LLMResult(choices=result["choices"])
        data = {
            "model": model,
            "messages": [message.to_dict() for message in prompt_messages],
            "stream": stream,
        }

        # オプションパラメータの追加
        if model_parameters:
            data.update(model_parameters)
        
        if tools:
            data["tools"] = [tool.to_dict() for tool in tools]
        
        if stop:
            data["stop"] = stop
        
        if user:
            data["user"] = user

        # API Call
        try:
            response = requests.post(
                f"{api_endpoint}/v1/chat/completions", 
                headers=headers, 
                json=data,
                stream=stream
            )
            response.raise_for_status()
        
            # Process Responses
            if stream:
                return self._process_stream_response(response)
            else:
                result = response.json()
                return LLMResult(choices=result.get("choices", []))
        
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise CredentialsValidateFailedError(f"API request failed: {e}")

    def _process_stream_response(self, response):
        """
        Process Stream response
        """
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                # Process Chunk
                yield chunk

    def get_num_tokens(
        self,
        model: str,
        credentials: dict,
        prompt_messages: list[PromptMessage],
        tools: Optional[list[PromptMessageTool]] = None,
    ) -> int:
        """
        Get number of tokens for given prompt messages

        :param model: model name
        :param credentials: model credentials
        :param prompt_messages: prompt messages
        :param tools: tools for tool calling
        :return:
        """
        return 0

    def validate_credentials(self, model: str, credentials: dict) -> None:
        """
        Validate model credentials

        :param model: model name
        :param credentials: model credentials
        :return:
        """
        try:
            pass
        except Exception as ex:
            raise CredentialsValidateFailedError(str(ex))

    def get_customizable_model_schema(self, model: str, credentials: dict) -> AIModelEntity:
        """
        If your model supports fine-tuning, this method returns the schema of the base model
        but renamed to the fine-tuned model name.

        :param model: model name
        :param credentials: credentials

        :return: model schema
        """
        entity = AIModelEntity(
            model=model,
            label=I18nObject(zh_Hans=model, en_US=model),
            model_type=ModelType.LLM,
            features=[],
            fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
            model_properties={},
            parameter_rules=[],
        )

        return entity

@property
def _invoke_error_mapping(self) -> dict[type[InvokeError], list[type[Exception]]]:
    """
    Map model invoke error to unified error
    The key is the error type thrown to the caller
    The value is the error type thrown by the model,
    which needs to be converted into a unified error type for the caller.

    :return: Invoke error mapping
    """
    return {
        InvokeConnectionError: [ConnectionError],
        InvokeServerUnavailableError: [ServerUnavailableError],
        InvokeRateLimitError: [RateLimitError],
        InvokeAuthorizationError: [AuthorizationError],
        InvokeBadRequestError: [BadRequestError]
    }