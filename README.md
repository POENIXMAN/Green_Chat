# Green Chat

## Описание проекта
Green Chat — это чат-приложение, которое предоставляет возможность пользователям общаться в реальном времени через веб-сокеты. Приложение поддерживает аутентификацию пользователей с использованием JWT, управление каналами (чатами), сохранение сообщений в базе данных и базовую админку для управления.

---

## Установка и запуск приложения

### 1. Установка с использованием Docker
Убедитесь, что у вас установлены Docker и Docker Compose.

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/POENIXMAN/Green_Chat.git
   cd Green_Chat
   ```

2. Соберите и запустите контейнеры:
   ```bash
   docker-compose up --build
   ```

3. После запуска приложение будет доступно по адресу:
   ```
   http://127.0.0.1:8000
   ```

4. Для доступа к админке:
   - Перейдите на `http://127.0.0.1:8000/admin/`
   - Логин/пароль администратора можно создать через Django Management:
     ```bash
     docker-compose exec web python manage.py createsuperuser
     ```
5. Миграция:
   ```bash
     docker-compose exec web python manage.py migrate
     ```

---

## API-эндпоинты

### 1. **Регистрация нового пользователя**
**URL:** `/api/register/`  
**Метод:** `POST`  
**Пример тела запроса:**
```json
{
  "username": "testuser",
  "password": "123456",
  "email": "testuser@example.com"
}
```
**Ответ:**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "testuser@example.com"
}
```

---

### 2. **Получение JWT-токена для аутентификации**
**URL:** `/api/token/`  
**Метод:** `POST`  
**Пример тела запроса:**
```json
{
  "username": "testuser",
  "password": "123456"
}
```
**Ответ:**
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

---

### 3. **Обновление JWT-токена**
**URL:** `/api/token/refresh/`  
**Метод:** `POST`  
**Пример тела запроса:**
```json
{
  "refresh": "<refresh_token>"
}
```
**Ответ:**
```json
{
  "access": "<new_access_token>"
}
```

---

### 4. **Создание канала (чата)**
**URL:** `/api/chat/channels/`  
**Метод:** `POST`  
**Требует аутентификации через заголовок:**
```
Authorization: Bearer <access_token>
```
**Пример тела запроса:**
```json
{
  "name": "general"
}
```
**Ответ:**
```json
{
  "id": 1,
  "name": "general"
}
```

---

### 5. **Получение списка каналов**
**URL:** `/api/chat/channels/`  
**Метод:** `GET`  
**Требует аутентификации через заголовок:**
```
Authorization: Bearer <access_token>
```
**Ответ:**
```json
[
  {
    "id": 1,
    "name": "general"
  },
  {
    "id": 2,
    "name": "random"
  }
]
```

---

### 6. **Получение сообщений из канала**
**URL:** `/api/chat/messages/<channel_id>/`  
**Метод:** `GET`  
**Требует аутентификации через заголовок:**
```
Authorization: Bearer <access_token>
```
**Ответ:**
```json
[
  {
    "id": 1,
    "sender": "testuser",
    "text": "Hello, world!",
    "timestamp": "2024-11-18T10:00:00Z"
  },
  {
    "id": 2,
    "sender": "anotheruser",
    "text": "Hi there!",
    "timestamp": "2024-11-18T10:05:00Z"
  }
]
```

---

### 7. **Блокировка пользователя**
**URL:** `/api/chat/block_user/`  
**Метод:** `POST`  
**Требует аутентификации через заголовок:**
```
Authorization: Bearer <access_token>
```
**Пример тела запроса:**
```json
{
  "channel_id": 1,
  "user_id": 2
}
```
**Ответ:**
```json
{
  "message": "User 2 was blocked in channel 1."
}
```

---

### 8. **Подключение к WebSocket-чату**
**URL:** `ws://127.0.0.1:8000/ws/chat/<channel_id>/?token=<access_token>`  
**Метод:** WebSocket  

**Пример подключения через WebSocket:**
- Клиент отправляет сообщение:
  ```json
  {
    "message": "Привет всем!"
  }
  ```
- Сервер возвращает сообщение:
  ```json
  {
    "message": "Привет всем!",
    "sender": "testuser"
  }
  ```

---

## Скрипт для создания тестовых данных
Чтобы создать тестовые данные (пользователей, каналы и сообщения), выполните команду:
```bash
docker-compose exec web python manage.py create_test_data
```
Это создаст:
- Несколько тестовых пользователей
- Примерные каналы
- Примерные сообщения

---


## Важные моменты
1. Все запросы к API, требующие аутентификации, должны содержать заголовок `Authorization: Bearer <access_token>`.
2. WebSocket требует передачи JWT-токена в строке запроса.

---

### Ссылка на репозиторий
[Green Chat на GitHub](https://github.com/POENIXMAN/Green_Chat)

