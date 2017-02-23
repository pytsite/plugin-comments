# PytSite Comments HTTP API


## GET comments/settings

Получение параметров конфигурации API комментариев.


### Формат ответа

Объект.

- **int** `max_depth`. Максимальная глубина вложенности комментария.
- **int** `body_min_length`. Минимальная длина текста комментария.
- **int** `body_max_length`. Максимальная  длина текста комментария.
- **object** `statuses`. Возможные статусы комментария и их описания.
- **object** `permissions`. Права учётной записи.
    - **bool** `create`. Право на создание комментариев.


### Примеры

Запрос:

```
curl -X GET \
-H 'PytSite-Auth: 227912317f4439e6b5ba496f183947f8' \
-H 'PytSite-Lang: ru' \
http://test.com/api/1/comments/settings
```


Ответ:

```
{
    "body_min_length": 2, 
    "body_max_length": 2048,
    "max_depth": 4,
    "statuses": {
        "published": "Опубликован",
        "waiting": "На модерации",
        "spam": "Спам",
        "deleted": "Удалён"
    },
    "permissions": {
        "create": true
    }
}
```


## POST comments/comment

Добавление нового комментария. Обязательна [аутентификация](https://github.com/pytsite/pytsite/blob/devel/pytsite/http_api/doc/ru/index.md#%D0%90%D1%83%D1%82%D0%B5%D0%BD%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F-%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81%D0%BE%D0%B2).


### Аргументы

- *required* **str** `thread_uid`. Уникальный идентификатор ветки комментариев. Как правило, это путь страницы, на 
  которой будет отображаться данная ветка, без учёта суффикса локализации. Абсолютный URL использовать не рекомендуется, 
  поскольку это усложнит перенос сайта на другой домен.
- *required* **str** `body`. Текст сообщения. HTML и лишние пробелы будут автоматически удалены. Минимальная длина по 
  умолчанию: 2 символа, максимальная длина по умолчанию: 2048 символов. Минимальная и максимальная длины вычисляются
  *после* очистки текста от лишних пробелов и HTML.
- *optional* **str** `parent_uid`. UID родительского комментария. При использовании этого параметра необходимо следить,
  чтобы не было превышения максимально-допустимой вложенности, которая по умолчанию составляет 4.
- *optional* **str** `driver`. Имя драйвера.


### Формат ответа

Объект.

- **str** `uid`. Уникальный идентификатор комментария.
- **str** `parent_uid`. Уникальный идентификатор родительского комментария.
- **str** `thread_uid`. Уникальный идентификатор ветки.
- **str** `status`. Статус.
- **int** `depth`. Глубина вложенности комментария.
- **str** `body`. Текст комментария.
- **object** `author`. Данные об учётной записи автора комментария.
    - **str** `uid`. Уникальный идентификатор.
    - **str** `nickname`. Никнейм.
    - **str** `full_name`. Имя и фамилия.
    - **str** `picture_url`. URL изображения.
    - **str** `profile_url`. URL профиля.
- **object** `publish_time`. Дата и время публикации.
    - **str** `w3c`. В формате W3C (https://www.w3.org/TR/NOTE-datetime).
    - **str** `pretty_date`. Дата в "человеческом" формате, например "4 сентября".
    - **str** `pretty_date_time`. Дата и время в "человеческом" формате, например "3 мая, 15:32".
    - **str** `ago`. Дата и время в формате "тому назад", например "2 недели". 
- **object** `permissions`. Права учётной записи в контексте комментария.
    - **bool** `modify`. Право на удаление комментария.
    - **bool** `delete`. Право на изменение комментария.
 

### Примеры

Запрос:

```
curl -X POST \
-H 'PytSite-Auth: 227912317f4439e6b5ba496f183947f8' \
-H 'PytSite-Lang: ru' \
-d thread_uid=/hello/world \
-d parent_uid=57b0b315523af525a269a02a \
-d body='Привет, Мир!' \
http://test.com/api/1/comments/comment
```


Ответ:

```
{
    "uid": "57b25223523af558d54f33ad", 
    "parent_uid": "57b0b315523af525a269a02a", 
    "thread_uid": "/hello/world",
    "status": "published",
    "depth": 2,
    "body": "Привет, Мир!",
    "publish_time": {
        "w3c": "2016-08-16T02:37:07+0300",
        "pretty_date": "16 августа",
        "pretty_date_time": "16 августа, 02:37",
        "ago": "Только что"
    }, 
    "author": {
        "uid": "579178ed523af5473134aed6",
        "nickname": "pupkeen", 
        "full_name": "Василий Пупкин",
        "picture_url": "http://test.com/image/resize/50/50/15/b5/8c319860b6a92a69.png", 
        "profile_url": "http://test.com/auth/profile/pupkeen"
    }, 
    "permissions": {
        "modify": true, 
        "delete": true
    }
}
```


## GET comment/:uid

Получение комментария.


### Аргументы

- `uid`. Уникальный идентификатор комментария.


### Параметры

- *optional* **str** `driver`. Дравйер.


### Формат ответа

Объект. Набор полей полностью идентичен ответу метода **POST comments/comment**.


### Прмеры

Запрос:

```
curl -X GET \
-H 'PytSite-Auth: 227912317f4439e6b5ba496f183947f8' \
-H 'PytSite-Lang: ru' \
http://test.com/api/1/comments/comment/57b25223523af558d54f33ad
```



## GET comments

Получение списка комментариев.


### Параметры

- *required* **str** `thread_uid`. Уникальный идентификатор ветки комментариев.
- *optional* **str** `driver`. Дравйер.


### Формат ответа

Объект.

- **array[object]** `items`. Информация о комментариях. Структура какждого элемента полностью совпадает со структурой 
  ответа метода `POST comments/comment` за исключением того, что если комментарий имеет статус, отличный от `published`,
  то поля `body` и `author` будут отсутствовать.

### Примеры

Запрос:

```
curl -X GET \
-H 'PytSite-Auth: 227912317f4439e6b5ba496f183947f8' \
-H 'PytSite-Lang: ru' \
-d thread_uid='/hello/world' \
http://test.com/api/1/comments
```


Ответ:

```
{
    "items": [
        ...
    ]
}
```


## DELETE comments/comment/:uid

Удаление комментария. Обязательна [аутентификация](https://github.com/pytsite/pytsite/blob/devel/pytsite/http_api/doc/ru/index.md#%D0%90%D1%83%D1%82%D0%B5%D0%BD%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F-%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81%D0%BE%D0%B2).


### Аргументы

- `uid`. Уникальный идентификатор комментария.


### Параметры

- *optional* **str** `driver`. Дравйер.


### Формат ответа

Объект.

- **bool** `status`. Результат обработки запроса.


### Примеры

Запрос:

```
curl -X DELETE \
-H 'PytSite-Auth: 227912317f4439e6b5ba496f183947f8' \
http://test.com/api/1/comments/comment/57b25223523af558d54f33ad
```


Ответ:

```
{
    "status": true
}
```


## POST comments/report/:uid

Отправка жалобы на комментарий.


### Аргументы

- `uid`. Уникальный идентификатор комментария.


### Формат ответа

Объект.

- **bool** `status`. Результат обработки запроса.


### Примеры

Запрос:

```
curl -X POST \
-H 'PytSite-Auth: 227912317f4439e6b5ba496f183947f8' \
http://test.com/api/1/comments/report/57b25223523af558d54f33ad
```


Ответ:

```
{
    "status": true
}
```
