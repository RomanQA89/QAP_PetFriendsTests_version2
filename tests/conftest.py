from datetime import datetime
import pytest
from settings import valid_email, valid_password
from tests.test import pf


@pytest.fixture(autouse=True)
def get_key():
    # Отправляет запрос и сохраняет полученный ответ с кодом статуса в 'status', текст ответа в 'result'
    status, result = pf.get_api_key(valid_email, valid_password)
    # Проверка полученных данных
    assert status == 200
    assert 'key' in result
    return result


@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print(f"\nТест шел: {end_time - start_time}")


# @pytest.fixture(scope="class", autouse=True)
# def get_key():
#     # переменные email и password нужно заменить своими учетными данными
#     response = requests.post(url='https://petfriends.skillfactory.ru/login',
#                              data={"email": valid_email, "pass": valid_password})
#     assert response.status_code == 200, 'Запрос выполнен неуспешно'
#     assert 'Cookie' in response.request.headers, 'В запросе не передан ключ авторизации'
#     # print("\nreturn auth_key")
#     return response.request.headers.get('Cookie')
