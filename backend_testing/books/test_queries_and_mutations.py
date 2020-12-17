from graphene_django.utils.testing import GraphQLTestCase
import json

from books.models import Author, Book
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

    def setUp(self):
        gerald_durrell = Author(first_name="Gerald", last_name="Durrell")
        gerald_durrell.save()
        Book(title="My Family and Other Animals", author=gerald_durrell).save()
        Book(title="The Bafut Beagles", author=gerald_durrell).save()

    def test_it_works(self):
        """It should return all of the books"""
        response = self.query(self.query_string)
        decoded = json.loads(response.content)

        self.assertEqual(
            response.status_code,
            200,
            f"Unpexpected bad response to good query: {decoded}",
        )
