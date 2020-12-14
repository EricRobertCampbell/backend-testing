import graphene
from graphene_django import DjangoObjectType
from books.models import Book, Author
from books.utility import add_book_to_existing_author, add_book_with_author


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("title", "author")


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ("first_name", "last_name")


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    all_books = graphene.List(BookType)
    all_authors = graphene.List(AuthorType)

    def resolve_all_books(root, info):
        return Book.objects.all()

    def resolve_all_authors(root, info):
        return Author.objects.all()


# mutations
class CreateBookWithExistingAuthorMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    book = graphene.Field(BookType)
    author = graphene.Field(AuthorType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        title = kwargs.get("title")
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        [book, author] = add_book_to_existing_author(title, first_name, last_name)
        return CreateBookWithExistingAuthorMutation(book=book, author=author)


class CreateBookWithNewAuthorMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    book = graphene.Field(BookType)
    author = graphene.Field(AuthorType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        title = kwargs.get("title")
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        [book, author] = add_book_with_author(title, first_name, last_name)
        return CreateBookWithNewAuthorMutation(book=book, author=author)


class Mutation(graphene.ObjectType):
    create_book_with_existing_author = CreateBookWithExistingAuthorMutation.Field()
    create_book_with_new_author = CreateBookWithNewAuthorMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
