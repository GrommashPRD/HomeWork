import unittest

from Library import Library


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library("memory")  # Используем временный файл для тестирования
        self.library.add_book("Test Book", "Test Author", 2023)

    def test_add_book(self):
        self.library.add_book("New Book", "New Author", 2022)
        self.assertEqual(len(self.library.books), 2)

    def test_borrow_book(self):
        self.library.borrow_book(1)
        self.assertEqual(self.library.books[0].status, "арендована")

    def test_return_book(self):
        self.library.borrow_book(1)
        self.assertEqual(self.library.books[0].status, "в наличии")


if __name__ == '__main__':
    unittest.main()