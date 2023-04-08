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
libraryHeading = ["ID Number", "Title", "Author", "Category", "Quantity"]
bookChoices = []


class SearchBy(Screen):
    def compose(self) -> ComposeResult:
        with Container(classes='container'):
            yield Static("Search for book by:", classes="text")
            yield Button("Title", id="title", variant="primary")
            yield Button("Author", id="author", variant="primary")
            yield Button("Category", id="category", variant="primary")


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
            with Horizontal(classes="top"):
                yield Button("<", id='back', variant="error")
                self.input = Input(placeholder="Search Query")
                yield self.input

            self.table = DataTable()
            rows = iter(libraryArr)
            self.table.add_columns(*libraryHeading)
            self.table.add_rows(rows)
            self.table.zebra_stripes = True
            self.table.cursor_type = "row"
            yield self.table
            with Horizontal(classes='bottom'):
                yield Button("Add to Cart", id='addToCart', variant="primary")
                yield Button(">>", id='next', variant="success")
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
            rows = iter(libraryArr)
            self.table.add_rows(rows)

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == 'addToCart':
            row = self.table.cursor_row
            bookID = self.table.get_row_at(row)[0]
            global bookChoices
            bookChoices.append(bookID)
        elif event.button.id == 'next':
            await self.app.push_screen('checkout')





# self.table = DataTable()
#             rows = iter(libraryArr)
#             self.table.add_columns(*libraryHeading)
#             self.table.add_rows(rows)
#             self.table.zebra_stripes = True
#             self.table.cursor_type = "row"
#             yield self.table

class Checkout(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(classes="container"):
            yield Button("<", id='back', variant="error")
            table = DataTable()
            books = []
            for el in bookChoices:
                books.append(db.searchBooks(SearchField.id, el)[0])
            table.add_columns(*libraryHeading)
            table.add_rows(books)
            yield Button("Check Out", variant="success")
        yield Footer()

class LibraryApp(App):
    """The main application function"""
    BINDINGS = [
        ('f1', 'toggle_dark', 'Toggle Dark Mode'),
        ('q', 'quit', "Quit"),
        ('r', 'resetCart', "Reset Shopping Cart")
    ]
    CSS_PATH = "interface.css"

    TITLE = "MyLibrary"
    SUB_TITLE = "Your source for all the best books!"

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        self.install_screen(SearchBy(), name="buttonContainer")
        self.install_screen(Checkout(), name='checkout')
        self.install_screen(Search(), name='searchContainer')
        self.push_screen('buttonContainer')
        yield Footer()


    async def action_search(self):
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
        self.query_one("searchContainer").searchString = ""

    def action_resetCart(self):
        global bookChoices
        bookChoices = []
        # todo: confirmation


if __name__ == '__main__':
    libraryArr = LibraryApp()
    libraryArr.run()
    # main()

