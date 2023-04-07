class Book:
    _ID: int = None
    _title: str = None
    _author: str = None
    _category: str = None
    _quantity: int = None
    _availability: bool = None

    def __init__(self, title: str, author: str, category: str, quantity: int = 5, id: int = None):
        self._ID = id
        self._title = title
        self._author = author
        self._category = category
        self._quantity = quantity
        self._updateAvailability()

    def getID(self):
        return self._ID

    def getTitle(self):
        return self._title

    def getCategory(self):
        return self._category

    def getQuantity(self):
        return self._quantity

    def getAvailability(self):
        return self._availability

    def borrowBook(self) -> bool:
        if self._quantity == 0:
            return False
        self._quantity -= 1
        self._updateAvailability()

    def getAuthor(self):
        return self._author

    def _updateAvailability(self):
        if self._quantity > 0:
            self._availability = True
        else:
            self._availability = False

    def updateID(self, db: 'DbManager'):
        self._ID = db.getBookID(self)

    def __str__(self):
        return f"{self._title}, {self._author}, {self._category}"

    def __eq__(self, other: "Book"):
        if self._ID == other.getID() and \
                self._title == other.getTitle() and \
                self._author == other.getAuthor() and \
                self._category == other.getCategory() and \
                self._availability == other.getAvailability() and \
                self._quantity == other.getQuantity():
            return True
        return False
