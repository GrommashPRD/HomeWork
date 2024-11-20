import json
import os
from typing import List, Dict


class Book:
    """
    Класс для представления книги в библиотеке.
    """

    def __init__(self, id, title, author, year, status="в наличии"):
        """
        Инициализирует объект книги.

        """
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        """
        Преобразует объект Book() в словарь.

        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        """
        Создает объект Book() из словаря.

        """
        return Book(data['id'], data['title'], data['author'], data['year'], data['status'])

    def __str__(self):
        return f"ID: {self.id}, Название: {self.title}, Автор: {self.author}, Год: {self.year}, Статус: {self.status}"


class Library:
    """
    Класс библиотеки.

    """

    def __init__(self, filename: str = 'library.json'):
        self.filename = filename
        self.books: List[Book] = []
        self.next_id: int = 1
        self.load_books()

    def load_books(self):
        """
        Загружает книги из JSON.

        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.books = [Book.from_dict(book) for book in data]
                self.next_id = max(book.id for book in self.books) + 1 if self.books else 1

    def save_books(self):
        """
        Сохраняет книги в JSON.

        """
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """
        Добавляет новую книгу в библиотеку.

        """
        new_book = Book(self.next_id, title, author, year)
        self.books.append(new_book)
        self.next_id += 1
        self.save_books()

    def remove_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f'Книга с ID {book_id} удалена.')
                return
        print(f'Ошибка: Книга с ID {book_id} не найдена.')

    def find_book(self, query):
        found_books = [book for book in self.books if
                       query.lower() in book.title.lower() or query.lower() in book.author.lower() or query.lower() in str(
                           book.year)]
        if found_books:
            return found_books
        else:
            print("Ошибка: Книги не найдены.")
            return []

    def list_books(self) -> None:
        """
        Все книги из библиотеки.

        """
        for book in self.books:
            print(book)

    def borrow_book(self, book_id: int):
        """
        Позволяет взять книгу в аренду.
        И вернуть обратно в библиотеку.

        """
        for book in self.books:
            if book.id == book_id:
                if book.status == "в наличии":
                    book.status = "арендована"
                    self.save_books()
                    print(f"Вы взяли книгу: {book.title}")
                    return
                elif book.status == "арендована":
                    book.status = "в наличии"
                    self.save_books()
                    print(f"Вы вернули книгу: {book.title}")
                    return
        raise ValueError("Книга не найдена.")


def main():
    library = Library()

    while True:
        print("\nВыберите операцию:")
        print("1 - Добавить книгу")
        print("2 - Удалить книгу")
        print("3 - Найти книгу")
        print("4 - Отобразить все книги")
        print("5 - Изменить статус книги")
        print("0 - Выйти")

        choice = input("Ваш выбор: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год публикации: ")
            library.add_book(title, author, year)

        elif choice == '2':
            book_id = int(input("Введите ID книги для удаления: "))
            library.remove_book(book_id)

        elif choice == '3':
            query = input("Введите название или автора книги для поиска: ")
            found_books = library.find_book(query)
            for book in found_books:
                print(book)

        elif choice == '4':
            library.list_books()

        elif choice == '5':
            book_id = int(input("Введите ID книги для изменения статуса: "))
            library.borrow_book(book_id)

        elif choice == '0':
            print("Выход из программы.")
            break

        else:
            print("Ошибка: Неверный ввод. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
