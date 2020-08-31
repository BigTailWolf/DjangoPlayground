from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('process/<str:option>', views.process),
    path('end', views.end),
    path('reset', views.reset),
]
