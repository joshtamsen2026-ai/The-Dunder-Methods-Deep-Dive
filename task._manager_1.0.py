import csv
import os
import platform
import subprocess
from datetime import datetime, timedelta


class Book:
    next_id = 1

    def __init__(self, title, author, year,
                 genre="General", pages=100):

        if not isinstance(year, int) or year <= 0:
            raise ValueError(
                "Year must be a positive integer."
            )

        if not isinstance(pages, int) or pages <= 0:
            raise ValueError(
                "Pages must be a positive integer."
            )

        self.book_id = f"BK-{Book.next_id:04d}"
        Book.next_id += 1

        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.pages = pages

        self.checked_out = False
        self.borrower = ""
        self.checkout_date = ""
        self.due_date = ""
        
    def check_out(self, borrower="Unknown User"):

        if self.checked_out:
            print(f'"{self.title}" is already checked out.')
            return

        self.checked_out = True
        self.borrower = borrower

        today = datetime.now()
        due = today + timedelta(days=14)

        self.checkout_date = today.strftime("%Y-%m-%d")
        self.due_date = due.strftime("%Y-%m-%d")

        print(
            f'"{self.title}" checked out by '
            f'{borrower}.'
        )

    def return_book(self):

        if not self.checked_out:
            print(f'"{self.title}" is already available.')
            return

        self.checked_out = False
        self.borrower = ""
        self.checkout_date = ""
        self.due_date = ""

        print(f'"{self.title}" returned successfully.')

    def is_overdue(self):

        if not self.checked_out:
            return False

        due = datetime.strptime(
            self.due_date,
            "%Y-%m-%d"
        ).date()

        return datetime.now().date() > due

    # -----------------------
    # Dunder Methods
    # -----------------------

    def __eq__(self, other):

        if not isinstance(other, Book):
            return False

        return (
            self.title.lower(),
            self.author.lower()
        ) == (
            other.title.lower(),
            other.author.lower()
        )

    def __lt__(self, other):

        return (
            self.title.lower()
            <
            other.title.lower()
        )

    def __len__(self):

        return self.pages

    def __contains__(self, keyword):

        return (
            keyword.lower()
            in self.title.lower()
        )

    def __repr__(self):

        status = (
            "Checked Out"
            if self.checked_out
            else "Available"
        )

        return (
            f"{self.book_id} | "
            f"{self.title} | "
            f"{self.author} | "
            f"{self.genre} | "
            f"{status}"
        )


class EBook(Book):

    next_id = 1

    def __init__(self,
                 title,
                 author,
                 year,
                 file_size_mb,
                 genre="Technology",
                 pages=100):

        super().__init__(
            title,
            author,
            year,
            genre,
            pages
        )

        self.book_id = f"EBK-{EBook.next_id:04d}"
        EBook.next_id += 1

        self.file_size_mb = file_size_mb
        self.checkout_count = 0

    @property
    def checked_out(self):
        return self.checkout_count > 0

    @checked_out.setter
    def checked_out(self, value):

        if not hasattr(
            self,
            "checkout_count"
        ):
            self.checkout_count = 0

    def check_out(self, borrower="Unknown User"):

        self.checkout_count += 1

        print(
            f'"{self.title}" checked out. '
            f'Active Users: '
            f'{self.checkout_count}'
        )

    def return_book(self):

        if self.checkout_count > 0:
            self.checkout_count -= 1

        print(
            f'"{self.title}" returned. '
            f'Active Users: '
            f'{self.checkout_count}'
        )

    def __repr__(self):

        return (
            f"{self.book_id} | "
            f"{self.title} | "
            f"{self.author} | "
            f"{self.genre} | "
            f"Users={self.checkout_count}"
        )


