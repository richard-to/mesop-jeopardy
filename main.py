import json
import logging
import os
import random
import time

import css
import trebek_bot
import question_bank
import mesop as me


_NUM_CATEGORIES = 6
_MAX_RETRIES = 3


@me.stateclass
class State:
  selected_clue: str
  # We use a dict since dataclasses do not seem to be deserialized back to a dict.
  # This may be due to the use of the nested list.
  board: list[list[dict[str, str | int]]]
  # Used for clearing the text input.
  response_value: str
  response: str
  answer_is_correct: bool = False
  answer_check_response: str
  score: int
  # Key format: click-{row_index}-{col_index}
  selected_question_key: str
  # Set is not JSON serializable
  # Key format: click-{row_index}-{col_index}
  answered_questions: dict[str, bool]
  modal_open: bool = False
  # App is loading
  loading: bool = False
  # Means that we failed to load or generate the questions.
  loading_failed: bool = False


@me.page(
    path="/",
    title="Mesop Jeopardy",
    security_policy=me.SecurityPolicy(
      allowed_iframe_parents=["https://huggingface.co"]
    ),
)
def app():
  state = me.state(State)

  if state.loading:
    with me.box(style=css.LOADING_PAGE):
      me.progress_spinner()
      me.text(
        "Generating Jeopardy questions...",
        style=me.Style(font_size=20, font_weight="bold", margin=me.Margin(left=10))
      )
    return

  if state.loading_failed:
    with me.box(style=css.LOADING_PAGE):
      me.text(
        "Failed to generate Jeopardy questions.",
        style=me.Style(font_size=20, font_weight="bold", margin=me.Margin(right=15))
      )
      me.button(
        "Try Again",
        type="raised",
        style=me.Style(background=css.COLOR_YELLOW, color="#000"),
        on_click=on_generate_questions)
    return

  if not state.board:
    with me.box(style=css.LOADING_PAGE):
      me.button(
        "Start Game",
        type="raised",
        style=me.Style(font_size=30, padding=me.Padding.all("30px"), background=css.COLOR_YELLOW, color="#000"),
        on_click=on_generate_questions)
    return

  # Modal is displayed to notify when the user is correct or not.
  with modal(state.modal_open):
    with me.box(style=css.MODAL_HEADER):
      me.text("Correct!" if state.answer_is_correct else "Wrong!", type="headline-5")
      with me.box(on_click=on_click_close_modal):
        me.icon("close")
    me.text(state.answer_check_response)

  with me.box(style=css.MAIN_COL_GRID):
    with me.box(style=css.BOARD_COL_GRID):
      for col_index in range(len(state.board[0])):
        # Render Jeopardy categories
        if col_index == 0:
          for row_index in range(len(state.board)):
            cell = state.board[row_index][col_index]
            with me.box(style=css.CATEGORY_BOX):
              me.text(cell["category"])

        # Render Jeopardy questions
        for row_index in range(len(state.board)):
          cell = state.board[row_index][col_index]
          key = f"clue-{row_index}-{col_index}"
          is_selectable = not (key in state.answered_questions or state.selected_question_key)
          with me.box(style=css.clue_box(is_selectable), key=key, on_click=on_click_cell):
            if key in state.answered_questions:
              me.text("")
            elif key == state.selected_question_key:
              me.text(cell["question"], style=me.Style(text_align="left"))
            else:
              me.text(f"${cell['normalized_value']}", style=me.Style(font_size="2.2vw"))

    # Sidebar
    with me.box(style=css.SIDEBAR):

      # Score
      with me.box(style=css.SIDEBAR_SECTION):
        me.text("Score", type="headline-5")
        with me.box(style=css.SCORE_BOX):
          me.text(format_dollars(state.score), style=css.score_text(state.score))

      # Clue
      with me.box(style=css.SIDEBAR_SECTION):
        me.text("Clue", type="headline-5")
        with me.box(style=css.CURRENT_CLUE_BOX):
          if state.selected_question_key:
            selected_question = get_selected_question(state.board, state.selected_question_key)
            me.text(selected_question["question"])
          else:
            me.text("No clue selected. Please select one.", style=me.Style(font_style="italic"))

      # Response
      with me.box(style=css.SIDEBAR_SECTION):
        me.text("Response", type="headline-5")
        me.textarea(
          label="Enter your response",
          value=state.response_value,
          disabled=not bool(state.selected_question_key),
          on_blur=on_input_response,
          style=css.RESPONSE_INPUT,
        )

        disabled = not bool(state.selected_question_key)
        me.button(
          label="Submit your response",
          type="flat",
          disabled=disabled,
          style=css.response_button(disabled),
          on_click=on_click_submit,
        )


