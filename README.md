# Інструкції по запуску #

## Установка ##
* .Створіть віртуальне середовище: python -m venv env
* .Активуйте віртуальне середовище:
**Windows: .\env\Scripts\activate**
**MacOS / Linux: source env/bin/activate**
* Встановіть залежності: pip install -r requirements.txt

## Запуск застосунку ##
* Запустіть застосунок за допомогою Uvicorn:
**uvicorn app.main:app --reload**
*Відкрийте браузер і перейдіть за адресою http://localhost:8000/ для перевірки роботи застосунку.*

## Запуск тестів ##
* pytest