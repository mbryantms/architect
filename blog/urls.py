# URLconf
from django.urls import path
from blog.views import Index

from . import views

urlpatterns = [
    path('', Index.as_view()),
]