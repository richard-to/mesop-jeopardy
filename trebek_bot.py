import json
import os

import google.generativeai as genai


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

answer_check_model = genai.GenerativeModel('gemini-1.5-pro')
question_gen_model = genai.GenerativeModel('gemini-1.5-flash', generation_config={
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 24576,
  "response_mime_type": "application/json",
})


_JEOPARDY_QUESTION_GENERATE_PROMPT = """
You are a Jeopardy! expert who specializes in crafting great questions.

Generate Jeopardy! questions to populate a Jeopardy! game board.

A Jeopardy! board has 6 unique categories each with 5 questions of increasing
difficulty.

IT IS VERY IMPORTANT THAT YOU GENERATE 6 CATEGORIES AND NOT 5 CATEGORIES.

Output in JSON format like this:

[
  {
    "category": "HISTORY",
    "air_date": "2004-12-31",
    "question": "'For the last 8 years of his life, Galileo was...",
    "value": "$200",
    "answer": "Copernicus",
    "round": "Jeopardy!",
    "show_number": "4680"
  }
]
"""

_JEOPARDY_PROMPT = """
You are the host of Jeopardy.

The current answer is {clue}
The correct question response is {question}

I respond with: {response}

Am I correct?

Start with "Yes. That is correct. " if the response is correct.
Or "No. That is incorrect. " if the response is incorrect.

Afterwards, elaborate on why.
"""


def check_answer(clue: str, answer: str, response: str) -> list[bool, str]:
  """Checks if the given answer is correct.

  Args:
    clue: Clue being presented
    answer: The real response to the clue
    response: The user's response to the clue

  Returns:
    bool: Whether the response to the clue was correct
    answer_response: Explanation on why the user's response was right/wrong
  """
  response = answer_check_model.generate_content(_JEOPARDY_PROMPT.format(
    clue=clue, question=answer, response=response)
  ).text

  if response.startswith("Yes. That is correct."):
    return True, response[len("Yes. That is correct."):]
  return False, response[len("No. That is incorrect."):]


def generate_questions() -> list[dict[str, str]]:
  """Generate Jeopardy questions using Gemini.

  Returns:
    Generated jeopardy data set in the expected format.
  """
  return json.loads(
    question_gen_model.generate_content(_JEOPARDY_QUESTION_GENERATE_PROMPT).text
  )
