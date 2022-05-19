## Ranks | Тестовое задание  


### Описание
Тестовое задание выполнено в двух вариантах:
- минимальная версия (в `apps.items`) + тесты **[Stripe Session]**  
- с бонусами (в `apps.cart`) + тесты **[Payment Intent]**  

Бонусных задачи:
- Запуск используя Docker  
- ✅ Использование environment variables   
- ✅ Просмотр Django Моделей в Django Admin панели  
- ✅ Запуск приложения на удаленном сервере, доступном для тестирования  
- ✅ Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items  
- Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме.   
- Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте  
- ✅ Реализовать не Stripe Session, а Stripe Payment Intent.  

Для скорости разработки были выполнены лишь те задачи, которым, на мой взгляд, стоило уделить внимание.


## Начало
- python 3.7+
- скопировать файл `envs/.env.dist` в корневую директорию проекта 
- создать виртуальное окружение `python -m venv/virtualenv env` 
- установить зависимости `pip install -r requirements.txt`
- `python manage.py migrate` -> `python manage.py runserver`
- при запуске будет создан админ пользователь (login: `admin`, password: `1`)
- при запуске будут созданы товары
- залогиниться через админ панель (в моделе `Order` необходима привязка к пользователю)


### URLS
#### Минимальная версия
<h3><code>GET /v1/item/{id}/</code></h2>
Простейшая HTML страница с информация о выбранном `Item` и кнопка Buy. 
По нажатию на кнопку Buy происходит запрос на `v1/buy/{id}`, получение session_id. С помощью JS библиотеки Stripe происходит редирект на Checkout форму.


<h3><code>GET /v1/buy/{id}/</code></h2>
Получение Stripe Session Id для оплаты выбранного `Item`.

`Response example`
```json  
HTTP 200
{   
    sessionId: "example"
}
```

---

#### С бонусами
<h3><code>GET /v2/item/list/ </code></h3>
HTML страница со списком всех товаров. На странице можно добавлять товары в корзину.  
**(динамическое обновление через JS)**


<h3><code>POST /v2/cart/add/</code></h3>
Добавление товара в корзину

`Params`
```json  
{
    itemId: int
}  
```

`Response example`
```json 
HTTP 200 
{
    itemId: 1,
    addedd: true 
}
```  


<h3><code>POST /v2/cart/remove/</code></h3>
Удаление товара из корзины

`Params`
```json  
{
    itemId: int
}  
```

`Response example`
```json  
HTTP 200
{
    itemId: 1,
    removed: true 
}
```  


<h3><code>POST /v2/cart/order/</code></h3>
Создание `Order` из содержимого корзины

`Params`
```json  
{}  
```

`Responses example`
```json  
HTTP 400
{
    orderCreated: false
}
```

```json  
HTTP 201
{
    orderId: 1,
    orderCreated: true 
}
```  


<h3><code>GET /v2/order/status/</code></h3>
HTML страница со статусом оплаты Payment Intent.  


<h3><code>GET /v2/order/status/check/</code></h3>
Получение статуса оплаты Payment Intent.  
Обновление статуса оплаты `Order`


`Params`
```json  
{
    pi_secret: 'example'
}
```

`Response example`
```json  
{
    intentSecret: 'example'
}
```

