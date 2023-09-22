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


def codemaster(module_code_map):
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

    code = module_code_map[module]

    try:
        st.markdown(rate_code(code, BOTS[bot]))
    except RuntimeError as e:
        st.error(body="Error: " + str(e), icon="🔥")
