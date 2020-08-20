from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('books', views.books),
    path('books/<int:book_id>', views.book_details),
    path('books/add', views.new_book),
    path('users/<int:user_id>', views.user_details),
]
