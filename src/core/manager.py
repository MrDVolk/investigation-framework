from src.core.history import History
from src.core.client import Client
from src.core.actor import Actor, Persona
from dataclasses import dataclass, field
from typing import Generator
import time


@dataclass
class GenerationToken:
    author: str
    content: str = field(default='')
    is_start: bool = field(default=False)
    is_final: bool = field(default=False)


class Manager:
    def __init__(self, config: dict, prompts: dict[str, str], personas: dict[str, dict]):
        self.prompts = prompts
        self.config = config
        self.actors = [
            Actor(
                persona=Persona.from_json(personas[name]),
                client=Client(config['models'], model),
                prompts=prompts
            )
            for name, model in config['personas'].items()
        ]

    def register(self, history: History):
        for actor in self.actors:
            actor.register(history)
        
        history.add('system', self.prompts['brainstorm'])

    def run(self, history: History, actor_names: list[str] = None) -> Generator[GenerationToken, None, None]:
        actors = self.actors if actor_names is None else [
            actor for actor in self.actors if actor.persona.name in actor_names
        ]
        
        for actor in actors:
            yield GenerationToken(author=actor.persona.name, is_start=True)

            # TODO: Implement a better way to handle the delay
            time.sleep(0.125)
            for response in actor.run(history):
                yield GenerationToken(author=actor.persona.name, content=response)
            
            yield GenerationToken(author=actor.persona.name, is_final=True)

    def try_get_actors(self, message: str) -> list[str] | None:
        actor_names = [
            actor.persona.name
            for actor in self.actors
            if f'@{actor.persona.name}' in message
        ]

        if len(actor_names) == 0:
            return None
        
        return actor_names
