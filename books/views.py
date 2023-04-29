from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthorSerializer

class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthorSerializer

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = BookSerializer

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = BookSerializer
