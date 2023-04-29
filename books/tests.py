import json
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from .models import Author, Book
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import date

class AuthorModelTestCase(TestCase):
    def setUp(self):
        self.first_name = "John"
        self.last_name = "Doe"
        self.birth_date = "1980-01-01"
        self.author = Author.objects.create(
            first_name=self.first_name,
            last_name=self.last_name,
            birth_date=self.birth_date
        )

    def test_author_model(self):
        self.assertEqual(self.author.first_name, self.first_name)
        self.assertEqual(self.author.last_name, self.last_name)
        self.assertEqual(str(self.author), self.first_name + " " + self.last_name)


class BookAPIViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Создаем автора книги
        self.author = Author.objects.create(
            first_name='Test',
            last_name='Author',
            birth_date="2023-01-01"
        )

        # Создаем книгу
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            description='Test description',
            pub_date="2023-01-01"
        )

    def test_get_book_list_unauthenticated(self):
        self.client.credentials()
        # Получаем URL для списка книг
        url = reverse("books:book-list")
        # Выполняем GET-запрос без аутентификации
        response = self.client.get(url)
        # Проверяем, что сервер вернул код 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_book_list_authenticated(self):
        # Получаем URL для списка книг
        url = reverse("books:book-list")
        # Добавляем в заголовок запроса токен аутентификации
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        # Выполняем GET-запрос с аутентификацией
        response = self.client.get(url)
        # Проверяем, что сервер вернул код 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что в ответе содержится созданная книга
        self.assertIn(self.book.title.encode(), response.content)

    def test_create_book_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    # Получаем URL для создания книги
        url = reverse("books:book-list")
        # Параметры создаваемой книги
        data = {
            "title": "New Book",
            "author": self.author.pk,
            "description": "New book description",
            "pub_date": "2023-01-01"
        }
        print(data)
        response = self.client.post(url, data)
        # Проверяем, что сервер вернул код 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверяем, что книга была создана
        self.assertTrue(Book.objects.filter(title=data['title']).exists())


    def test_create_book_unauthenticated(self):
        self.client.credentials()
    # Получаем URL для создания книги
        url = reverse("books:book-list")
        # Параметры создаваемой книги
        data = {
            "title": "New Book",
            "author": self.author.id,
            "description": "New book description",
            "pub_date": "2023-01-01"
        }
        # Выполняем POST-запрос без аутентификации
        response = self.client.post(url, data)
        # Проверяем, что сервер вернул код 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_unauthenticated(self):
        self.client.credentials()
        # Получаем URL для изменения книги
        url = reverse("books:book-detail", args=[self.book.pk])
        # Параметры изменяемой книги
        data = {
            "title": "Updated Book",
            "author": self.author.pk,
            "description": "Updated book description",
            "pub_date": "2023-02-01"
        }
        # Выполняем PUT-запрос без аутентификации
        response = self.client.put(url, data)
        # Проверяем, что сервер вернул код 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        # Получаем URL для редактирования книги
        url = reverse("books:book-detail", args=[self.book.id])
        # Добавляем в заголовок запроса токен аутентификации
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        # Создаем нового автора книги
        new_author = Author.objects.create(
            first_name='New',
            last_name='Author',
            birth_date=date(1980, 1, 1)
        )

        # Обновляем информацию о книге
        data = {
            'title': 'New Book Title',
            'author': new_author.id,
            'description': 'New Book Description',
            'pub_date': '2023-01-01'
        }
        response = self.client.put(url, data=data)

        # Проверяем, что сервер вернул код 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Обновляем информацию о книге в базе данных и получаем ее
        self.book.refresh_from_db()

        # Проверяем, что информация о книге была успешно обновлена
        self.assertEqual(self.book.title, data['title'])
        self.assertEqual(self.book.author, new_author)
        self.assertEqual(self.book.description, data['description'])
        self.assertEqual(self.book.pub_date, date.fromisoformat(data['pub_date']))

    def test_delete_book_unauthenticated(self):
        # Получаем URL для удаления книги
        self.client.credentials()
        url = reverse("books:book-detail", args=[self.book.id])
        # Выполняем DELETE-запрос без аутентификации
        response = self.client.delete(url)
        # Проверяем, что сервер вернул код 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated(self):
        # Получаем URL для удаления книги
        url = reverse("books:book-detail", args=[self.book.id])
        # Добавляем в заголовок запроса токен аутентификации
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        # Выполняем DELETE-запрос с аутентификацией
        response = self.client.delete(url)
        # Проверяем, что сервер вернул код 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Проверяем, что книга была удалена из базы данных
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

class AuthorViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.first_name = "John"
        self.last_name = "Doe"
        self.birth_date = "1980-01-01"
        self.author = Author.objects.create(
            first_name=self.first_name,
            last_name=self.last_name,
            birth_date=self.birth_date
        )

    def test_author_list_authenticated(self):
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_author_list_unauthenticated(self):
        self.client.credentials()
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_author_detail_authenticated(self):
        response = self.client.get('/api/authors/{}/'.format(self.author.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_author_authenticated(self):
        data = {'first_name': 'Jane', 'last_name': 'Doe', 'birth_date': '1990-01-01'}
        response = self.client.post('/api/authors/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_author_unauthenticated(self):
        self.client.credentials()
        data = {'first_name': 'Jane', 'last_name': 'Doe', 'birth_date': '1990-01-01'}
        response = self.client.post('/api/authors/', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
