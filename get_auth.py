import requests

url = 'http://localhost:8000/api/token/'
data = {'username': 'a', 'password': 'a'}
response = requests.post(url, data=data)

api_url = 'http://localhost:8000/api/'
books_endpoint = 'books/'

if response.status_code == 200:
    token = response.json()['token']
    print(f'Token: {token}')
else:
    print('Invalid credentials')

# Добавляем токен в заголовок Authorization для отправки запросов к API
headers = {'Authorization': f'Token {token}'}

# Отправляем GET-запрос для получения списка книг
response = requests.get(f'{api_url}{books_endpoint}', headers=headers)

# Получаем список книг из ответа сервера
books = response.json()

print(books)
