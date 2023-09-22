import os

from bardapi import BardCookies


def call_bard(prompt):
    cookie_dict = {
        "__Secure-1PSID": "bAjwms4CcZlNBpmZL_oXP33IIOS2glwn1bkikD4DRYvfHCC6MmM682cbft6I2hzHd126fw.",
        "__Secure-1PSIDTS": "sidts-CjEB3e41hSwABvrfm9lfu-Fs_T5_rBULIANsRQHgAYDB8tcvusJhem6MW4ggOj32mJTxEAA",
        "__Secure-1PSIDCC": "APoG2W8snt4UUCAHLvt7b9_NMpiDjbJ8bGLa2zAc1egGyw4RJv2TX8A6dLT9U7ptP4Esfk7RSa8",
    }

    bard = BardCookies(cookie_dict=cookie_dict)
    return bard.get_answer(prompt)["content"]


def call_poe(prompt, bot):
    from poe_api_wrapper import PoeApi

    token = "o9Pifo9lwZEXDva-h4daOA=="
    client = PoeApi(token)

    for chunk in client.send_message(bot, prompt):
        pass

    return chunk["text"]
