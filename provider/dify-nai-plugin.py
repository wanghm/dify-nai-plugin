import logging
from collections.abc import Mapping
from typing import Generator, Optional, Union
from dify_plugin import ModelProvider
from dify_plugin.entities.model import ModelType
from dify_plugin.entities.prompt import PromptMessage, PromptMessageTool
from dify_plugin.entities.llm import LLMResult
from dify_plugin.errors.model import CredentialsValidateFailedError

logger = logging.getLogger(__name__)


class DifyNaiProvider(ModelProvider):
    def validate_provider_credentials(self, credentials: Mapping) -> None:
        """
        Validate provider credentials
        if validate failed, raise exception

        :param credentials: provider credentials, credentials form defined in `provider_credential_schema`.
        """
        try:
            pass
        except CredentialsValidateFailedError as ex:
            raise ex
        except Exception as ex:
            logger.exception(
                f"{self.get_provider_schema().provider} credentials validate failed"
            )
            raise ex

    def _invoke(
        self,
        model: str,
        credentials: dict,
        prompt_messages: list[PromptMessage],
        model_parameters: dict,
        tools: Optional[list[PromptMessageTool]] = None,
        stop: Optional[list[str]] = None,
        stream: bool = True,
        user: Optional[str] = None
    ) -> Union[LLMResult, Generator]:
        """
        Invoke the large language model.

        :param model: model name
        :param credentials: model credentials
        :param prompt_messages: prompt messages
        :param model_parameters: model parameters
        :param tools: tools for tool calling
        :param stop: stop words
        :param stream: determines if response is streamed
        :param user: unique user id
        :return: full response or a chunk generator
        """
        # 実装例: ログを出力して、仮の結果を返す
        logger.info(f"Invoking model {model} with parameters {model_parameters}")
        return LLMResult()  # 仮の戻り値

    def _invoke(self, stream: bool, **kwargs) -> Union[LLMResult, Generator]:
        if stream:
            return self._handle_stream_response(**kwargs)
        return self._handle_sync_response(**kwargs)

    def _handle_stream_response(self, **kwargs) -> Generator:
        for chunk in response:
            yield chunk

    def _handle_sync_response(self, **kwargs) -> LLMResult:
        return LLMResult(**response)

    def get_num_tokens(
        self,
        model: str,
        credentials: dict,
        prompt_messages: list[PromptMessage],
        tools: Optional[list[PromptMessageTool]] = None
    ) -> int:
        """
        Get the number of tokens for the given prompt messages.
        """
        return 0

    def validate_credentials(self, model: str, credentials: dict) -> None:
        """
        Validate model credentials.
        """
        pass

    def get_customizable_model_schema(self, model: str, credentials: dict) -> AIModelEntity | None:
        """
            used to define customizable model schema
        """
        rules = [
            ParameterRule(
                name='temperature', type=ParameterType.FLOAT,
                use_template='temperature',
                label=I18nObject(
                    zh_Hans='温度', en_US='Temperature'
                )
            ),
            ParameterRule(
                name='top_p', type=ParameterType.FLOAT,
                use_template='top_p',
                label=I18nObject(
                    zh_Hans='Top P', en_US='Top P'
                )
            ),
            ParameterRule(
                name='max_tokens', type=ParameterType.INT,
                use_template='max_tokens',
                min=1,
                default=512,
                label=I18nObject(
                    zh_Hans='最大生成长度', en_US='Max Tokens'
                )
            )
        ]

        # if model is A, add top_k to rules
        if model == 'A':
            rules.append(
                ParameterRule(
                    name='top_k', type=ParameterType.INT,
                    use_template='top_k',
                    min=1,
                    default=50,
                    label=I18nObject(
                        zh_Hans='Top K', en_US='Top K'
                    )
                )
            )

        """
            some NOT IMPORTANT code here
        """

        entity = AIModelEntity(
            model=model,
            label=I18nObject(
                en_US=model
            ),
            fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
            model_type=model_type,
            model_properties={ 
                ModelPropertyKey.MODE:  ModelType.LLM,
            },
            parameter_rules=rules
        )

        return entity

    @property
    def _invoke_error_mapping(self) -> dict[type[InvokeError], list[type[Exception]]]:
        """
        Map model invocation errors to unified error types.
        The key is the error type thrown to the caller.
        The value is the error type thrown by the model, which needs to be mapped to a
        unified Dify error for consistent handling.
        """
        # return {
        #   InvokeConnectionError: [requests.exceptions.ConnectionError],
        #   ...
        # }
        return {}
