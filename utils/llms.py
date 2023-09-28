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

    token = st.session_state.POE_API_KEY
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
    
def call_bard(prompt: str):
    from bardapi import BardCookies

    cookie_dict = {
        "__Secure-1PSID": st.session_state._1PSID,
        "__Secure-1PSIDTS": st.session_state._1PSIDTS,
        "__Secure-1PSIDCC": st.session_state._1PSIDCC,
        # Any cookie values you want to pass session object.
    }

    bard = BardCookies(cookie_dict=cookie_dict)
    response = bard.get_answer(prompt)
    print(response.keys())
    st.session_state.response_container.markdown(response['content'])

        