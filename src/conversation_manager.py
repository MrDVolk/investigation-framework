from src.actors.base_actor import Actor


class ConversationManager:
    def __init__(self, config) -> None:
        self.actors = {}
        for actor_name, actor_config in config['actors'].items():
            self.actors[actor_name] = Actor(actor_config)

    async def run(self, message: str):
        answers = {}
        for actor_name, actor in self.actors.items():
            answer = await actor.generate_answer(message)
            answers[actor_name] = answer
        return answers