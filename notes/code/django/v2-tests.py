from django.test import TestCase
from books.models import Book, Author
from books.utility import add_book_with_author, add_book_to_existing_author

# Create your tests here.
class TestAddBookToExistingAuthor(TestCase):
    def setUp(self):
        author1 = Author(first_name="Jack", last_name="London")
        author2 = Author(first_name="Jack", last_name="Black")
        author1.save()
        author2.save()
        self.assertEqual(
            len(Author.objects.all()),
            2,
            f"Wrong number of authors found in test setup!",
        )

    def test_it_works(self) -> None:
        """When given all parameters, should actually work"""
        add_book_to_existing_author("White Fang", "Jack", "London")

        # the book sghould have been created
        all_books = Book.objects.all()
        self.assertEqual(
            len(all_books),
            1,
            f"Incorrect number of books - expecting just the added one!",
        )

        #  the book should exist and have the right title and author
        white_fang = Book.objects.all()[0]
        self.assertEqual(white_fang.title, "White Fang", f"Wrong title!")
        self.assertEqual(
            white_fang.author.first_name, "Jack", f"Wrong Author first name!"
        )
        self.assertEqual(
            white_fang.author.last_name, "London", f"Wrong author last name!"
        )

        # also, they should be linked in the db
        jack_london = Author.objects.get(first_name="Jack", last_name="London")
        self.assertEqual(
            white_fang.author,
            jack_london,
            f"Book created, but not linked to the existing author!",
        )


class TestAddBook(TestCase):
    def test_should_work(self) -> None:
        add_book_with_author("A Memoir", "Bob", "Howard")

        all_books = Book.objects.all()
        all_authors = Author.objects.all()

        # first check that they exist
        self.assertEqual(
            len(all_books), 1, f"Unexpected number of books given that we only added 1!"
        )
        self.assertEqual(
            len(all_authors),
            1,
            f"Unexpected number of authors given that we only added 1!",
        )

        # now check that they have the right attributes
        the_book = all_books[0]
        the_author = all_authors[0]

        self.assertEqual(the_book.title, "A Memoir", f"Wrong title!")
        self.assertEqual(the_author.first_name, "Bob", f"Wrong first name!")
        self.assertEqual(the_author.last_name, "Howard", f"Wrong last name!")

        # now check that they've been linked properly
        self.assertEqual(
            the_book.author, the_author, f"The book and title weren't linked properly!"
        )
