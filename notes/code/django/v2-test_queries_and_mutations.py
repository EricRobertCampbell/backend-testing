from graphene_django.utils.testing import GraphQLTestCase
import json

from books.models import Book, Author
from backend_testing.schema import schema


class TestAllBooks(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    @classmethod
    def setUpClass(cls):
        super(TestAllBooks, cls).setUpClass()
        cls.query_string = """
        query {
            allBooks {
                title 
                author {
                    firstName
                    lastName
                }
            }
        }
        """

        james_corey = Author(first_name="James", last_name="Corey")
        james_corey.save()
        gerald_durrell = Author(first_name="Gerald", last_name="Durrell")
        gerald_durrell.save()

        Book(title="Leviathan Wakes", author=james_corey).save()
        Book(title="Caliban's War", author=james_corey).save()
        Book(title="The Bafut Beagles", author=gerald_durrell).save()
        Book(title="My Family and Other Animals", author=gerald_durrell).save()

    def test_all_books_works(self):
        """It should return them all!"""
        response = self.query(
            self.query_string,
            variables={},
        )
        decoded = json.loads(response.content)

        self.assertEqual(
            response.status_code,
            200,
            f"Unexpected status code for syntactically good query: {decoded}",
        )
        self.assertNotIn("error", decoded, f"Unexpected error in returned data")
        self.assertIn("data", decoded, f"No data in response!")
        self.assertIn("allBooks", decoded["data"], f"Returned data missing 'allBooks'")

        allBooks = decoded["data"]["allBooks"]
        self.assertEqual(len(allBooks), 4, f"Incorrect number of books returned!")
        # &c.

    class TestCreatBookWithExistingAuthor(GraphQLTestCase):
        GRAPHQL_SCHEMA = schema

        @classmethod
        def setUpClass(cls):
            super(TestCreatBookWithExistingAuthor, cls).setUpClass()
            cls.query_string = """
                mutation createBookWithExistingAuthor($title: String!, firstName: String!, lastName: String!) {
                    createBookWithExistingAuthor(title: $title, firstName: $firstName, lastName: $lastName) {
                        book {
                            title
                        }
                        author {
                            firstName
                            lastName
                        }
                    }
                }
                    """

            # now create the author we will be adding to
            Author(first_name="Robert", last_name="Martin").save()

        def test_create_book_with_existing_author_should_work(self) -> None:
            """When given correct parameters, the query should work"""
            query_variables = {
                "title": "Clean Code",
                "firstName": "Robert",
                "lastName": "Martin",
            }
            response = self.query(self.query_string, variables=query_variables)
            decoded = json.loads(response.content)

            self.assertIn("data", decoded, f"Response missing data: {decoded}")
            self.assertIn(
                "createBookWithExistingAuthor",
                decoded["data"],
                f"Returned data missing `createBooksWithExistingAuthor`: {decoded['data']}",
            )
            self.assertIn(
                "book",
                decoded["data"]["createBookWithExistingAuthor"],
                f"Returned data missing 'book': {decoded['data']['createBookWithExistingAuthor']}",
            )
            book = decoded["data"]["createBookWithExistingAuthor"]["book"]
            self.assertIn(
                "author",
                decoded["data"]["createBookWithExistingAuthor"],
                f"Returned data missing 'author': {decoded['data']['createBookWithExistingAuthor']}",
            )
            author = decoded["data"]["createBookWithExistingAuthor"]["author"]

            # now test that what was received is what was sent

            self.assertEqual(
                book,
                {"title": query_variables["title"]},
                f"Returned book was not what we expected: {query_variables}; {book}",
            )
            self.assertEqual(
                author,
                {
                    "first_name": query_variables["first_name"],
                    "last_name": query_variables["last_name"],
                },
                f"Returned author was not what was expected! {query_variables}; {author}",
            )

            # now test that what was created in the database is what we sent / received
            book_in_db = Book.objects.get(title=query_variables["title"])
            author_in_db = book_in_db.author

            self.assertEqual(
                book_in_db.title,
                book.title,
                f"Received book and that in the databse do not match! {book}; {book_in_db}",
            )
            self.assertEqual(
                author_in_db.first_name,
                author.first_name,
                f"First name of the received author and the one in the DB do not match: {author_in_db}; {author}",
            )
            self.assertEqual(
                author_in_db.last_name,
                author.last_name,
                f"First name of the received author and the one in the DB do not match: {author_in_db}; {author}",
            )
