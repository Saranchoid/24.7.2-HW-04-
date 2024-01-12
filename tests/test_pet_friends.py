from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_add_new_pet_simple_with_valid_data(
        name='Коржик',
        animal_type='агама',
        age='1'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_set_pet_photo(pet_photo='images\\agama1.jpg'):
    """Проверяем, что можно добавить фото к существующему питомцу без фото"""
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # указываем путь до фото
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo=pet_photo)


    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200


def test_add_new_pet_simple_invalid_content_type(
        name='Коржик',
        animal_type='агама',
        age='1'):
    """Проверяем что можно добавить питомца с телом JSON и content-type = XML"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, None, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


def test_add_new_pet_simple_invalid_animal_type(
        name='Коржик',
        animal_type='images\\agama1.jpg',
        age='1'):
    """Проверяем что можно передать фото в animal type вместо строки"""

    # указываем путь до фото
    pet_photo = os.path.join(os.path.dirname(__file__), animal_type)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, None, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 при попытке получить api с неверным логином и паролем """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


def test_add_new_pet_simple_with_empty_age_field(
        name='Фландерс',
        animal_type='кот',
        age=''):
    """Проверяем что можно добавить питомца с пустой строкой в разделе age"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_valid_data(name='Анна-Лиза-Мария Де Асуансьон', animal_type='жывтоне',
                                     age='100', pet_photo='images\\eto_foto_kota.txt'):
    """Проверяем что можно добавить питомца с текстовым файлом в разделе фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_set_pet_photo_txt_file(pet_photo='images\\eto_foto_kota.txt'):
    """Проверяем, что можно добавить текстовый файл в раздел фото к существующему питомцу без фото"""
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # указываем путь до фото
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][1]['id'], pet_photo=pet_photo)

def test_add_new_pet_simple_with_invalid_method(
        name='Коржик',
        animal_type='агама',
        age='1'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple_with_invalid_method(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 405


def test_get_all_pets_with_invalid_key(filter=''):

    auth_key = {"key": "123"}
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
