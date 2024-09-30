import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(__file__) + "/../..")
import pytest

from hulua.agents.model_factory import (
    WrappedChatglm,
    create_model_glm,
    get_base_and_headers_glm,
)

# from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from hulua.agents_services.zhipu import ChatZhipuAI

# from hulua.schema import ModelSettings, UserBase
from hulua.schema.model import ModelSettings
from hulua.settings import Settings


def test_helicone_enabled_without_custom_api_key():
    model_settings = ModelSettings()
    user = UserBase(id="user_id")
    settings = Settings(
        helicone_api_key="some_key",
        helicone_api_base="helicone_base",
        openai_api_base="openai_base",
    )

    base, headers, use_helicone = get_base_and_headers(settings, model_settings, user)

    assert use_helicone is True
    assert base == "helicone_base"
    assert headers == {
        "Helicone-Auth": "Bearer some_key",
        "Helicone-Cache-Enabled": "true",
        "Helicone-User-Id": "user_id",
        "Helicone-OpenAI-Api-Base": "openai_base",
    }


def test_helicone_disabled():
    model_settings = ModelSettings()
    user = UserBase(id="user_id")
    settings = Settings()

    base, headers, use_helicone = get_base_and_headers(settings, model_settings, user)
    assert base == "https://api.openai.com/v1"
    assert headers is None
    assert use_helicone is False


def test_helicone_enabled_with_custom_api_key():
    model_settings = ModelSettings(
        custom_api_key="custom_key",
    )
    user = UserBase(id="user_id")
    settings = Settings(
        openai_api_base="openai_base",
        helicone_api_key="some_key",
        helicone_api_base="helicone_base",
    )

    base, headers, use_helicone = get_base_and_headers(settings, model_settings, user)

    assert base == "https://api.openai.com/v1"
    assert headers is None
    assert use_helicone is False


@pytest.mark.parametrize(
    "streaming, use_azure",
    list(
        itertools.product(
            [True, False],
            [True, False],
        )
    ),
)
def test_create_model(streaming, use_azure):
    # user = UserBase(id="user_id")
    settings = Settings()
    model_settings = ModelSettings(
        temperature=0.7,
        model="glm-4",
        max_tokens=100,
    )

    settings.zhipu_api_base = (
        "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        if not use_azure
        else "https://oai.azure.com"
    )
    settings.zhipu_api_key = "585f2d5ddf103304729767c75ab08094.uStCbbMiva4xxPTJ"
    # settings.openai_api_version = "version"

    result = create_model_glm(settings, model_settings, streaming)
    assert issubclass(result.__class__, WrappedChatglm)
    assert issubclass(result.__class__, ChatZhipuAI)

    # Check if the required keys are set properly
    assert result.zhipuai_api_base == settings.zhipu_api_base
    assert result.zhipuai_api_key == settings.zhipu_api_key
    assert result.temperature == model_settings.temperature
    assert result.max_tokens == model_settings.max_tokens
    assert result.streaming == streaming
    # assert result.max_retries == 5


@pytest.mark.parametrize(
    "model_settings, streaming",
    list(
        itertools.product(
            [
                ModelSettings(
                    customTemperature=0.222,
                    customModelName="gpt-4",
                    maxTokens=1234,
                ),
                ModelSettings(),
            ],
            [True, False],
        )
    ),
)
def test_custom_model_settings(model_settings: ModelSettings, streaming: bool):
    model = create_model(
        Settings(),
        model_settings,
        UserBase(id="", email="test@example.com"),
        streaming=streaming,
    )

    assert model.temperature == model_settings.temperature
    assert model.model_name.startswith(model_settings.model)
    assert model.max_tokens == model_settings.max_tokens
    assert model.streaming == streaming


test_create_model(False, False)
