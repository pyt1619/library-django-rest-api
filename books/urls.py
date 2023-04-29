from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import AuthorList, AuthorDetail, BookList, BookDetail
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'books'


urlpatterns = [
    path('authors/', AuthorList.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetail.as_view(), name='author-detail'),
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('token/', obtain_auth_token, name='api-token-auth'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
