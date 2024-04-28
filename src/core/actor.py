from dataclasses import dataclass
from src.core.client import Client
from src.core.history import History, Message
from typing import Generator
import json


@dataclass
class Persona:
    name: str
    character: str
    thinking_style: str

    @staticmethod
    def from_json(persona_json: dict) -> 'Persona':
        return Persona(
            persona_json['name'],
            persona_json['character'],
            persona_json['thinking_style']
        )


class Actor:
    def __init__(self, persona: Persona, client: Client, prompts: dict[str, str]):
        self.persona = persona
        self.client = client
        self.prompts = prompts

    def register(self, history: History):
        persona_introduction = f'{self.persona.character}\n{self.persona.thinking_style}'
        character_intro = history.add(
            self.persona.name,
            persona_introduction
        )
        character_intro.is_prompt = True

    def run(self, history: History) -> Generator[str, None, None]:
        history_list = history.to_list(self.persona.name)
        self.log_to_console(history_list)
        return self.client.run_stream(history_list)

    def invoke_thinking_process(self, history: History):
        history_list = history.to_list(self.persona.name)
        planning_prompt = self.prompts['plan'].format(
            thinking_style=self.persona.thinking_style,
        )
        planning_message = Message.from_request(planning_prompt).to_dict(self.persona.name)
        history_list.append(planning_message)

        created_plan = self.client.run_sync(history_list)

        planning_result = history.add(
            self.persona.name,
            created_plan
        )
        planning_result.is_thought = True

        acting_prompt = self.prompts['act'].format(
            thinking_style=self.persona.thinking_style,
            name=self.persona.name,
        )
        acting_message = Message.from_request(acting_prompt).to_dict(self.persona.name)
        history_list.append(acting_message)

        response = self.client.run_sync(history_list)
        history.add(self.persona.name, response)
        return response

    def log_to_console(self, history_list: list[dict[str, str]]):
        print(f'Running actor {self.persona.name}')
        printable_history = json.dumps(history_list, indent=4)
        print(printable_history)
        print('---')
        print()
        print()