class Catalog:

    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def search_by_author(self, author):

        return [
            book
            for book in self.books
            if author.lower()
            in book.author.lower()
        ]

    def search_by_title(self, keyword):

        return [
            book
            for book in self.books
            if keyword.lower()
            in book.title.lower()
        ]

    def get_available(self):

        available = []

        for book in self.books:

            if isinstance(book, EBook):
                available.append(book)

            elif not book.checked_out:
                available.append(book)

        return available

    def summary(self):

        print("\n" + "=" * 60)
        print("LIBRARY SUMMARY")
        print("=" * 60)

        print(
            f"Total Books: {len(self.books)}"
        )

        print(
            f"Available Books: "
            f"{len(self.get_available())}"
        )

        print("\nCatalog Contents:")

        for book in self.books:
            print(book)

        print("=" * 60)

    def export_to_csv(
        self,
        filename="Library_Report.csv"
    ):

        export_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        total_pages = sum(
            book.pages
            for book in self.books
        )

        genres = {}

        for book in self.books:

            genres[book.genre] = (
                genres.get(
                    book.genre,
                    0
                )
                + 1
            )

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(
                ["LIBRARY MANAGEMENT REPORT"]
            )

            writer.writerow(
                ["Generated",
                 export_time]
            )

            writer.writerow([])
            writer.writerow([])

            writer.writerow(
                ["EXECUTIVE SUMMARY"]
            )

            writer.writerow(
                ["Metric", "Value"]
            )

            writer.writerow(
                ["Total Items",
                 len(self.books)]
            )

            writer.writerow(
                ["Total Pages",
                 total_pages]
            )

            writer.writerow([])
            writer.writerow([])

            writer.writerow(
                ["GENRE BREAKDOWN"]
            )

            writer.writerow(
                ["Genre", "Count"]
            )

            for genre, count in genres.items():

                writer.writerow([
                    genre,
                    count
                ])

            writer.writerow([])
            writer.writerow([])

            writer.writerow(
                ["COMPLETE INVENTORY"]
            )

            writer.writerow([
                "Library ID",
                "Type",
                "Title",
                "Author",
                "Genre",
                "Pages",
                "Year",
                "Status",
                "Borrower",
                "Checkout Date",
                "Due Date",
                "Overdue",
                "File Size(MB)",
                "Users"
            ])

            for book in self.books:

                if isinstance(book, EBook):

                    writer.writerow([
                        book.book_id,
                        "EBook",
                        book.title,
                        book.author,
                        book.genre,
                        book.pages,
                        book.year,
                        "Multi User",
                        "",
                        "",
                        "",
                        "",
                        book.file_size_mb,
                        book.checkout_count
                    ])

                else:

                    writer.writerow([
                        book.book_id,
                        "Physical",
                        book.title,
                        book.author,
                        book.genre,
                        book.pages,
                        book.year,
                        (
                            "Checked Out"
                            if book.checked_out
                            else "Available"
                        ),
                        book.borrower,
                        book.checkout_date,
                        book.due_date,
                        (
                            "YES"
                            if book.is_overdue()
                            else "NO"
                        ),
                        "",
                        ""
                    ])

        print(
            f"\nReport exported: "
            f"{filename}"
        )

        try:

            if platform.system() == "Windows":
                os.startfile(filename)

            elif platform.system() == "Darwin":
                subprocess.run(
                    ["open", filename]
                )

            else:
                subprocess.run(
                    ["xdg-open", filename]
                )

        except Exception:
            pass


# =================================================
# TESTING
# =================================================

catalog = Catalog()

catalog.add_book(
    Book(
        "Python Crash Course",
        "Eric Matthes",
        2019,
        "Programming",
        544
    )
)

catalog.add_book(
    Book(
        "Clean Code",
        "Robert Martin",
        2008,
        "Programming",
        464
    )
)

catalog.add_book(
    Book(
        "Spacebound",
        "Lambert Martin",
        2008,
        "Science Fiction",
        385
    )
)

catalog.add_book(
    EBook(
        "AI Engineering",
        "Chip Huyen",
        2025,
        15.2,
        "Artificial Intelligence",
        350
    )
)

