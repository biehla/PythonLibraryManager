from Library.Book import Book
from Library.dbManager import DbManager, SearchField
from unittest import TestCase


class testDbManager(TestCase):
    def setUp(self) -> None:
        with open("test.db", 'w') as f:
            pass

        self.db = DbManager("test.db")
        self.testBook = Book("Around the world in 80 days", "jules vernes", "scifi")
        self.db.addBook(self.testBook)
        self.testBook.updateID(self.db)

    def testGetBookID(self):
        self.assertEqual(self.testBook.getID(), 1)

    def testSearchBooks(self):
        books = self.db.searchBooks(SearchField.category, 'scifi')
        for book in books:
            self.assertEqual(book, Book("Around the world in 80 days", "jules vernes", "scifi", id=1))

    def testAddBook(self):
        newBook = Book("Perl 5 for Dummies", "Dummies", "scifi")
        self.db.addBook(newBook)
        newSearch = self.db.searchBooks(SearchField.category, 'scifi')
        contents = [str(i) for i in newSearch]
        self.assertTrue(len(newSearch) == 2, msg=f"Actual length: {len(newSearch)}, Contents: {contents}")

if __name__ == '__main__':
    testDbManager.main()

