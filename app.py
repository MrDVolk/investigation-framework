from src.conversation_manager import ConversationManager
import chainlit as cl

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set('manager', ConversationManager(config={'actors':{'Assistant': {}}}))


@cl.on_message
async def on_message(message: cl.Message):
    manager = cl.user_session.get('manager')
    answers = await manager.run(message.content)
    for author, answer in answers.items():
        answer_message = cl.Message(
            author=author,
            content=answer
        )
        await answer_message.send()
