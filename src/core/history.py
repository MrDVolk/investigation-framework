from dataclasses import dataclass, field
from uuid import uuid4
from time import time


@dataclass
class Message:
    sender: str
    content: str
    id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: int = field(default_factory=lambda: int(time()))
    is_thought: bool = field(default=False)
    is_prompt: bool = field(default=False)

    def to_dict(self, agent_name: str) -> dict[str, str]:
        normalized_sender = self.sender.lower()
        agent_name = agent_name.lower()

        if normalized_sender == agent_name:
            role = 'assistant'
            content = self.content
            if self.is_prompt:
                role = 'system'
        elif normalized_sender == 'system':
            role = normalized_sender
            content = self.content
        else:
            role = 'user'
            content = f'[{self.sender}]: {self.content}'

        if self.is_thought:
            content = f'[Internal thinking]: {content}'

        return {
            'role': role,
            'content': content
        }
    
    def belongs_to(self, agent_name: str) -> bool:
        return self.sender.lower() == agent_name.lower()
    
    @staticmethod
    def from_request(request: str) -> 'Message':
        return Message('user', request)


@dataclass
class History:
    history: list[Message] = field(default_factory=list)

    def add(self, sender: str, content: str) -> Message:
        message = Message(sender, content)
        self.history.append(message)
        self.history.sort(key=lambda x: x.timestamp)
        return message

    def to_list(self, agent_name: str) -> list[dict[str, str]]:
        return [
            message.to_dict(agent_name) 
            for message in self.history
            if (not message.is_thought and not message.is_prompt) or message.belongs_to(agent_name)
        ]
