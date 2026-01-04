# Эндпоинты сайта ТвГУ и полезные страницы

## Ключ
- **UR** – Неопознанное предназначение  
- **AF** – API без необходимости авторизации (Auth Free)  
- **NeA** – API с необходимостью авторизации (Need Auth, JWT)

---

## Публичные эндпоинты (AF)

### AF-1
`https://tversu.ru/calendars?year=2025&month=10&with_years=true`  
Выдаёт новости по дням.  
**Аргументы:**  
- `year` – текущий год отсчёта  
- `month` – номер месяца (0 = январь)  
- `with_years` – назначение не выяснено

### AF-2
`https://abiturient.tversu.ru/api/catalog/level-categories`  
Формы обучения с ID, названием и дополнительной информацией (`budgetTotal`, `paidTotal`).

### AF-3
`https://abiturient.tversu.ru/api/catalog/sources`  
Типы мест на направлениях (Целевая квота, совмещённая квота, по договору, бюджетные места и т.д.) с их ID, сокращениями названий и порядком сортировки.

### AF-4
`https://abiturient.tversu.ru/api/departments`  
Возвращает название университета и его ID.

### AF-5
`https://abiturient.tversu.ru/api/catalog/forms`  
Формы обучения.

### AF-6
`https://abiturient.tversu.ru/api/freports/screen/1/2/1`  
HTML-страница экрана подачи заявлений. Числа в конце влияют на фильтрацию и сортировку.

### AF-7
`https://abiturient.tversu.ru/api/freports/list/{DIRECTION}/{TYPE}/{LEVEL}`  
HTML-страница списка подавших документы.  
**Параметры:**  
- `DIRECTION` – ID направления  
- `TYPE` – ID типа места  
- `LEVEL` – уровень обучения (бакалавриат, магистратура, аспирантура)  

> Замечание: направления с разными формами обучения считаются различными.

### AF-8
`https://abiturient.tversu.ru/api/specialties/get/{DIRECTION}`  
Информация о направлении по его ID.

### AF-9
`https://abiturient.tversu.ru/api/catalog/current-date`  
Текущее время в ISO-8601 формате.

### AF-10
`https://abiturient.tversu.ru/api/catalog/nationality`  
Список национальностей.

### AF-11
`https://abiturient.tversu.ru/api/catalog/education-types`  
Список типов образования (высшее, среднее и т.д.).

### AF-12
`https://abiturient.tversu.ru/api/catalog/languages`  
Список языков.

### AF-13
`https://abiturient.tversu.ru/api/catalog/disciplines`  
Список дисциплин, учитываемых при поступлении.

### AF-14
`https://abiturient.tversu.ru/api/catalog/school-types`  
Список типов образовательных учреждений (школа, гимназия, институт и т.д.).

### AF-15
`https://abiturient.tversu.ru/api/catalog/faculties`  
Список факультетов без подробной информации.

### AF-16
`https://abiturient.tversu.ru/api/catalog/reference/{NUM}`  
Список справочной информации в зависимости от `NUM` (например, тип родства, уровень знания языка).

### AF-17
`https://abiturient.tversu.ru/api/catalog/epgu-reasons`  
Список причин отказа от Госуслуг (ЕГПУ).

### AF-18
`https://abiturient.tversu.ru/api/catalog/payment-types`  
Список способов оплаты обучения.

### AF-19
`https://abiturient.tversu.ru/api/catalog/contract-statuses`  
Список состояний договоров.

### AF-20
`https://abiturient.tversu.ru/api/catalog/ege`  
Список предметов ЕГЭ.

### AF-21
`https://abiturient.tversu.ru/api/catalog/regions`  
Список регионов (только СНГ и ЮФО).

### AF-22 **UR**
`https://abiturient.tversu.ru/api/catalog/divisions`  

### AF-23
`https://abiturient.tversu.ru/api/catalog/benefits`  
Список преимуществ при поступлении (инвалиды, сироты, ветераны и т.д.).

### AF-24
`https://abiturient.tversu.ru/api/catalog/test-types`  
Список типов результатов при поступлении (ЕГЭ, собеседование, внутренние экзамены и т.д.).

### AF-25
`https://abiturient.tversu.ru/api/specialties/enroll/2025/1/1`  
Информация о подаче документов, частично дублирует другие точки.

### AF-26
`https://timetable.tversu.ru/api/v3/groups`  
Список всех групп ТвГУ.

### AF-27
`https://timetable.tversu.ru/api/v3/timetable?group_name={GROUP_NAME}&type={CATEGORY}`  
Выдаёт информацию о расписании.  
**Параметры:**  
- `GROUP_NAME` – название группы (например, ПМиК-16)  
- `CATEGORY` – ID категории (0 – занятия, 1 – экзамены, 2 – пересдачи, 3 – ГИА)

---

## Эндпоинты с авторизацией (NeA, JWT)

> JWT хранит email и ID аккаунта, поэтому данные могут быть идентифицируемыми.

### NeA-1
`https://abiturient.tversu.ru/api/address/regions`  
Список областей РФ.

### NeA-2 … NeA-8
`https://abiturient.tversu.ru/api/document-types/list/{N}`  
Списки документов для разных целей (образование, достижения, особые обстоятельства, портфолио).  

- N=8–9 возвращают пустой список

### NeA-9
`https://abiturient.tversu.ru/api/document-types/list/10`  
Список документов: заявления на обучение, ИНН, заграничный паспорт и т.д.

### NeA-10 **UR**
`https://abiturient.tversu.ru/api/catalog/sports`  
Список спортивных достижений.