catalog.add_book(Book("The Silent Forest", "Emma Carter", 2010, "Fiction", 320))
catalog.add_book(Book("Python Fundamentals", "Mark Benson", 2020, "Programming", 450))
catalog.add_book(Book("Ocean of Dreams", "Sophia Reed", 2012, "Adventure", 288))
catalog.add_book(Book("The Last Kingdom", "Henry Clarke", 2008, "Historical Fiction", 410))
catalog.add_book(Book("Data Structures Explained", "Robert Lewis", 2018, "Programming", 530))
catalog.add_book(Book("Celestial Journey", "Liam Brooks", 2015, "Science Fiction", 375))
catalog.add_book(Book("Artificial Intelligence Essentials", "Grace Kim", 2024, "Artificial Intelligence", 490))
catalog.add_book(Book("Mountain Echoes", "Lucas White", 2011, "Adventure", 340))
catalog.add_book(Book("Mastering Algorithms", "Sarah Wilson", 2019, "Programming", 610))
catalog.add_book(Book("The Hidden Path", "Ava Green", 2007, "Fantasy", 390))
catalog.add_book(Book("Cybersecurity Basics", "Ethan Hall", 2023, "Cybersecurity", 420))
catalog.add_book(Book("Stars Beyond", "Olivia Scott", 2021, "Science Fiction", 350))
catalog.add_book(Book("The River's Secret", "Noah Baker", 2014, "Mystery", 295))
catalog.add_book(Book("Deep Learning Simplified", "Andrew Fisher", 2022, "Artificial Intelligence", 560))
catalog.add_book(Book("Code Like a Pro", "Nathan Adams", 2017, "Programming", 510))
catalog.add_book(Book("The Crystal Tower", "Emily Turner", 2009, "Fantasy", 450))
catalog.add_book(Book("Business Leadership", "James Cooper", 2016, "Business", 330))
catalog.add_book(Book("Journey to Mars", "Aiden Mitchell", 2013, "Science Fiction", 370))
catalog.add_book(Book("The Midnight Puzzle", "Ella Morris", 2020, "Mystery", 310))
catalog.add_book(Book("Clean Architecture", "Robert Martin", 2017, "Software Engineering", 432))
catalog.add_book(Book("Cloud Computing Guide", "Michael Ross", 2021, "Technology", 540))
catalog.add_book(Book("The Forgotten Gate", "Chloe Hughes", 2012, "Fantasy", 402))
catalog.add_book(Book("Digital Marketing Today", "Sophia Walker", 2018, "Business", 305))
catalog.add_book(Book("Quantum Discoveries", "Benjamin King", 2023, "Science", 475))
catalog.add_book(Book("The Lost Expedition", "Daniel Young", 2010, "Adventure", 365))
catalog.add_book(Book("Network Security", "Matthew Allen", 2022, "Cybersecurity", 490))
catalog.add_book(Book("Secrets of the Sea", "Victoria Perez", 2015, "Adventure", 340))
catalog.add_book(Book("Advanced Python Programming", "David Hill", 2024, "Programming", 680))
catalog.add_book(Book("Beyond the Horizon", "Samantha Flores", 2019, "Fiction", 298))
catalog.add_book(Book("Machine Learning Mastery", "Andrew Jones", 2023, "Artificial Intelligence", 590))
catalog.add_book(Book("The Iron Throne", "Ryan Edwards", 2006, "Fantasy", 520))
catalog.add_book(Book("Modern Web Development", "Kevin Murphy", 2021, "Programming", 615))
catalog.add_book(Book("Hidden Treasures", "Natalie Rogers", 2017, "Adventure", 280))
catalog.add_book(Book("Enterprise Systems", "William Cook", 2018, "Technology", 455))
catalog.add_book(Book("The Secret Chamber", "Jessica Bell", 2011, "Mystery", 335))
catalog.add_book(Book("AI Engineering in Practice", "Chip Huyen", 2025, "Artificial Intelligence", 520))
catalog.add_book(Book("Legends of Avalon", "Christopher Ward", 2014, "Fantasy", 430))
catalog.add_book(Book("Cryptography Essentials", "Andrew Reed", 2022, "Cybersecurity", 410))
catalog.add_book(Book("Data Analytics Handbook", "Rebecca Evans", 2020, "Technology", 495))
catalog.add_book(Book("The Silver Ship", "Hannah Turner", 2016, "Science Fiction", 360))
catalog.add_book(Book("Programming Logic", "Anthony Ortiz", 2019, "Programming", 470))
catalog.add_book(Book("The Emerald Crown", "Megan Rivera", 2008, "Fantasy", 405))
catalog.add_book(Book("Startup Strategy", "Aaron Campbell", 2013, "Business", 300))
catalog.add_book(Book("Artificial Minds", "Dylan Collins", 2021, "Artificial Intelligence", 540))
catalog.add_book(Book("The Desert Code", "Lauren Stewart", 2017, "Mystery", 285))
catalog.add_book(Book("Refactoring Techniques", "Martin Fowler", 2018, "Software Engineering", 560))
catalog.add_book(Book("JavaScript Masterclass", "Justin Gray", 2024, "Programming", 620))
catalog.add_book(Book("The Sapphire Quest", "Abigail Howard", 2015, "Adventure", 375))
catalog.add_book(Book("The Hidden Algorithm", "Gabriel Diaz", 2020, "Technology", 440))
catalog.add_book(Book("Infinite Worlds", "Logan Price", 2012, "Science Fiction", 390))
catalog.add_book(Book("Database Systems", "Mia Richardson", 2023, "Technology", 570))
catalog.add_book(Book("Mystery Manor", "Zoe Cox", 2009, "Mystery", 315))
catalog.add_book(Book("The Ruby Dragon", "Elijah Bailey", 2014, "Fantasy", 460))
catalog.add_book(Book("Financial Intelligence", "Sophia Peterson", 2021, "Business", 325))
catalog.add_book(Book("Practical Neural Networks", "Lily Ward", 2024, "Artificial Intelligence", 620))
catalog.add_book(Book("The Northern Lights", "Jack Cooper", 2018, "Adventure", 350))
catalog.add_book(Book("Python Design Patterns", "Ethan Reed", 2020, "Programming", 510))
catalog.add_book(Book("Guardians of Earth", "Grace Morgan", 2013, "Science Fiction", 385))
catalog.add_book(Book("The Hidden Cipher", "Avery Bell", 2022, "Cybersecurity", 435))
catalog.add_book(Book("Leadership Principles", "Thomas Howard", 2019, "Business", 295))
catalog.add_book(Book("The Golden Compass", "Madison Murphy", 2010, "Adventure", 370))
catalog.add_book(Book("Software Testing Guide", "Christopher Ross", 2017, "Software Engineering", 475))
catalog.add_book(Book("Artificial Intelligence Ethics", "Emma Foster", 2024, "Artificial Intelligence", 410))
catalog.add_book(Book("The Crystal Cavern", "Owen Rogers", 2011, "Fantasy", 425))
catalog.add_book(Book("Data Visualization", "Charlotte Jenkins", 2022, "Technology", 530))
catalog.add_book(Book("Moon Colony", "Mason Sanders", 2015, "Science Fiction", 355))
catalog.add_book(Book("Cloud Native Apps", "Harper Bennett", 2023, "Technology", 605))
catalog.add_book(Book("Programming Challenges", "Leo Barnes", 2016, "Programming", 490))
catalog.add_book(Book("The Shadow Key", "Ella Henderson", 2014, "Mystery", 310))
catalog.add_book(Book("Big Data Analytics", "Samuel Powell", 2021, "Technology", 575))
catalog.add_book(Book("The Dragon Empire", "Scarlett Hughes", 2012, "Fantasy", 480))
catalog.add_book(Book("Cyber Defense Strategies", "Caleb Richardson", 2025, "Cybersecurity", 520))
catalog.add_book(Book("Journey Through Time", "Layla Coleman", 2019, "Science Fiction", 395))
catalog.add_book(Book("Practical DevOps", "Isaac Perry", 2020, "Technology", 545))
catalog.add_book(Book("The Emerald Forest", "Victoria Long", 2007, "Adventure", 340))
catalog.add_book(Book("AI for Business", "Julian Patterson", 2024, "Artificial Intelligence", 505))
catalog.add_book(Book("The Clockmaker", "Paisley Hughes", 2013, "Mystery", 280))
catalog.add_book(Book("Full Stack Development", "Dominic Russell", 2022, "Programming", 650))
catalog.add_book(Book("The King's Legacy", "Mila Simmons", 2009, "Fantasy", 450))
catalog.add_book(Book("Modern Networking", "John Foster", 2021, "Technology", 485))
catalog.add_book(Book("Secrets of Innovation", "Aubrey Ward", 2018, "Business", 330))
catalog.add_book(Book("The Infinite Machine", "Wyatt Griffin", 2024, "Science Fiction", 410))
catalog.add_book(Book("Practical Cybersecurity", "Eleanor Hayes", 2023, "Cybersecurity", 460))
catalog.add_book(Book("The Hidden Temple", "Luke Bennett", 2012, "Adventure", 375))
catalog.add_book(Book("Machine Learning Applications", "Claire Reynolds", 2025, "Artificial Intelligence", 630))
catalog.add_book(Book("Programming Paradigms", "Nathaniel Scott", 2017, "Programming", 515))
catalog.add_book(Book("Castle of Shadows", "Stella Bell", 2011, "Fantasy", 405))
catalog.add_book(Book("Data Engineering Blueprint", "Joshua Morgan", 2024, "Technology", 590))
catalog.add_book(Book("The Secret Island", "Riley Howard", 2010, "Adventure", 365))
catalog.add_book(Book("Business Transformation", "Leah Diaz", 2020, "Business", 315))
catalog.add_book(Book("Neural Network Design", "Carter James", 2025, "Artificial Intelligence", 675))
catalog.add_book(Book("Lost in the Stars", "Brooklyn Murphy", 2016, "Science Fiction", 345))
catalog.add_book(Book("Modern Software Design", "Adam Turner", 2023, "Software Engineering", 540))
catalog.add_book(Book("The Ancient Scroll", "Penelope Cooper", 2008, "Mystery", 295))
catalog.add_book(Book("Future Technologies", "Jason White", 2026, "Technology", 605))
catalog.add_book(Book("The Warrior's Path", "Savannah Brooks", 2014, "Fantasy", 435))
catalog.add_book(Book("Advanced Cloud Architecture", "Brian Hall", 2025, "Technology", 720))
catalog.add_book(Book("The Forgotten Realm", "Zoey Edwards", 2013, "Fantasy", 470))


