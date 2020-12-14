from books.models import Book, Author


def add_book_to_existing_author(title, first_name, last_name) -> None:
    """Adds a book to an existing author"""
    author = Author.objects.get(first_name=first_name, last_name=last_name)
    book = Book(title=title, author=author)
    book.save()


def add_book_with_author(title, first_name, last_name) -> None:
    """Adds a book and author at the same time, relating them also"""
    author = Author(first_name=first_name, last_name=last_name)
    author.save()
    book = Book(title=title, author=author)
    book.save()
