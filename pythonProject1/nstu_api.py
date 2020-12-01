import requests
import json


class NSTU_API:
    def __init__(self, url='https://api.ciu.nstu.ru/v1.0/tgbot/', api_key='s13dfget456DADHGWEv34g435f'):
        self.url = url
        self.api_key = api_key

    def __getStudentID__(self, phone):
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
        return [self.__getStudentInfo__(id_hash['ID'], id_hash['HASH']) for id_hash in self.__getStudentID__(phone)]
