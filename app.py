import chainlit as cl
from src.core.history import History
from src.core.manager import Manager
from src.utils.loader import load_application

configuration = load_application()
manager = Manager(**configuration)


@cl.on_chat_start
async def on_chat_start():
    history = History()
    manager.register(history)
    cl.user_session.set('history', history)


@cl.action_callback(continue_action := 'continue')
async def on_action(action: cl.Action):
    await action.remove()
    await on_message(cl.Message(author='system', content='continue'))


@cl.on_message
async def on_message(message: cl.Message):
    history: History = cl.user_session.get('history')

    request = message.content
    if request != 'continue':
        history.add('user', request)

    actor_names = manager.try_get_actors(request)

    response_message = None
    for generation_token in manager.run(history, actor_names):
        if generation_token.is_start:
            response_message = cl.Message(author=generation_token.author, content='')
            await response_message.send()
        elif generation_token.is_final:
            await response_message.update()
            history.add(response_message.author, response_message.content)
        else:
            await response_message.stream_token(generation_token.content)

    response_message.actions = [cl.Action(name=continue_action, value='continue', description='continue')]
    await response_message.update()
