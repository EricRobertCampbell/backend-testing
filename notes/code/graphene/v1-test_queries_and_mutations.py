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