# -------------------------
# Search Tests
# -------------------------

print("\nTITLE SEARCH:")
results = catalog.search_by_title(
    "python"
)
print(results)

print("\nAUTHOR SEARCH:")
print(
    catalog.search_by_author(
        "Martin"
    )
)

# -------------------------
# Checkout Tests
# -------------------------

catalog.books[0].check_out(
    "John Smith"
)

ebook = next(
    book
    for book in catalog.books
    if isinstance(book, EBook)
)

ebook.check_out()
ebook.check_out()
ebook.check_out()

# -------------------------
# Dunder Tests
# -------------------------

print("\nEQUALITY TEST")

book1 = Book(
    "Python Crash Course",
    "Eric Matthes",
    2019,
    "Programming",
    544
)

book2 = Book(
    "Python Crash Course",
    "Eric Matthes",
    2025,
    "Programming",
    600
)

print(book1 == book2)

print("\nLEN TEST")
print(len(book1))

print("\nCONTAINS TEST")
print("Python" in book1)
print("Java" in book1)

print("\nSORTING TEST")

books = [
    Book(
        "Zoo Adventures",
        "Alice Smith",
        2018,
        "Adventure",
        300
    ),
    Book(
        "AI Engineering",
        "Chip Huyen",
        2025,
        "Technology",
        350
    ),
    Book(
        "Clean Code",
        "Robert Martin",
        2008,
        "Programming",
        464
    )
]

sorted_books = sorted(books)

for book in sorted_books:
    print(book.title)

catalog.summary()

catalog.export_to_csv()