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
  "max_output_tokens": 16384,
  "response_mime_type": "application/json",
})


_JEOPARDY_QUESTION_GENERATE_PROMPT = """
You are a Jeopardy! expert who specializes in crafting great questions.

Generate Jeopardy! questions to populate a Jeopardy! board.

A Jeopardy! category has 5 questions of increasing difficulty.

A Jeopardy! board has 6 categories.

Populate the categories in JSON Format using this template:

```
{
  "CATEGORY 1": [
   {
      "question": "'Question 1",
      "value": "$200",
      "answer": "Answer 1"
    },
    {
      "question": "'Question 2",
      "value": "$400",
      "answer": "Answer 2"
    },
  ],
  "CATEGORY 2": [],
  "CATEGORY 3": [],
  "CATEGORY 4": [],
  "CATEGORY 5": [],
  "CATEGORY 6": [],
}
```
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
  question_sets = json.loads(
    question_gen_model.generate_content(_JEOPARDY_QUESTION_GENERATE_PROMPT).text
  )
  questions_list = []
  # Format the questions like the data set.
  for category, questions in question_sets.items():
    for question in questions:
      questions_list.append(
        {
          "category": category,
          "air_date": "2024-1-1",
          "show_number": "0",
          **question
        }
      )
  return questions_list
