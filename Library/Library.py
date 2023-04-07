from Library.dbManager import DbManager, SearchField


class Library:
    library: ["Book"] = []

    def __init__(self):
        self.dbManager = None

        self.getBooksFromDB()

    def getBooksFromDB(self):
        self.dbManager = DbManager()
        self.library = self.dbManager.getLibrary()


"""
    library features:
        borrow books
        search books
        generate receipt with due dates (30 days from rent day)
"""