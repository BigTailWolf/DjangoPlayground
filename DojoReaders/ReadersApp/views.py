from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def books(request):
    return render(request, 'books.html')

def book_details(request, book_id):
    return render(request, 'book_details.html')

def new_book(request):
    return render(request, 'new_book.html')

def user_details(request, user_id):
    return render(request, 'user_details.html')