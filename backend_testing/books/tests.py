from django.test import TestCase
from books.models import Book, Author
from books.utility import add_book_to_existing_author


class TestAddBookToExistingAuthor(TestCase):
    def setUp(self):
        """Set up the tests"""
        Author(first_name="Jack", last_name="London").save()
        Author(first_name="Jack", last_name="White").save()

    def test_it_works(self):
        """When given correct parameters, it should work!"""
        add_book_to_existing_author("White Fang", "Jack", "London")
        all_books = Book.objects.all()
        self.assertEqual(
            len(all_books), 1, f"Expected to find only one book, but found {all_books}"
        )
        white_fang = all_books[0]

        # &c.
        self.assertEqual(white_fang.title, "White Fang", f"")
        self.assertEqual(white_fang.author.first_name, "Jack", f"")
        self.assertEqual(white_fang.author.last_name, "London", f"")

        # asserting that it was added to the right author
        jack_london = Author.objects.get(first_name="Jack", last_name="London")
        self.assertEqual(white_fang.author, jack_london, f"Incorrect author!")
