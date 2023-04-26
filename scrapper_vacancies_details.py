import json
import os
import requests
import time

# Получение перечня ранее созданных файлов со списком вакансий и их циклический перебор
for fl in os.listdir('./docs/pagination'):

    # Открытие файла, чтение содержимого, закрытие
    f = open('./docs/pagination/{}'.format(fl), encoding='utf8')
    jsonText = f.read()
    f.close()

    # Преобразование полученного текста в объект справочника
    jsonObj = json.loads(jsonText)

    # Получение и перебор списка вакансий
    for v in jsonObj['items']:
        # Обращение к API и получение детальной информации по конкретной вакансии
        req = requests.get(v['url'])
        data = req.content.decode()
        req.close()

        # Создание файла в формате json с идентификатором вакансии в качестве названия
        # Запись в данный файл ответа на запрос и закрытие
        fileName = './docs/vacancies/{}.json'.format(v['id'])
        f = open(fileName, mode='w', encoding='utf8')
        f.write(data)
        f.close()

        time.sleep(1)

print('Вакансии собраны')