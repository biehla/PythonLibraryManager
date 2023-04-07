from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal, Grid
from textual.events import Click
from textual.screen import Screen, ModalScreen
from textual.widgets import Header, Footer, Button, Static, Label, Input

from Library.Library import Library
from Library.dbManager import SearchField

searchType: SearchField = None

class SearchBy(Screen):
    def compose(self) -> ComposeResult:
        with Container(classes='container'):
            yield Static("Search for book by:", classes="text")
            yield Button("Title", id="title")
            yield Button("Author", id="author")
            yield Button("Category", id="category")



class Search(Screen):
    BINDINGS = [
        ('b', "goBack", "Go Back")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(classes='container'):
            with Horizontal():
                yield Button("<", id='back')
                self.input = Input(placeholder="Search Query")
                self.input.cursor_blink = True
                yield self.input
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        self.input.value = ""

    # def on_event(self, event: events.Event) -> None:
    #     if type(event) == events.Paste:
    #         self.input.value =



class LibraryApp(App):
    """The main application function"""
    BINDINGS = [
        ('f1', 'toggle_dark', 'Toggle Dark Mode'),
        ('q', 'quit', "Quit")
    ]
    CSS_PATH = "interface.css"

    TITLE = "MyLibrary"
    SUB_TITLE = "Your source for all the best books!"

    def compose(self) -> ComposeResult:
        yield Header()
        self.install_screen(SearchBy(), name="buttonContainer")
        self.install_screen(Search(), name='searchContainer')
        self.push_screen('buttonContainer')
        yield Footer()

    # def on_mount(self) -> None:


    async def action_search(self):
        # self.pop_screen()
        self.push_screen('searchContainer')

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        buttonID = event.button.id
        print(buttonID)
        global searchType
        match buttonID:
            case "title":
                searchType = SearchField.title
                await self.run_action("search")
            case "category":
                searchType = SearchField.category
                await self.run_action("search")
            case "author":
                searchType = SearchField.author
                await self.run_action("search")
            case "back":
                await self.run_action("goBack")

    async def action_goBack(self):
        self.pop_screen()

    # async def action_searchByAuthor(self):
    #     self.searchBy.styles.display = "none"
    #     global searchType
    #     searchType = SearchField.author
    #
    # async def action_searchByCategory(self):
    #     self.searchBy.styles.display = "none"
    #     global searchType
    #     searchType = SearchField.category


if __name__ == '__main__':
    library = LibraryApp()
    library.run()
    # main()

