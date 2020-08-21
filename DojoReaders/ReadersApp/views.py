from django.shortcuts import render, redirect
from django.contrib import messages
from ReadersApp.models import User, Book, Author, Review
import bcrypt


def index(request):
    return render(request, 'index.html')


def books(request):
    user = User.objects.get(id = request.session['user_id'])

    recent_reviews = []

    for review in Review.objects.all().order_by('-created_at')[:3]:
        recent_reviews.append(review)

    context = {
        'user': user,
        'recent_reviews': recent_reviews,
        'all_books': Book.objects.all(),
    }
    return render(request, 'books.html', context)


def book_details(request, book_id):
    book = Book.objects.get(id=book_id)

    context = {
        'book': book,
    }
    return render(request, 'book_details.html', context)


def new_book(request):

    user = User.objects.get(id = request.session['user_id'])

    if request.method == 'POST':
        errors = {}
        print('Adding Book and reviews')
        book_errors = Book.objects.basic_validator(request.POST)
        if book_errors:
            errors.update(book_errors)

        author_errors = Author.objects.basic_validator(request.POST)
        if author_errors:
            errors.update(author_errors)
        
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        
        else:
            # Get or create author
            if request.POST['author_selection'] == '0':
                author = Author.objects.create(name=request.POST['author_name'])
            else:
                author = Author.objects.get(id=request.POST['author_selection'])
            
            book_created = Book.objects.create(
                title  = request.POST['book_title'],
                author = author
            )

            review_desc =  request.POST['user_review']
            if len(review_desc) > 0: # Need to create a review
                review = Review.objects.create(
                    desc = review_desc,
                    rate = request.POST['rating'],
                    user = user,
                    book = book_created,
                )

            return redirect(f'/books/{book_created.id}')


    context = {
        'user': user,
        'all_authors': Author.objects.all(),
    }
    return render(request, 'new_book.html', context)


def user_details(request, user_id):
    user = User.objects.get(id=user_id)
    reviews = user.reviews.all()
    count = len(reviews)
    books = []
    for review in reviews:
        if review.book not in books:
            books.append(review.book)

    context = {
        'user': user,
        'total_reviews': count,
        'books': books,
    }
    return render(request, 'user_details.html', context)


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    user_name   = request.POST['user_name']
    user_alias  = request.POST['user_alias']
    user_email  = request.POST['user_email']
    user_passwd = request.POST['user_passwd']
    passwd_hash = bcrypt.hashpw(user_passwd.encode(), bcrypt.gensalt()).decode()

    user = User.objects.create(
        name   = user_name,
        alias  = user_alias,
        email  = user_email,
        passwd = passwd_hash
    )
    request.session['user_id'] = user.id

    return redirect('/books')


def login(request):

    user = User.objects.filter(email=request.POST['login_email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['login_passwd'].encode(), logged_user.passwd.encode()):
            request.session['user_id'] = logged_user.id

            return redirect('/books')
    
    return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')


def submit_review(request):
    review_cmt = request.POST['user_review']
    book_id = request.POST['book_id']
    
    if len(review_cmt) > 0:
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.get(id=book_id)
        Review.objects.create(
            desc = review_cmt,
            rate = request.POST['rating'],
            user = user,
            book = book
        )

    return redirect(f'/books/{book_id}')


def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)
    book_id = review.book.id
    review.delete()
    
    return redirect(f'/books/{book_id}')
