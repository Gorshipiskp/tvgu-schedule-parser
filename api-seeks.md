# Эндпоинты сайта ТвГУ и полезные страницы

## Ключ
- **UR** – Неопознанное предназначение  
- **AF** – API без необходимости авторизации (Auth Free)  
- **NeA** – API с необходимостью авторизации (Need Auth, JWT)

---

## Публичные эндпоинты (AF – Auth Free)

### Точка AF-1
`https://tversu.ru/calendars?year=2025&month=10&with_years=true`  
Выдаёт новости по дням  
**Аргументы:**  
- `year` – текущий год отсчёта  
- `month` – номер месяца (0 = январь)  
- `with_years` – назначение не выяснено

### Точка AF-2
`https://abiturient.tversu.ru/api/catalog/level-categories`  
Формы обучения с ID, названием и дополнительной информацией (`budgetTotal`, `paidTotal`)

### Точка AF-3
`https://abiturient.tversu.ru/api/catalog/sources`  
Типы мест на направлениях (Целевая квота, совмещённая квота, по договору, бюджетные места и т.д.) с их ID, сокращениями названий и порядком сортировки

### Точка AF-4
`https://abiturient.tversu.ru/api/departments`  
Возвращает название университета и его ID

### Точка AF-5
`https://abiturient.tversu.ru/api/catalog/forms`  
Формы обучения

### Точка AF-6
`https://abiturient.tversu.ru/api/freports/screen/1/2/1`  
HTML-страница экрана подачи заявлений. Числа в конце, видимо, влияют на фильтрацию и сортировку, либо указывают на форму обучения и т.п.

### Точка AF-7
`https://abiturient.tversu.ru/api/freports/list/{DIRECTION}/{TYPE}/{LEVEL}`  
HTML-страница списка подавших документы  
**Аргументы:**  
- `DIRECTION` – ID направления  
- `TYPE` – ID типа места  
- `LEVEL` – уровень обучения (бакалавриат, магистратура, аспирантура)  

> Замечание: направления с разными формами обучения считаются различными

### Точка AF-8
`https://abiturient.tversu.ru/api/specialties/get/{DIRECTION}`  
Информация о направлении по его ID

### Точка AF-9
`https://abiturient.tversu.ru/api/catalog/current-date`  
Текущее время в ISO-8601 формате

### Точка AF-10
`https://abiturient.tversu.ru/api/catalog/nationality`  
Список национальностей

### Точка AF-11
`https://abiturient.tversu.ru/api/catalog/education-types`  
Список типов образования (высшее, среднее и т.д.)

### Точка AF-12
`https://abiturient.tversu.ru/api/catalog/languages`  
Список языков

### Точка AF-13
`https://abiturient.tversu.ru/api/catalog/disciplines`  
Список дисциплин, учитываемых при поступлении

### Точка AF-14
`https://abiturient.tversu.ru/api/catalog/school-types`  
Список типов образовательных учреждений (школа, гимназия, институт и т.д.)

### Точка AF-15
`https://abiturient.tversu.ru/api/catalog/faculties`  
Список факультетов без подробной информации

### Точка AF-16
`https://abiturient.tversu.ru/api/catalog/reference/{NUM}`  
Список справочной информации в зависимости от `NUM` (например, тип родства, уровень знания языка)

### Точка AF-17
`https://abiturient.tversu.ru/api/catalog/epgu-reasons`  
Список причин отказа от Госуслуг (ЕГПУ)

### Точка AF-18
`https://abiturient.tversu.ru/api/catalog/payment-types`  
Список способов оплаты обучения

### Точка AF-19
`https://abiturient.tversu.ru/api/catalog/contract-statuses`  
Список состояний договоров

### Точка AF-20
`https://abiturient.tversu.ru/api/catalog/ege`  
Список предметов ЕГЭ

### Точка AF-21
`https://abiturient.tversu.ru/api/catalog/regions`  
Список регионов (только СНГ и ЮФО)

### Точка AF-22 **UR**
`https://abiturient.tversu.ru/api/catalog/divisions`  

### Точка AF-23
`https://abiturient.tversu.ru/api/catalog/benefits`  
Список преимуществ при поступлении (инвалиды, сироты, ветераны и т.д.)

### Точка AF-24
`https://abiturient.tversu.ru/api/catalog/test-types`  
Список типов результатов при поступлении (ЕГЭ, собеседование, внутренние экзамены и т.д.)

### Точка AF-25
`https://abiturient.tversu.ru/api/specialties/enroll/2025/1/1`  
Информация о подаче документов, частично дублирует другие точки

### Точка AF-26
`https://timetable.tversu.ru/api/v3/groups`  
Список всех групп ТвГУ

### Точка AF-27
`https://timetable.tversu.ru/api/v3/timetable?group_name={GROUP_NAME}&type={CATEGORY}`  
Выдаёт информацию о расписании
**Параметры:**  
- `GROUP_NAME` – название группы (например, ПМиК-16)  
- `CATEGORY` – ID категории (0 – занятия, 1 – экзамены, 2 – пересдачи, 3 – ГИА)

---

## Эндпоинты с авторизацией (NeA – Need Auth)

> Авторизация реализована через Bearer Token в заголовке (JWT)  
JWT хранит в себе в том числе электронную почту, ID аккаунта


### Точка NeA-1
`https://abiturient.tversu.ru/api/address/regions`  
Список регионов РФ

### Точка NeA-2
`https://abiturient.tversu.ru/api/document-types/list/{N}`  
Списки документов для разных целей (образование, достижения, особые обстоятельства, портфолио)

> Для подробностей смотрите приложение 1

### Точка NeA-3
`https://abiturient.tversu.ru/api/document-types/list/10`  
Список документов: заявления на обучение, ИНН, заграничный паспорт и т.д.

### Точка NeA-4 **UR**
`https://abiturient.tversu.ru/api/catalog/sports`  
Список спортивных достижений

  
## Приложение 1  
> Для NeA 2  

### N = 1:
`https://abiturient.tversu.ru/api/document-types/list/1`  
Выдаёт список типов документов

### N = 2:
`https://abiturient.tversu.ru/api/document-types/list/2`  
Выдаёт список особых обстоятельств сдачи экзамена

### N = 3:
`https://abiturient.tversu.ru/api/document-types/list/3`  
Выдаёт список документов об окончании образования

### N = 4:
`https://abiturient.tversu.ru/api/document-types/list/4`  
Выдаёт список документов за достижения, добавляющие дополнительные баллы

### N = 5:
`https://abiturient.tversu.ru/api/document-types/list/5`  
Выдаёт список документы по типу родства с кем-то и т.д., а также портфолио

### N = 6:
`https://abiturient.tversu.ru/api/document-types/list/6`  
Список документов, подтверждающих индивидуальные достижения

### N = 7:
`https://abiturient.tversu.ru/api/document-types/list/7`  
Список документов, подтверждающих индивидуальные достижения спортивного характера

- N=8, N=9 **UR**

### N = 10:
`https://abiturient.tversu.ru/api/document-types/list/10`  
Список документов по типу заявлений на обучение, ИНН, отзыв согласия, заграничный паспорот и т.д.
