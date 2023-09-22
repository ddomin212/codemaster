""" This module contains functions for generating ideas for youtube videos. """
from dotenv import load_dotenv

from utils.llms import call_poe


def rate_code(code, bot):
    text = f"""
    Ignore all previous instructions.
    You are an expert on writing clean and readable code in Python. You are asked to rate the following code on a scale of 1 to 10, with 1 being the worst and 10 being the best.
    You are harsh in your ratings, and you do not give out 10s easily, because you know that there is always room for improvement, that is why you focus mostly on reccomendations and not praise.
    In your rating you shoud consider guidelines such as PEP8, PEP20, and PEP257, along with principles such as DRY, KISS, YAGNI and SOLID.
    You also consider other aspects of the code outside of the principles, such as coupling, cohesion, and the single responsibility principle.
    You also provide an explanation of your rating, along with a recommendation for how the code could be improved in all the areas you considered.

    
    PYTHON CODE:
    ====================
    {code}
    """

    response = call_poe(text, bot)

    return response
