import os
import streamlit as st
from dotenv import load_dotenv

def call_poe(
    prompt: str,
    bot: str,
    chat_id: str | None = None,
) -> tuple[str, str, str]:
    """Call poe api to generate text

    Arguments:
        prompt {str} -- prompt to send to bot
        bot {str} -- bot name

    Returns:
        str -- generated text
    """
    from poe_api_wrapper import PoeApi
    load_dotenv()

    token = os.getenv("POE_API_TOKEN")
    client = PoeApi(token)

    bot_response = ""

    if chat_id:
        for chunk in client.send_message(
            bot, prompt, chatId=chat_id
        ):
            bot_response += chunk["response"]
            st.session_state.response_container.markdown(bot_response)
        return bot_response, chunk["chatId"]
    else:
        for chunk in client.send_message(bot, prompt):
            bot_response += chunk["response"]
            st.session_state.response_container.markdown(bot_response)
        return chunk["text"], chunk["chatId"]


def call_local_llama(prompt: str) -> str:
    from langchain.llms import CTransformers

    llm = CTransformers(
        model="/home/dan/Documents/codemaster/llama-2-7b-chat.ggmlv3.q4_0.bin",
        model_type="llama",
        config={"max_new_tokens": 128, "temperature": 0.9},
    )

    text = llm.predict(prompt)
    print(text)
    return text
