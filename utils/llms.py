import os


def call_poe(prompt, bot):
    """Call poe api to generate text

    Arguments:
        prompt {str} -- prompt to send to bot
        bot {str} -- bot name

    Returns:
        str -- generated text
    """
    from poe_api_wrapper import PoeApi

    token = os.getenv("POE_API_TOKEN")
    client = PoeApi(token)

    for chunk in client.send_message(bot, prompt):
        pass

    return chunk["text"]
