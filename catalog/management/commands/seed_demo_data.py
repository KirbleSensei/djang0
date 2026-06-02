from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from catalog.models import Author, Book, BookCopy


class Command(BaseCommand):
    help = "Seed demo authors, books, copies, and a non-staff demo user."

    def handle(self, *args, **options):
        authors = {
            "George Orwell": "English novelist and essayist.",
            "J.K. Rowling": "British author of the Harry Potter series.",
            "Harper Lee": "American novelist known for To Kill a Mockingbird.",
            "F. Scott Fitzgerald": "American novelist of the Jazz Age.",
        }
        author_objects = {}
        for name, bio in authors.items():
            author, _ = Author.objects.update_or_create(name=name, defaults={"bio": bio})
            author_objects[name] = author

        books = [
            ("1984", "9780451524935", 1949, ["George Orwell"]),
            ("Animal Farm", "9780451526342", 1945, ["George Orwell"]),
            ("Harry Potter and the Sorcerer's Stone", "9780590353427", 1997, ["J.K. Rowling"]),
            ("Harry Potter and the Chamber of Secrets", "9780439064873", 1998, ["J.K. Rowling"]),
            ("To Kill a Mockingbird", "9780061120084", 1960, ["Harper Lee"]),
            ("The Great Gatsby", "9780743273565", 1925, ["F. Scott Fitzgerald"]),
        ]
        for title, isbn, year, author_names in books:
            book, _ = Book.objects.update_or_create(
                title=title,
                defaults={"isbn": isbn, "publication_year": year},
            )
            book.authors.set(author_objects[name] for name in author_names)
            prefix = "".join(ch for ch in title if ch.isalnum())[:3].upper()
            for number, condition in ((1, BookCopy.Condition.GOOD), (2, BookCopy.Condition.NEW)):
                BookCopy.objects.get_or_create(
                    copy_code=f"{prefix}{book.pk}-{number:03d}",
                    defaults={"book": book, "condition": condition},
                )

        User = get_user_model()
        demo_user, _ = User.objects.get_or_create(
            username="demo",
            defaults={"email": "demo@example.com"},
        )
        demo_user.set_password("demo12345")
        demo_user.is_staff = False
        demo_user.is_superuser = False
        demo_user.save()

        self.stdout.write(self.style.SUCCESS("Seeded demo data and demo user."))
