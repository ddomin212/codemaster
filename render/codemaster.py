import streamlit as st

from utils.rate_code import rate_code

from .other import exception_handler

BOTS = {
    "Assistant": "capybara",
    "Claude": "a2",
    "ChatGPT": "chinchilla",
    "Google-PaLM": "acouchy",
    "Llama2-small": "llama_2_7b_chat",
    "Llama2-medium": "llama_2_13b_chat",
    "Llama2-large": "llama_2_70b_chat",
    "CodeLlama-small": "code_llama_7b_instruct",
    "CodeLlama-medium": "code_llama_13b_instruct",
    "CodeLlama-large": "code_llama_34b_instruct",
    "Solar": "upstage_solar_0_70b_16bit",
    "PythonMaster": "PythonMind",
}


def select_params(module_code_map: dict[str, str]) -> tuple[str, str]:
    """Select module (code file) and bot

    Arguments:
        module_code_map {dict} -- dict with module names as keys and code contents as values
    """
    c1, c2 = st.columns(2)

    with c1:
        if st.session_state.provider == "poe.com":
            bot = st.selectbox(
                "Bot - [docs](https://github.com/snowby666/poe-api-wrapper#available-default-bots):",
                list(BOTS.keys()),
            )
        else:
            st.markdown("You cannot select a bot when using the Bard API.")
    with c2:
        module = st.selectbox(
            "Module:",
            list(module_code_map.keys()),
        )

    submit = st.button("Generate")

    return module, bot, submit


@exception_handler
def render_response(module: str, module_code_map: dict[str, str], bot: str):
    """Render response from bot on page

    Arguments:
        module {str} -- module name
        module_code_map {dict} -- dict with module names as keys and code contents as values
        bot {str} -- bot name
    """
    code = module_code_map[module]
    response_container = st.empty()
    st.session_state.response_container = response_container

    if not hasattr(st.session_state, "chat_id"):
        response, chat_id = rate_code(code, BOTS[bot])
        st.session_state.chat_id = chat_id
    else:
        response, chat_id = rate_code(
            code,
            BOTS[bot],
            st.session_state.chat_id
        )
    
    # st.markdown(response)


def select_provider():
    """Select provider (bot)"""
    provider = st.selectbox(
        "Provider:",
        ["poe.com", "Bard"]
    )
    st.session_state.provider = provider
    if provider == "poe.com":
        st.session_state.POE_API_KEY = st.text_input("Your poe API Key:")
        if st.session_state.POE_API_KEY:
            return True
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.session_state._1PSID = st.text_input("Your Bart _1PSID Cookie:")
        with c2:
            st.session_state._1PSIDTS = st.text_input("Your Bart _1PSIDTS Cookie:")
        with c3:
            st.session_state._1PSIDCC = st.text_input("Your Bart _1PSIDCC Cookie:")
        if st.session_state._1PSID and st.session_state._1PSIDTS and st.session_state._1PSIDCC:
            return True

@exception_handler
def codemaster(module_code_map: dict[str, str]):
    """Show codemaster page

    Arguments:
        module_code_map {dict} -- dict with module names as keys and code contents as values
    """
    if select_provider():
        module, bot, submit = select_params(module_code_map)
        if submit:
            render_response(module, module_code_map, bot)
