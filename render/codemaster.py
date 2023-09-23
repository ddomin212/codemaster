import streamlit as st

from utils.rate_code import rate_code

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
        bot = st.selectbox(
            "Bot - [docs](https://github.com/snowby666/poe-api-wrapper#available-default-bots):",
            list(BOTS.keys()),
        )
    with c2:
        module = st.selectbox(
            "Module:",
            list(module_code_map.keys()),
        )

    return module, bot


def render_response(module: str, module_code_map: dict[str, str], bot: str):
    """Render response from bot on page

    Arguments:
        module {str} -- module name
        module_code_map {dict} -- dict with module names as keys and code contents as values
        bot {str} -- bot name
    """
    code = module_code_map[module]

    try:
        if not hasattr(st.session_state, "chat"):
            response, chat_id, chat_code = rate_code(code, BOTS[bot])
            st.session_state.chat = [chat_id, chat_code]
        else:
            response, chat_id, chat_code = rate_code(
                code,
                BOTS[bot],
                st.session_state.chat[0],
                st.session_state.chat[1],
            )
        st.markdown(response)
    except RuntimeError as e:
        st.error(body="Error: " + str(e), icon="🔥")


def codemaster(module_code_map: dict[str, str]):
    """Show codemaster page

    Arguments:
        module_code_map {dict} -- dict with module names as keys and code contents as values
    """
    module, bot = select_params(module_code_map)
    render_response(module, module_code_map, bot)