def on_generate_questions(e: me.ClickEvent):
  state = me.state(State)
  state.loading_failed = False
  state.loading = True
  yield

  try:
    state.board = make_default_board(question_bank.load(
      use_gemini=os.environ.get("GENERATE_JEOPARDY_QUESTIONS", "false").lower() == "true"
    ))
  except json.JSONDecodeError:
    logging.warning("Gemini failed to generate valid JSON.")

  # Sometimes Gemini does not generate enough categories and questions.
  if len(state.board) != _NUM_CATEGORIES:
    state.loading_failed = True
    state.board = []

  state.loading = False
  yield


def on_click_cell(e: me.ClickEvent):
  """Selects the given clue.

  This function is noop if the following states are true:

  - Clue is already selected (user must answer first).
  - Clue is alreaady answered (can't answer clues that have already been done).
  """
  state = me.state(State)
  if state.selected_question_key or e.key in state.answered_questions:
    return
  state.selected_question_key = e.key


def on_input_response(e: me.InputBlurEvent):
  """Stores user input into state, so we can process their response."""
  state = me.state(State)
  state.response = e.value


def on_click_submit(e: me.ClickEvent):
  """Submit user response to clue to check if they are correct."""
  state = me.state(State)
  if not state.response.strip():
    return

  selected_question = get_selected_question(state.board, state.selected_question_key)

  # Check and score answer.
  is_correct, response = trebek_bot.check_answer(
    selected_question["question"],
    selected_question["answer"],
    state.response,
  )
  if is_correct:
    state.score += selected_question["normalized_value"]
  else:
    state.score -= selected_question["normalized_value"]

  # Clear question so another can be picked.
  state.answered_questions[state.selected_question_key] = True
  state.selected_question_key = ""

  # Set up modal response.
  state.modal_open = True
  state.answer_is_correct = is_correct
  state.answer_check_response = response

  # Hack to reset text input. Update the initial response value to current response
  # first, which will trigger a diff when we set the initial response back to empty
  # string.
  #
  # A small delay is also needed because some times the yield happens too fast, which
  # does not allow the UI on the client to update properly.
  state.response_value = state.response
  yield
  time.sleep(0.5)
  state.response_value = ""
  yield


def on_click_close_modal(e: me.ClickEvent):
  """Allows modal to be closed by clicking on the modal background."""
  state = me.state(State)
  if state.modal_open:
    state.modal_open = False


@me.content_component
def modal(modal_open: bool):
  """Basic modal box component."""
  with me.box(style=css.modal_background(modal_open)):
    with me.box(style=css.MODAL_GRID):
      with me.box(style=css.MODAL_CONTAINER):
        with me.box(style=css.MODAL_CONTENT):
          me.slot()


def make_default_board(jeopardy_questions) -> list[list[dict[str, str]]]:
  """Creates a board with some random jeopardy questions."""
  random.shuffle(jeopardy_questions)
  return jeopardy_questions[:_NUM_CATEGORIES]


def get_selected_question(board, selected_question_key) -> dict[str, str]:
  """Gets the selected question from the key."""
  _, row, col = selected_question_key.split("-")
  return board[int(row)][int(col)]


def format_dollars(value: int) -> str:
  """Formats an integer value in US dollars format."""
  if value < 0:
    return f"-${value * -1:,}"
  return f"${value:,}"
