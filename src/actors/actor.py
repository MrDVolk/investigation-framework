from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.memory import ChatMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

class Actor:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.config.setdefault("purpose", "You are a helpful assistant")

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.config["purpose"]),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )
        model = ChatOpenAI(model_name="gpt-3.5-turbo-0125")
        self.runnable = prompt | model | StrOutputParser()

    def generate_answer(self, question: str, history: ChatMessageHistory) -> str:
        return self.runnable.invoke({
            "question": question,
            "chat_history": history,
        })
