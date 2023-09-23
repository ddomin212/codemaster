import os


def call_poe(
    prompt: str,
    bot: str,
    chat_id: str | None = None,
    chat_code: str | None = None,
) -> tuple[str, str, str]:
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

    if chat_id and chat_code:
        for chunk in client.send_message(
            bot, prompt, chatId=chat_id, chatCode=chat_code
        ):
            pass
        return chunk["response"], chunk["chatCode"], chunk["chatId"]
    else:
        for chunk in client.send_message(bot, prompt):
            pass
        return chunk["text"], chunk["chatCode"], chunk["chatId"]
