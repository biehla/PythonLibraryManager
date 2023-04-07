import unittest

from Library.Book import Book


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.testBook = Book("The Hitch Hiker's Guide to the Galaxy", "Douglas Adams", "scifi", quantity=3, id=9)

    def testGetID(self):
        self.assertEqual(self.testBook.getID(), 9)

    def testGetTitle(self):
        self.assertEqual(self.testBook.getTitle(), "The Hitch Hiker's Guide to the Galaxy")

    def testGetCategory(self):
        self.assertEqual(self.testBook.getCategory(), "scifi")

    def testGetQuantity(self):
        self.assertEqual(self.testBook.getQuantity(), 3)

    def testGetAvailability(self):
        self.assertTrue(self.testBook.getAvailability())

if __name__ == '__main__':
    unittest.main()
