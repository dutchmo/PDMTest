from datetime import date

import rapidfuzz
from rich.text import Text

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Grid
from textual.screen import Screen, ModalScreen
from textual.widgets import DataTable, Footer, Input, Rule, Static, Label, Button, Digits

ROWS = [
    ("lane", "swimmer", "country", "time 1", "time 2", "created"),
    (4, "Joseph Schooling", Text("Singapore", style="italic"), 50.39, 51.84, date(2023, 3, 1)),
    (2, "Michael Phelps", Text("United States", style="italic"), 50.39, 51.84, date(2023, 3, 1)),
    (5, "Tom Shads", Text("South Africa", style="italic"), 51.14, 51.73, date(2023, 3, 7)),
    (6, "László Cseh", Text("Hungary", style="italic"), 51.14, 51.58, date(2023, 3, 5)),
    (3, "Tammy Shields", Text("China", style="italic"), 51.26, 51.26, date(2023, 3, 2)),
    (8, "Mehdy Metella", Text("France", style="italic"), 51.58, 52.15, date(2023, 3, 9)),
    (7, "Tom Shields", Text("United States", style="italic"), 51.73, 51.12, date(2023, 3, 22)),
    (1, "Aleksandr Sadovnikov", Text("Russia", style="italic"), 51.84, 50.85, date(2023, 3, 1)),
    (10, "Darren Burns", Text("Scotland", style="italic"), 51.84, 51.55, date(2023, 6, 1)),
]


class QuitScreen(ModalScreen[bool]):
    """Screen with a dialog to quit."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.dismiss(True)
        else:
            self.dismiss(False)


class TableApp(App):
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=False, priority=True),
        Binding("escape", "toggle_search", "Search", show=True, priority=False),
        ("a", "sort_by_average_time", "Sort By Average Time"),
        ("n", "fuzzy_sort", "Fuzzy Sort By Last Name"),
        ("c", "sort_by_created", "Sort By Created"),
        ("q", "request_quit", "Quit")
    ]

    def action_request_quit(self) -> None:
        """Action to display the quit dialog."""

        def check_quit(quit: bool) -> None:
            """Called when QuitScreen is dismissed."""
            if quit:
                self.exit()

        self.push_screen(QuitScreen(), check_quit)

    #SCREENS = {"bsod": BSOD()}

    CSS = """
    Input {
    text-style: bold italic;
  border: red;
  }
  
QuitScreen {
    align: center middle;
}

#dialog {
    grid-size: 2;
    grid-gutter: 1 2;
    grid-rows: 1fr 3;
    padding: 0 1;
    width: 60;
    height: 11;
    border: thick $background 80%;
    background: $surface;
}

#question {
    column-span: 2;
    height: 1fr;
    width: 1fr;
    content-align: center middle;
}

Button {
    width: 100%;
}

    """

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self.notify(f" {event.row_key}", title="Select")

    current_sorts: set = set()

    def compose(self) -> ComposeResult:
        input = Input(placeholder="Filter", restrict=r"[a-zA-Z0-9_\-\s]*")
        datatable = DataTable(
            zebra_stripes=True,
            show_cursor=True,
            cursor_foreground_priority="css",
            cursor_background_priority="renderable",
            cursor_type="row",
            name=None,
            id=None,
        )
        yield input

        yield datatable
        yield Rule(line_style="heavy")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        for col in ROWS[0]:
            table.add_column(col, key=col)
        for number, row in enumerate(ROWS[1:], start=1):
            label = Text(str(number), style="#B0FC38 italic")
            table.add_row(*row, label=label)
        # table.add_rows(ROWS[1:])

    # def on_button_pressed(self) -> None:
    #     """Clear the text input."""
    #     input = self.query_one(Input)
    #     with input.prevent(Input.Changed):
    #         input.value = ""

    def action_toggle_search(self):
        input = self.query_one(Input)
        input.display = not input.display
        # input.remove()
        # if input.display:
        #     input.display = False
        # else:
        #     input.display = True

    def on_input_changed(self) -> None:
        """Called as the user types."""
        input = self.query_one(Input)
        self.action_fuzzy_sort(input.value)

        # with input.prevent(Input.Changed):
        #     self.action_fuzzy_sort(input.value)

    def on_input_submitted(self) -> None:
        """Called as the user types."""
        table = self.query_one(DataTable)
        row = table.get_row_at(0)
        self.notify(f" {row[0]}", title="Search")

    def sort_reverse(self, sort_type: str):
        """Determine if `sort_type` is ascending or descending."""
        reverse = sort_type in self.current_sorts
        if reverse:
            self.current_sorts.remove(sort_type)
        else:
            self.current_sorts.add(sort_type)
        return reverse

    def action_sort_by_average_time(self) -> None:
        """Sort DataTable by average of times (via a function) and
        passing of column data through positional arguments."""

        def sort_by_average_time_then_last_name(row_data):
            name, *scores = row_data
            return (sum(scores) / len(scores), name.split()[-1])

        table = self.query_one(DataTable)
        table.sort(
            "swimmer",
            "time 1",
            "time 2",
            key=sort_by_average_time_then_last_name,
            reverse=self.sort_reverse("time"),
        )

    def action_fuzzy_sort(self, filterby="++++++") -> None:
        """Sort DataTable by fuzzy (via a function) and
        passing of column data through positional arguments."""

        def sort_by_fuzzy_score(row_data):
            name = row_data
            weight = rapidfuzz.fuzz.token_sort_ratio(name, filterby)
            return weight
            # return (sum(scores) / len(scores), name.split()[-1])

        table = self.query_one(DataTable)
        # table.cursor_coordinate = (0, 0)
        table.action_scroll_home()
        table.sort(
            "swimmer",
            key=sort_by_fuzzy_score,
            reverse=True
        )

    def action_sort_by_created(self) -> None:
        """Sort DataTable by country which is a `Rich.Text` object."""
        table = self.query_one(DataTable)
        table.sort(
            "created",
            reverse=self.sort_reverse("created"),
        )

    def action_sort_by_columns(self) -> None:
        """Sort DataTable without a key."""
        table = self.query_one(DataTable)
        table.sort("swimmer", "lane", reverse=self.sort_reverse("columns"))


app = TableApp()
if __name__ == "__main__":
    app.run()
