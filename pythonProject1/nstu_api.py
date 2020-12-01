import requests
import json


class NSTU_API:
    def __init__(self, url='https://api.ciu.nstu.ru/v1.0/tgbot/', api_key='s13dfget456DADHGWEv34g435f'):
        """Конструктор.

        url -- Адрес, по которому будет обращение к API НГТУ
        api_key -- Ключ для аутентификации запросов
        """

        if not url.endswith('/'):
            url += '/'
        self.url = url
        self.api_key = api_key

    def __getStudentID__(self, phone):
        """Получить id и хэш студента по его номеру телефона. Возвращает список словарей с полями `ID` и `HASH`.

        phone -- Телефонный номер студента, указанный в его личном кабинете
        """

        headers = {
            'Content-Type': 'application/json',
            'Http-Api-Key': self.api_key,
        }
        params = {
            'phone_number': phone,
        }
        endpoint = self.url + 'check_stud_phone'
        response = requests.get(endpoint, headers=headers, params=params)
        if response.ok:
            return json.loads(response.text)
        else:
            raise requests.exceptions.HTTPError(response)

    def __getStudentInfo__(self, id, hash):
        """Получить основную информацию о студенте по его `id` и `hash`.
        Получить их можно методом `__getStudentID__`.
        Возвращает список словарей с полями `STATUS`, `FIO`, `FORM`, `BASIS`"""

        headers = {
            'Content-Type': 'application/json',
            'Http-Api-Key': self.api_key
        }
        params = {
            'id': id,
            'hash': hash,
        }
        endpoint = self.url + 'stud_status'
        response = requests.get(endpoint, headers=headers, params=params)
        if response.ok:
            return json.loads(response.text)
        else:
            raise requests.exceptions.HTTPError(response)

    def getStudentInfo(self, phone):
        """Получить основную информацию о студенте по его номеру телефона.
        Возвращает список словарей с полями `STATUS`, `FIO`, `FORM`, `BASIS`.

        phone -- Телефонный номер студента, указанный в его личном кабинете
        """

        result = []
        for id_hash in self.__getStudentID__(phone):
            for info in self.__getStudentInfo__(id_hash['ID'], id_hash['HASH']):
                result.append(info)
        return result
