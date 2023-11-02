from api import PetFriends
from settings import valid_email, valid_password
from settings import unvalid_email, unvalid_password
import pytest


pf = PetFriends()


"""Позитивные тесты."""


@pytest.mark.auth
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


@pytest.mark.api
def test_get_all_pets_with_valid_key(get_key, filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    status, result = pf.get_list_of_pets(get_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


@pytest.mark.api
def test_add_new_pet_with_valid_data(get_key, name='Барбос', animal_type='терьер',
                                         age='49', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Добавляем питомца
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


@pytest.mark.api
def test_successful_delete_self_pet(get_key):
    """Проверяем возможность удаления питомца"""

    # Получаем список своих питомцев
    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(get_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(get_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


@pytest.mark.api
def test_successful_update_self_pet_info(get_key, name='игорь', animal_type='кот', age=7):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем список своих питомцев
    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(get_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


@pytest.mark.api
def test_add_new_pet_with_valid_data_without_photo(get_key, name='Jeronimo', animal_type='supermen',
                                     age='77'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


@pytest.mark.api
def test_success_add_photo_of_pet(get_key, pet_photo='images/P1040103.jpg'):
    """Проверяем что можно успешно добавить фото питомца"""

    # Получаем список своих питомцев
    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Если список своих питомцев не пустой, то отправляем данные серверу
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_photo_of_pet(get_key, pet_id, pet_photo)

        # Проверяем что статус ответа равен 200 и в списке питомцев есть питомец с обновленным фото
        assert status == 200
        assert result['pet_photo'] == pet_photo
    else:
        raise Exception("There is no my pets")


"""Негативные тесты."""


@pytest.mark.auth
def test_get_api_key_with_unvalid_email(get_key, email=unvalid_email, password=valid_password):
    """Проверяем что запрос api ключа с невалидным email возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


@pytest.mark.auth
def test_get_api_key_with_unvalid_password(get_key, email=valid_email, password=unvalid_password):
    """Проверяем что запрос api ключа с невалидным паролем возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


@pytest.mark.api
def test_add_new_pet_with_unvalid_auth_key_without_photo(get_key, name='Tom', animal_type='dog',
                                     age='5'):
    """Проверяем добавление питомца без фото с некорректным auth_key на 403 статус"""

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo_with_unvalid_auth_key(get_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


@pytest.mark.api
@pytest.mark.skip(reason="Баг в продукте - <https://petfriends.skillfactory.ru/>")
def test_add_new_pet_without_photo_with_unvalid_name(get_key, name='MjIeBfj0TO7blscy5xZGbwahNOEVAcxkp37H98fHKoZJYnyErUJLimvC5Z6M0h4j34UkgDb0j9pOdITkGneP4S2uZP7NY5xqThxQbs4pMFhSt92qRDHhBYAGNuLvQfPLfwfkoFrO452M5OYtssJcpWJCbKDtUqXaWYFxwXcLt4uYYLMffuKeVtcbrR7oXG9s6QMpOEtBGgwziqEU3f1fr5XdEkAo0Nx6YoDejoBSTzSQIRkxffWh25u6yWC3Oyfr', animal_type='',
                                     age='6'):
    """Проверяем добавление питомца без фото с именем в 256 символов на 400 статус"""
    """Баг не воспроизводится так как нет ограничений на вводимые данные!"""

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


@pytest.mark.api
@pytest.mark.skip(reason="Баг в продукте - <https://petfriends.skillfactory.ru/>")
def test_add_new_pet_without_photo_with_unvalid_animal_type(get_key, name='Том', animal_type='MjIeBfj0TO7blscy5xZGbwahNOEVAcxkp37H98fHKoZJYnyErUJLimvC5Z6M0h4j34UkgDb0j9pOdITkGneP4S2uZP7NY5xqThxQbs4pMFhSt92qRDHhBYAGNuLvQfPLfwfkoFrO452M5OYtssJcpWJCbKDtUqXaWYFxwXcLt4uYYLMffuKeVtcbrR7oXG9s6QMpOEtBGgwziqEU3f1fr5XdEkAo0Nx6YoDejoBSTzSQIRkxffWh25u6yWC3Oyfr',
                                     age='6'):
    """Проверяем добавление питомца без фото с animal_type в 256 символов на 400 статус"""
    """Баг не воспроизводится так как нет ограничений на вводимые данные!"""

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


@pytest.mark.api
@pytest.mark.skip(reason="Баг в продукте - <https://petfriends.skillfactory.ru/>")
def test_add_new_pet_without_photo_with_unvalid_age(get_key, name='Том', animal_type='кот',
                                     age='-68689676'):
    """Проверяем добавление питомца без фото с отрицательным возрастом на 400 статус"""
    """Баг не воспроизводится так как нет ограничений на вводимые данные!"""

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


@pytest.mark.api
def test_unsuccessful_get_all_pets(get_key, filter=''):
    """ Проверяем что запрос всех питомцев с невалидным ключом будет иметь 403 статус."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets_with_unvalid_auth_key(auth_key, filter)

    assert status == 403


@pytest.mark.api
def test_unsuccessful_add_new_pet(get_key, name='Bil', animal_type='hen',
                                     age='9', pet_photo='images/cat1.jpg'):

    """Проверяем добавление питомца с невалидным ключом на 403 статус"""

    # Добавляем питомца
    status, result = pf.add_new_pet_with_incorrect_auth_key(get_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


@pytest.mark.api
def test_unsuccessful_add_photo_of_pet(get_key, pet_photo='images/P1040103.jpg'):
    """Проверка на 403 статус при добавлении фото питомца с невалидным ключом"""

    # Получаем список своих питомцев
    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Если список своих питомцев не пустой, то отправляем данные серверу
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_photo_of_pet_with_unvalid_auth_key(get_key, pet_id, pet_photo)

        # Проверяем что статус ответа равен 403
        assert status == 403


@pytest.mark.api
def test_unsuccessful_delete_self_pet_(get_key):
    """Проверка на 403 статус при невозможности удаления питомца"""

    # Получаем список своих питомцев
    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(get_key, "Суперкот", "кот", "2", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet_with_unvalid_auth_key(get_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Проверяем что статус ответа равен 403
    assert status == 403
