import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import textwrap
def wrap_labels(ax, width, break_long_words=False): # создание меток
    labels = []
    for label in ax.get_xticklabels():
        text = label.get_text()
        labels.append(textwrap.fill(text, width=width,
                      break_long_words=break_long_words))
    ax.set_xticklabels(labels, rotation=0)
def createBarChart(ds, name): #создание гистограммы
    fig, ax = plt.subplots()

    plt.legend(loc='best')

    ds.plot.bar(rot=0)
    wrap_labels(ax, 10)

    image_format = 'svg'
    image_name = name + '.svg'
    plt.savefig(image_name, format=image_format, dpi=1200, bbox_inches="tight")
    plt.close(fig)
def createPieChart(labels, sizes, name): #создание круговой диаграммы
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.5f%%')
    plt.legend(loc='best')

    image_format = 'svg'
    image_name = name + '.svg'
    plt.savefig(image_name, format=image_format, dpi=1200, bbox_inches="tight")
    plt.close(fig)

# Создание списков для столбцов таблицы vacancies
IDs = []  # Список идентификаторов вакансий
names = []  # Список наименований вакансий
descriptions = []  # Список описаний вакансий
allow_messages_flags = []
cities = []
employments = []

# Создание списков для столбцов таблицы skills
skills_vac = []  # Список идентификаторов вакансий
skills_name = []  # Список названий навыков

# В выводе будет отображаться прогресс
# Для этого узнаем общее количество файлов, которые надо обработать
# Счетчик обработанных файлов установим в ноль
cnt_docs = len(os.listdir('./docs/vacancies'))
i = 0

# Перебор всех файлов в папке vacancies
for fl in os.listdir('./docs/vacancies'):

    # Открытие, чтение и закрытие файла
    f = open('./docs/vacancies/{}'.format(fl), encoding='utf8')
    jsonText = f.read()
    f.close()

    # Перевод текста файла в справочник
    jsonObj = json.loads(jsonText)

    # Заполнение списков для таблиц
    IDs.append(jsonObj['id'])
    names.append(jsonObj['name'])
    descriptions.append(jsonObj['description'])
    allow_messages_flags.append(jsonObj['allow_messages'])

    if (jsonObj['area']['name'] is None):
        cities.append('Не указано')
    else:
        cities.append(jsonObj['area']['name'])


    #cities.append(jsonObj['address']['city'])
    if (jsonObj['employment']['name'] is None):
        employments.append('Не указано')
    else:
        employments.append(jsonObj['employment']['name'])
    # Т.к. навыки хранятся в виде массива, то проходимся по нему циклом
    for skl in jsonObj['key_skills']:
        skills_vac.append(jsonObj['id'])
        skills_name.append(skl['name'])

    # Увеличение счетчика обработанных файлов на 1, очистка вывода ячейки и вывод прогресса
    i += 1

# Создание датафрейма, который затем сохраняем в БД в таблицу vacancies
df = pd.DataFrame({'id': IDs, 'name': names, 'description': descriptions, 'city':cities, 'employment': employments,
                   'allow': allow_messages_flags})
ds = df.groupby('name')['id'].count().sort_values(ascending=False).head(5)
createBarChart(ds,'vacancy')

ds = df.groupby('city')['id'].count().sort_values(ascending=False).head(5)
createBarChart(ds,'city')

ds = df.groupby('employment')['id'].count().sort_values(ascending=False).head(5)
createBarChart(ds,'employments')

#создание круговой диаграммы по закрыты/открыты сообщения работадателю
labels = ['Закрыты сообщения', 'Открыты сообщения']

sizes = [df[df['allow'] == True]['id'].count(), df[df['allow'] == False]['id'].count()]
createPieChart(labels, sizes, 'Closed_private_messages')

df = pd.DataFrame({'vacancy': skills_vac, 'skill': skills_name})
ds = df.groupby('skill')['vacancy'].count().sort_values(ascending=False).head(5)
createBarChart(ds,'skill')

print(ds)