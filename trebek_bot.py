import os

import google.generativeai as genai


GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


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

def check_answer(clue: str, answer: str, response: str) -> list[bool,str]:
  """Checks if the given answer is correct.

  Args:
    clue: Clue being presented
    answer: The real response to the clue
    response: The user's response to the clue

  Returns:
    bool: Whether the response to the clue was correct
    answer_response: Explanation on why the user's response was right/wrong
  """
  response = model.generate_content(_JEOPARDY_PROMPT.format(
    clue=clue, question=answer, response=response)
  ).text

  if response.startswith("Yes. That is correct."):
    return True, response[len("Yes. That is correct."):]
  return False, response[len("No. That is incorrect."):]
