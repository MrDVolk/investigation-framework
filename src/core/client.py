import os
from typing import Generator
from openai import OpenAI, Stream
from openai.types.chat import ChatCompletion, ChatCompletionChunk


class Client:
    clients: dict[str, OpenAI] = {}

    def __init__(self, config: dict, model: str):
        self.config = config[model]
        self.model_type = self.config['model_type']
        self.client = Client.clients.get(model, self._create_client())

    def run_sync(self, history: list[dict[str, str]] = None, **kwargs) -> str:
        response: ChatCompletion = self.client.chat.completions.create(
            model=self.model_type,
            messages=history,
            **kwargs
        )
        return response.choices[0].message.content

    def run_stream(self, history: list[dict[str, str]] = None, **kwargs) -> Generator[str, None, None]:
        response: Stream[ChatCompletionChunk] = self.client.chat.completions.create(
            model=self.model_type,
            messages=history,
            stream=True,
            **kwargs
        )
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content

    def _create_client(self) -> OpenAI:
        source = self.config['source']
        match source:
            case 'local':
                return OpenAI(
                    api_key=self.config['api_key'],
                    base_url=self.config['base_url']
                )
            case 'openai':
                return OpenAI(
                    api_key=os.environ['OPENAI_API_KEY']
                )
