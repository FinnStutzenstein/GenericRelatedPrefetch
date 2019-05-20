import sys

from django.apps import AppConfig
from django.db import DEFAULT_DB_ALIAS, connections
from django.test.utils import CaptureQueriesContext



class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        # ignore migrates etc.
        if sys.argv[1] != "runserver":
            return

        print("\nMain app ready!")

        from main.models import Tag, Book, CD

        N = 1

        # Create objects: one book, one cd and a tag for each of these.
        Book.objects.all().delete()
        for i in range(N):
            Book.objects.create(name=f"Book{i}")

        CD.objects.all().delete()
        for i in range(N):
            CD.objects.create(name=f"CD{i}")

        Tag.objects.all().delete()
        for i in range(N):
            book = Book.objects.get(name=f"Book{i}")
            t = Tag(content_object=book, name=f"Tag to book{i}")
            t.save()
            cd = CD.objects.get(name=f"CD{i}")
            t = Tag(content_object=cd, name=f"Tag to cd{i}")
            t.save()

        context = CaptureQueriesContext(connections[DEFAULT_DB_ALIAS])
        with context:
            # Get all tags. Prefetch the content objects and the related tags for
            # the content objects. This is needed, so the following code makes
            # a constant amount of 4 queries:
            # - 1 request: get all books
            # - 1 request: get all tags
            # - 2 requests: get all tags (twice??)
            # You can try to adjust N above (e.g. N=10), and the amount of queries
            # should not change.
            prefetched_queryset = Tag.objects.prefetch_related("content_object", "content_object__tags")

            for tag in prefetched_queryset.all():
                print(f"Got '{tag}':\n\t-the content object: {tag.content_object}"
                    f"\n\t-the content objects tag (should be the same as '{tag}'!):"
                    f"{tag.content_object.tag}")

        queries = "\n".join(
            f"{i}. {query['sql']}"
            for i, query in enumerate(context.captured_queries, start=1)
        )
        print(f"{len(context)} queries executed\nCaptured queries were:\n{queries}")
