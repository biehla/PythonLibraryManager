from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal, Grid
from textual.events import Click
from textual.reactive import reactive
from textual.screen import Screen, ModalScreen
from textual.widgets import Header, Footer, Button, Static, Label, Input, DataTable

from Library.dbManager import DbManager
from Library.dbManager import SearchField
from Library.Book import Book


searchType: SearchField = None
db = DbManager()
libraryArr: [str] = db.getLibraryAsList()
libraryHeading = ["Title", "Author", "Category", "Quantity"]


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

    searchString: str = reactive("")

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(classes='container search'):
            with Horizontal():
                yield Button("<", id='back')
                self.input = Input(placeholder="Search Query")
                yield self.input

            self.table = DataTable()
            self.rows = iter(libraryArr)
            self.table.add_columns(*libraryHeading)
            self.table.add_rows(self.rows)
            yield self.table
        yield Footer()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.value != '':
            self.searchString = event.value
            self.table.clear()
            result = db.searchBooks(searchType, self.searchString)
            print(searchType, self.searchString)
            self.table.add_rows(result)
            # self.compose()
        else:
            self.table.clear()
            self.rows = iter(libraryArr)
            self.table.add_rows(self.rows)






class LibraryApp(App):
    """The main application function"""
    BINDINGS = [
        ('f1', 'toggle_dark', 'Toggle Dark Mode'),
        ('q', 'quit', "Quit")
    ]
    CSS_PATH = "interface.css"

    TITLE = "MyLibrary"
    SUB_TITLE = "Your source for all the best books!"

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        self.install_screen(SearchBy(), name="buttonContainer")
        self.push_screen('buttonContainer')
        yield Footer()


    async def action_search(self):
        self.install_screen(Search(), name='searchContainer')
        # self.pop_screen()
        await self.push_screen(Search())

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
                await self.run_action('goBack')

    def action_goBack(self):
        self.app.pop_screen()
        self.app.uninstall_screen('searchContainer')


if __name__ == '__main__':
    libraryArr = LibraryApp()
    libraryArr.run()
    # main()

