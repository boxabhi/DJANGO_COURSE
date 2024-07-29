from django.db.models import Avg

# Average price of books
average_price = Book.objects.aggregate(average=Avg('price'))
print(average_price)  # Output: {'average': 15.75} (example output)





from django.db.models import Count

# Annotate each author with the total number of books
authors_with_book_count = Author.objects.annotate(total_books=Count('book'))

for author in authors_with_book_count:
    print(f"Author: {author.name}, Total Books: {author.total_books}")



from django.db.models import Avg

# Annotate each author with the average price of their books
authors_with_avg_price = Author.objects.annotate(avg_price=Avg('book__price'))

for author in authors_with_avg_price:
    print(f"Author: {author.name}, Average Book Price: {author.avg_price}")



authors_with_many_books = Author.objects.annotate(
    total_books=Count('book')).filter(total_books__gt=3)

for author in authors_with_many_books:
    print(f"Author: {author.name}, Total Books: {author.total_books}")





from django.db.models import Count, Q

# Annotate each author with the total number of books published in 2023
authors_with_books_2023 = Author.objects.annotate(
    books_2023=Count('book', filter=Q(book__published_date__year=2023))
)

for author in authors_with_books_2023:
    print(f"Author: {author.name}, Books Published in 2023: {author.books_2023}")





from django.db.models import Count, Avg

# Annotate each author with both the total number of books and the average price of their books
authors_with_stats = Author.objects.annotate(
    total_books=Count('book'), avg_price=Avg('book__price'))

for author in authors_with_stats:
    print(f"Author: {author.name}, Total Books: {author.total_books}, Average Book Price: {author.avg_price}")









https://chatgpt.com/c/bc6206d7-a54b-4c26-8d58-fd7a6ba19dbe