from langchain.memory import ChatMessageHistory
from src.actors.actor import Actor
import chainlit as cl

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("actor", Actor(config={}))
    cl.user_session.set("history", ChatMessageHistory())


@cl.on_message
async def on_message(message: cl.Message):
    actor = cl.user_session.get("actor")
    history = cl.user_session.get("history")
    question = message.content
    history.add_user_message(question)
    answer = actor.generate_answer(question, history)
    history.add_ai_message(answer)
    msg = cl.Message(content=answer)
    await msg.send()
