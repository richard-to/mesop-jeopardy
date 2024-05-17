import mesop as me

COLOR_BLUE = "blue"
COLOR_YELLOW = "#f0cd6e"
COLOR_RED = "#cc153c"
COLOR_DISABLED_BG = "#ccc"

MAIN_COL_GRID = me.Style(
  background="#ececec",
  display="grid",
  grid_template_columns="70% 30%",
  height="100vh",
)

BOARD_COL_GRID = me.Style(
  background="#000",
  display="grid",
  gap="5px",
  grid_template_columns="repeat(6, 1fr)",
)

CATEGORY_BOX = me.Style(
  background=COLOR_BLUE,
  color="white",
  font_weight="bold",
  font_size="1em",
  padding=me.Padding.all(15),
  text_align="center",
)

CLUE_BOX = me.Style(
  background=COLOR_BLUE,
  color=COLOR_YELLOW,
  cursor="pointer",
  font_size="1em",
  font_weight="bold",
  padding=me.Padding.all(15),
  text_align="center",
)

SIDEBAR = me.Style(
  color="#111",
  overflow_y="scroll",
  padding=me.Padding.all(20),
)

SIDEBAR_SECTION = me.Style(margin=me.Margin(bottom=15))

SCORE_BOX = me.Style(
  background=COLOR_BLUE,
  color="white",
  font_weight="bold",
  font_size="2.2vw",
  padding=me.Padding.all(15),
  text_align="center",
)

CURRENT_CLUE_BOX = me.Style(
  background=COLOR_BLUE,
  color=COLOR_YELLOW,
  font_size="1em",
  font_weight="bold",
  padding=me.Padding.all(15),
)

RESPONSE_INPUT = me.Style(width="100%")

SELECT_CLUE_BOX = me.Style(
  background=COLOR_BLUE,
  color="white",
  padding=me.Padding.all(15),
  margin=me.Margin(bottom=20),
)

MODAL_GRID = me.Style(
  align_items="center",
  display="grid",
  height="100vh",
  justify_items="center",
)

MODAL_CONTAINER = me.Style(
  background="#ececec",
  border_radius="15px",
  box_sizing="content-box",
  box_shadow=("0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"),
  color="#222",
  font_size="18px",
  line_height="1.3",
  width="min(500px, 100%)",
)

MODAL_CONTENT = me.Style(margin=me.Margin.all(20))

MODAL_HEADER = me.Style(display="flex", justify_content="space-between")


def modal_background(modal_open: bool) -> me.Style:
  """Makes style for modal background.

  Args:
    modal_open: Whether the modal is open.
  """
  return me.Style(
    background="rgba(0,0,0,0.4)",
    display="block" if modal_open else "none",
    height="100%",
    overflow_x="auto",
    overflow_y="auto",
    position="fixed",
    width="100%",
    z_index=1000,
  )


def clue_box(is_selectable: bool) -> me.Style:
  """Style for clue box

  Args:
    is_selectable: Visual signify if the clue is selectable.
  """
  return  me.Style(
    background=COLOR_BLUE,
    color=COLOR_YELLOW,
    cursor="pointer" if is_selectable else "default",
    font_size="1em",
    font_weight="bold",
    padding=me.Padding.all(15),
    text_align="center"
  )


def response_button(disabled: bool) -> me.Style:
  """Styles for response submit button.

  Args:
    disabled: Since we're overriding the style, we need to handle disabled state
  """
  if disabled:
    return me.Style(background=COLOR_DISABLED_BG, color="#eee")
  return me.Style(background=COLOR_BLUE, color="white")


def score_text(score: int) -> me.Style:
  """In Jeopardy when the score is negative, it is red instead of white."""
  return me.Style(color="white" if score >= 0 else COLOR_RED)
