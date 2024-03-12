import os

import dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain.memory import ChatMessageHistory


def get_completionMessage(chat: ChatGroq, message: HumanMessage):
    pass


if __name__ == '__main__':
    dotenv.load_dotenv()
    chat = ChatGroq(model='mixtral-8x7b-32768', temperature=0.2)
    chat.groq_api_base = os.getenv('GROQ_BASE_URL')
    chat.groq_api_key = os.getenv('GROQ_API_KEY')

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Answer all questions to the best of your ability."
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    chain = prompt | chat
    # print(chain.invoke({
    #     "messages": [
    #         HumanMessage(
    #             content="Translate this sentence from English to French: I love programming."
    #         ),
    #         AIMessage(content="J'adore la programmation."),
    #         HumanMessage(content="What did you just say?"),
    #     ]
    # }))
    #
    history = ChatMessageHistory()
    history.add_user_message("hi!")
    history.add_ai_message("whats up?")
    print(history.messages)

    history.add_user_message("Translate this sentence from English to French: I love programming.")
    response = chain.invoke({"messages": history.messages})
    history.add_ai_message(response)
    history.add_user_message("What did you just say?")

    chain.invoke({"messages": history.messages})
