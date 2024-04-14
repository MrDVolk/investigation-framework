import semantic_kernel as sk
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import (
    OpenAIChatPromptExecutionSettings,
)


class Actor:
    def __init__(self, config: dict) -> None:
        self.kernel = sk.Kernel()
        self.settings = self._setup()
        self.history = ChatHistory()

    async def generate_answer(self, message: str) -> str:
        service = self.kernel.get_service('service')
        self.history.add_user_message(message)
        answer = await service.complete_chat(
            chat_history=self.history,
            settings=self.settings
        )
        answer = [
            message for message in answer
            if message.role == 'assistant'
        ][0].content
        self.history.add_assistant_message(answer)
        return answer

    def _setup(self):
        api_key, _ = sk.openai_settings_from_dot_env()
        settings = OpenAIChatPromptExecutionSettings(
            service_id="service",
            max_tokens=2000,
        )
        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id='service', 
                ai_model_id='gpt-3.5-turbo', 
                api_key=api_key
            )
        )
        return settings
