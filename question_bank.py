import json
import re

from collections import defaultdict


QuestionSet = list[dict[str, str]]


_JEOPARDY_DATA = "data/jeopardy.json"
_NUM_QUESTIONS_PER_CATEGORY = 5


def load() -> list[QuestionSet]:
  """Loads a cleaned up data set to use in Mesop Jeopardy game."""
  data = _load_raw_data()
  data = _add_raw_value(data)
  data = _clean_questions(data)
  question_sets = _group_into_question_sets(data)
  question_sets = _sort_question_sets(question_sets)
  question_sets = _normalize_values(question_sets)
  return _filter_out_final_jeopardy_question_sets(question_sets)


def _load_raw_data() -> QuestionSet:
  """Load the raw data set.

  Format of each question/clue looks like this:

  {
    "category": "HISTORY",
    "air_date": "2004-12-31",
    "question": "'For the last 8 years of his life, Galileo was...",
    "value": "$200",
    "answer": "Copernicus",
    "round": "Jeopardy!",
    "show_number": "4680"
  }
  """
  with open(_JEOPARDY_DATA, "r") as f:
    return json.load(f)


def _add_raw_value(data: QuestionSet) -> QuestionSet:
  """Add raw value since the value is formatted as a dollar string that isn't as easy
  to sort"""
  for row in data:
    row["raw_value"] = _convert_dollar_amount(row["value"])
  return data


def _clean_questions(data: QuestionSet) -> QuestionSet:
  """Clean up questions

  - Strip single quotes around each question
  - Replace escaped single quotes
  - Strip HTML tags
  """
  for row in data:
    row["question"] = re.sub(
      "<[^<]+?>", "",
      row["question"].strip("'").replace("\\'", "'")
    )
  return data


def _convert_dollar_amount(value: str) -> int:
  """Coverts raw value into an integer.

  The raw value is string formatted as a dollar amount, such as $1,000. In this
  dataset the dollar amount is not given for Daily Doubles that were not answered, so
  we'll set those cases to a value of 0 for now.

  In addition, answered daily doubles will have odd dollar amounts.

  These values won't be used in the actually game. Only for roughly sorting the
  question difficulty.
  """
  if value:
    return int(value.replace("$", "").replace(",", ""))
  else:
    return 0


def _group_into_question_sets(data: QuestionSet) -> list[QuestionSet]:
  """Groups the questions by category for that air date.

  We want to mix and match questions across games, but we want to keep the questions
  within a category together.
  """
  question_sets = defaultdict(lambda: [])
  for row in data:
    question_sets[(row["category"], row["air_date"])].append(row)
  return list(question_sets.values())


def _sort_question_sets(question_sets: list[QuestionSet]) -> list[QuestionSet]:
  return [_sort_question_set(question_set) for question_set in question_sets]


def _sort_question_set(question_set: QuestionSet) -> QuestionSet:
  """Sort the question sets so they are ordered roughly in order difficulty.

  This will not always be true due to Daily Doubles skewing the order. The data set
  did not store the Daily Double values separately from the normal game value.
  """
  return sorted(question_set, key=lambda q: q["raw_value"])


def _normalize_values(question_sets: list[QuestionSet]) -> list[QuestionSet]:
  """Normalizes question dollar amounts based on order of appearance.

  Since we picking random categories across different rounds and years, the dollar
  values will differ. So we will normalize them here.
  """
  for question_set in question_sets:
    for index, question in enumerate(question_set):
      question["normalized_value"] = (index + 1) * 200
  return question_sets


def _filter_out_final_jeopardy_question_sets(question_sets: list[QuestionSet]) -> list[QuestionSet]:
  """Filters out questions set for Final Jeopardy.

  Final Jeopardy categories only have one question so we want to ignore those.
  We also want to avoid anomalies in the data set.
  """
  return [
    question_set for question_set in question_sets
    if len(question_set) == _NUM_QUESTIONS_PER_CATEGORY
  ]
