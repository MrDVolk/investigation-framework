import os
import semantic_kernel as sk
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import (
    OpenAIChatPromptExecutionSettings,
)

class Actor:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.config.setdefault('purpose', 'You are a helpful assistant')

        self.kernel = sk.Kernel()
        api_key, _ = sk.openai_settings_from_dot_env()
        self.settings = OpenAIChatPromptExecutionSettings(
            service_id="oai_chat",
            max_tokens=150,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.5,
        )

        self.kernel.add_service(
            OpenAIChatCompletion(service_id='oai_chat_gpt', ai_model_id='gpt-3.5-turbo', api_key=api_key)
        )


    async def generate_answer(self, question: str, history: ChatHistory) -> str:
        kernel: sk.Kernel = self.kernel
        completion_service: OpenAIChatCompletion = kernel.get_service('oai_chat_gpt')
        history.add_system_message(self.config['purpose'])
        completion = await completion_service.complete_chat(chat_history=history, settings=self.settings)
        history.remove_message(-1)
        return completion[0].content
