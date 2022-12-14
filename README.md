# 
    Задание для[школы бэкэнд-разработки Yandex](http://yandex.ru/promo/academy/backend-school/)

[![Build Status](https://camo.githubusercontent.com/3b8b9e9a1ae7d2671892ae07ebb755733e1620fd33cce5bc5f13bd9e0222f31a/68747470733a2f2f7472617669732d63692e636f6d2f4b6f6e7973686576417274656d2f79616e6465782d61636164656d792d7461736b2e7376673f746f6b656e3d7a33736a6f416343344847577069577467547879266272616e63683d6d6173746572)](https://travis-ci.com/KonyshevArtem/yandex-academy-task)

* [Описание задания](https://github.com/KonyshevArtem/yandex-academy-task#decription)
* [Реализованные обработчики REST API](https://github.com/KonyshevArtem/yandex-academy-task#handlers)
  * [1: POST /imports](https://github.com/KonyshevArtem/yandex-academy-task#post-import)
  * [2: PATCH /imports/$import_id/citizens/$citizen_id](https://github.com/KonyshevArtem/yandex-academy-task#patch-citizen)
  * [3: GET /imports/$import_id/citizens](https://github.com/KonyshevArtem/yandex-academy-task#get-citizens)
  * [4: GET /imports/$import_id/citizens/birthdays](https://github.com/KonyshevArtem/yandex-academy-task#get-birthdays)
  * [5: GET /imports/$import_id/towns/stat/percentile/age](https://github.com/KonyshevArtem/yandex-academy-task#get-percentile)
* [Инструкции](https://github.com/KonyshevArtem/yandex-academy-task#guides)
  * [Запуск приложения](https://github.com/KonyshevArtem/yandex-academy-task#launch-app)
    * [Docker Compose](https://github.com/KonyshevArtem/yandex-academy-task#docker-compose)
    * [Вручную](https://github.com/KonyshevArtem/yandex-academy-task#manual)
  * [Запуск тестов](https://github.com/KonyshevArtem/yandex-academy-task#launch-tests)

## Описание задания

Интернет-магазин подарков хочет запустить акцию в разных регионах. Чтобы стратегия продаж была эффективной, необходимо произвести анализ рынка.

У магазина есть поставщик, регулярно присылающий выгрузки данных с информацией о жителях. Проанализировав их, можно выявить спрос на подарки в разных городах у жителей разных возрастных групп по месяцам.

Ваша задача - разработать на python REST API сервис, который сохраняет переданные ему наборы данных (выгрузки от поставщика) c жителями, позволяет их просматривать, редактировать информацию об отдельных жителях, а также производить анализ возрастов жителей по городам и анализировать спрос на подарки в разных месяцах для указанного набора данных.

Должна быть реализована возможность загрузить несколько независимых наборов данных с разными идентификаторами, независимо друг от друга изменять и анализировать их.

Сервис необходимо развернуть на предоставленной виртуальной машине на 0.0.0.0:8080.

## Обработчики REST API

### 1: POST /imports

Принимает на вход набор с данными о жителях в формате `json` и сохраняет его с уникальным идентификатором `import_id` .

В наборе данных для каждого жителя должны присутствовать все поля, значения не могут быть `null` , порядок полей не важен:

| Поле      | Тип                                  | Значение                                                                                                                                                               |
| ------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| citizen_id^1^ | целое число                   | Уникальный идентификатор жителя, неотрицательное число                                                                        |
| town          | строка                            | Название города. Непустая строка, содержащая хотя бы 1 букву или цифру.                                               |
| street        | строка                            | Название улицы. Непустая строка, содержащая хотя бы 1 букву или цифру.                                                 |
| building      | строка                            | Номер дома, корпус и строение. Непустая строка, содержащая хотя бы 1 букву или цифру.                       |
| apartment     | целое число                   | Номер квартиры, неотрицательное число.                                                                                                        |
| name          | строка                            | Непустая строка.                                                                                                                                                 |
| birth_date^2^ | строка                            | Дата рождения в формате ДД.ММ.ГГГГ (UTC)                                                                                                           |
| gender        | строка                            | Значение `male`, `female`                                                                                                                                          |
| relatives^3^  | список из целых чисел | Ближайшие родственники, уникальные значения существующих `citizen_id` жителей из этой же выгрузки. |

В случае, если в наборе есть неописанные поля - следует считать такой запрос некорректным и возвращать ошибку 400: Bad Request.

^(1)^ Поставщик предупредил, что в разных выгрузках `citizen_id` не уникален и может повторяться у разных жителей, не закладывайтесь на то, что `citizen_id` будут уникальны между выгрузками от поставщика.

^(2)^ помимо проверки на формат ДД.ММ.ГГГГ - дата должна быть существующей ( 31.02.2019 - не является валидной датой). Проверить, что дата является валидной можно с помощью datetime.date .

^(3)^ Родственные связи двусторонние (если у жителя #1 в родственниках указан житель #2, то и у жителя #2 должен быть родственник #1). Родственные связи `relatives` актуальны только в рамках одной выгрузки.

```
POST /imports
{
	"citizens": [
		{
			"citizen_id": 1,
			"town": "Москва",
			"street": "Льва Толстого",
			"building": "16к7стр5",
			"apartment": 7,
			"name": "Иванов Иван Иванович",
			"birth_date": " 26.12.1986",
			"gender": "male",
			"relatives": [2] // id родственников
		},
		{
			"citizen_id": 2,
			"town": "Москва",
			"street": "Льва Толстого",
			"building": "16к7стр5",
			"apartment": 7,
			"name": "Иванов Сергей Иванович",
			"birth_date": "17.04.1997",
			"gender": "male",
			"relatives": [1] // id родственников
		},
		{
			"citizen_id": 3,
			"town": "Керчь",
			"street": "Иосифа Бродского"
			"building": "2",
			"apartment": 11,
			"name": "Романова Мария Леонидовна",
			"birth_date": "23.11.1986",
			"gender": "female",
			"relatives": []
		},
		...
	]
}
```

В случае успеха возвращается ответ с HTTP статусом `201 Created` и идентификатором импорта:

```
HTTP 201
{
	"data": {
		"import_id": 1
	}
}
```

### 2: PATCH /imports/$import_id/citizens/$citizen_id

Изменяет информацию о жителе в указанном наборе данных.

На вход подается JSON в котором можно указать любые данные о жителе ( `name` , `gender` , `birth_date` (UTC), `relatives` , `town` , `street` , `building` , `apartment` ), кроме `citizen_id` .

В запросе должно быть указано хотя бы одно поле, значения не могут быть `null` .

Если в запросе указано поле `relatives` - изменение родственных связей должно быть двусторонним.

Например, есть два брата - Ивановы Иван ( `citizen_id=1` ) и Сергей ( `citizen_id=2` ). Мария Леонидовна ( `citizen_id=3` ) вышла замуж за Ивана, стала ему ближайшей родственницей и переехала в Москву:

```
PATCH /imports/1/citizens/3
{
	"name": "Иванова Мария Леонидовна",
	"town": "Москва",
	"street": "Льва Толстого",
	"building": "16к7стр5",
	"apartment": 7,
	"relatives": [1]
}
```

В результате этого запроса данные о жителях должны прийти в следующее состояние:

* Житель 1: relatives = [2, 3] (житель #2 брат, житель #3 супруга)
* Житель 2: relatives = [1] (житель #1 брат)
* Житель 3: relatives = [1] (житель #1 супруг)

Возвращается актуальная информация об указанном жителе:

```
HTTP 200
{
	"data": {
		"citizen_id": 3,
		"town": "Москва",
		"street": "Льва Толстого",
		"building": "16к7стр5",
		"apartment": 7,
		"name": "Иванова Мария Леонидовна",
		"birth_date": "23.11.1986",
		"gender": "female",
		"relatives": [1]
	}
}
```

Если девушка разведется с супругом, необходимо будет выполнить следующий запрос:

```
PATCH /imports/1/citizens/3
{
    "relatives": []
}
```

В результате этого запроса данные о жителях должны прийти в следующее состояние:

* Житель 1: relatives = [2] (житель #2 брат)
* Житель 2: relatives = [1] (житель #1 брат)
* Житель 3: relatives = []

И вернется актуальная информация об указанном жителе:

```
HTTP 200
{
    "data": {
        "citizen_id": 3,
        "town": "Москва",
        "street": "Льва Толстого",
        "building": "16к7стр5",
        "apartment": 7,
        "name": "Иванова Мария Леонидовна",
        "birth_date": "23.11.1986",
        "gender": "female",
        "relatives": []
    }
}
```

### 3: GET /imports/$import_id/citizens

Возвращает список всех жителей для указанного набора данных.

```
HTTP 200
{
	"data": [
		{
			"citizen_id": 1,
			"town": "Москва",
			"street": "Льва Толстого",
			"building": "16к7стр5",
			"apartment": 7,
			"name": "Иванов Иван Иванович",
			"birth_date": " 26.12.1986",
			"gender": "male",
			"relatives": [2,3] // id родственников
		},
		{
			"citizen_id": 2,
			"town": "Москва",
			"street": "Льва Толстого",
			"building": "16к7стр5",
			"apartment": 7,
			"name": "Иванов Сергей Иванович",
			"birth_date": "17.04.1997",
			"gender": "male",
			"relatives": [1] // id родственников
		},
		{
			"citizen_id": 3,
			"town": "Москва",
			"street": "Льва Толстого",
			"building": "16к7стр5",
			"apartment": 7,
			"name": "Иванова Мария Леонидовна",
			"birth_date": "23.11.1986",
			"gender": "female",
			"relatives": [1]
		},
		...
	]
}
```

### 4: GET /imports/$import_id/citizens/birthdays

Возвращает жителей и количество подарков, которые они будут покупать своим ближайшим родственникам (1-го порядка), сгруппированных по месяцам из указанного набора данных.

Ключом должен быть месяц (нумерация должна начинаться с единицы, `"1"` - январь, `"2"` - февраль и т.п.).

Если в импорте в каком-либо месяце нет ни одного жителя с днями рождения ближайших родственников, значением такого ключа должен быть пустой список.

```
HTTP 200
{
	"data": {
		"1": [],
		"2": [],
		"3": [],
		"4": [{
			"citizen_id": 1,
			"presents": 1,
		}],
		"5": [],
		"6": [],
		"7": [],
		"8": [],
		"9": [],
		"10": [],
		"11": [{
			"citizen_id": 1,
			"presents": 1
		}],
		"12": [
			{
				"citizen_id": 2,
				"presents": 1
			},
			{
				"citizen_id": 3,
				"presents": 1
			}
		]
	}
}
```

### 5: GET /imports/$import_id/towns/stat/percentile/age

Возвращает статистику по городам для указанного набора данных в разрезе возраста (полных лет) жителей: p50, p75, p99, где число - это значение перцентиля.

Расчеты необходимо производить используя текущую дату (UTC). Значения перцентилей необходимо округлять до 2х знаков после запятой.

```
HTTP 200
{
	"data": [
		{
			"town": "Москва",
			"p50": 20,
			"p75": 45,
			"p99": 100
		},
		{
			"town": "Санкт-Петербург",
			"p50": 17,
			"p75": 35,
			"p99": 80
		}
	]
}
```

Что означает:

* `"p50": 20,` - 50% жителей меньше 20 лет
* `"p75": 45,` - 75% жителей меньше 45 лет
