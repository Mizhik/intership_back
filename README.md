# Інструкції по запуску 

## Установка 
* Створіть віртуальне середовище: 

```bash
 pip install poetry
```
* Встановіть всі залежності:

```bash
poetry install
```

* Активуйте віртуальне середовище:

```bash
poetry shell
```



## Запуск застосунку 
* Запустіть застосунок за допомогою Uvicorn:
```bash
uvicorn app.main:app --reload
```
*Відкрийте браузер і перейдіть за адресою http://localhost:8000/ для перевірки роботи застосунку.*

## Запуск тестів 
* pytest

## Запуск програми у Docker

Цей проект можна запустити у Docker-контейнері для забезпечення консистентного середовища та простоти розгортання. Нижче наведено кроки для створення та запуску Docker-контейнера.

## Вимоги
Встановлений Docker на вашому комп'ютері. Інструкції щодо встановлення Docker можна знайти на офіційному сайті [Docker](https://docs.docker.com/engine/install/).

## Створення Docker-образу
Побудова Docker-образу

```bash
docker build -t example_name .
```

## Запуск Docker-контейнера
```bash
docker run -d -p 8000:8000 example_name
```