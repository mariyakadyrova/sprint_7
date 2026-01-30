import requests

def test_status_code():
    test_status_code = requests.get('https://qa-mesto.praktikum-services.ru/api/users/me',
                            headers={'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2OTBhMzU0ZDdlZTkyNzAwM2QyOGQ2ZmIiLCJpYXQiOjE3NjYwNDQ3NDksImV4cCI6MTc2NjY0OTU0OX0.uZNJhrEzA8D-6SucRucTIdlO6VO6nC5CV0ZXsZJqtHk'})
    assert test_status_code.status_code == 200