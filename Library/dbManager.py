import sqlite3
from enum import Enum


class SearchField(Enum):
    id = 0,
    title = 1,
    author = 2,
    category = 3,


class DbManager:
    def __init__(self, dbPath="library.db"):
        self.connection = sqlite3.connect(dbPath)
        self.cursor = self.connection.cursor()
        self.createDatabase()

    def createDatabase(self):
        SQLStatementBookTable = """
            CREATE TABLE IF NOT EXISTS Book (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                category TEXT NOT NULL,
                availability INT NOT NULL,
                quantity INTEGER NOT NULL
            )
        """

        self.cursor.execute(SQLStatementBookTable)
        self.connection.commit()

    def addBook(self, book):
        # for book in self.searchBooks(SearchField.title, book.getTitle()):

        addBookStatement = """
            INSERT INTO Book(title, author, category, availability, quantity)
                VALUES(?, ?, ?, ?, ?)
        """

        bookValues = [book.getTitle(), book.getAuthor(), book.getCategory(), book.getAvailability(), book.getQuantity()]

        self.cursor.execute(addBookStatement, bookValues)
        self.connection.commit()

    def searchBooks(self, searchField: SearchField, searchVar) -> []:
        searchString = None
        category = None
        searchVar = "%" + searchVar + "%"

        match searchField:
            case SearchField.id:
                searchString = "SELECT * FROM Book WHERE id LIKE ?"
            case SearchField.title:
                searchString = "SELECT * FROM Book WHERE title LIKE ?"
            case SearchField.author:
                searchString = "SELECT * FROM Book WHERE author LIKE ?"
            case SearchField.category:
                searchString = "SELECT * FROM Book WHERE category LIKE ?"

        books = self.cursor.execute(searchString, [searchVar]).fetchall()
        return self._convertToBookArray(books)

    def getLibraryAsList(self) -> [[]]:
        getAllQuery = "SELECT * FROM Book"
        books = self.cursor.execute(getAllQuery).fetchall()
        return self._convertToArray(books)

    def getBookID(self, book: "Book") -> int|None:
        getBookStatement = "SELECT id FROM Book WHERE title = ? AND author = ? AND category = ?"
        result = self.cursor.execute(getBookStatement, [book.getTitle(), book.getAuthor(), book.getCategory()])
        id = result.fetchone()
        if id is None:
            return None
        return id[0]

    def _convertToBookArray(self, books: [tuple]) -> ["Book"]:
        bookArray = []
        import Library.Book
        for index, book in enumerate(books):
            if len(book) != 6:
                continue
            bookArray.append(Library.Book.Book(book[1], book[2], book[3], quantity=book[5], id=book[0]))
        return bookArray

    def _convertToArray(self, books: [tuple]) -> ["Book"]:
        bookArray = []
        import Library.Book
        for index, book in enumerate(books):
            if len(book) != 6:
                continue
            bookArray.append([book[1], book[2], book[3]])
        return bookArray