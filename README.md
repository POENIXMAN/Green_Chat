# Green Chat

## Описание проекта
Green Chat — это чат-приложение, которое предоставляет возможность пользователям общаться в реальном времени через веб-сокеты. Приложение поддерживает аутентификацию пользователей с использованием JWT, управление каналами (чатами) и сохранение сообщений в базе данных.

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

### 3. **Создание канала (чата)**
**URL:** `/api/channels/`  
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

### 4. **Получение списка каналов**
**URL:** `/api/channels/`  
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

### 5. **Подключение к WebSocket-чату**
**URL:** `ws://127.0.0.1:8000/ws/chat/<channel_id>/?token=<access_token>`  
**Метод:** `WebSocket`  

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

### 6. **Отправка сообщения в канал**
Сообщения, отправленные через WebSocket, автоматически сохраняются в базу данных.

**Пример структуры сообщения:**
```json
{
  "message": "Как дела?"
}
```

---

### 7. **Скрипт для создания тестовых данных**
Чтобы создать тестовые данные (пользователей, каналы и сообщения), выполните команду:
```bash
docker-compose exec web python manage.py create_test_data
```
Это создаст:
- Несколько тестовых пользователей
- Примерные каналы
- Примерные сообщения

---

## Тестирование API
Для запуска тестов выполните:
```bash
docker-compose exec web python manage.py test
```

---

## Структура проекта
- **chat/**  
  Основное приложение, содержащее модели, API, веб-сокетных потребителей и маршруты.

- **Dockerfile**  
  Описание сборки Docker-образа.

- **docker-compose.yml**  
  Конфигурация для Docker Compose.

- **tests.py**  
  Тесты для API и WebSocket.

---

## Важные моменты
1. Все запросы к API, требующие аутентификации, должны содержать заголовок `Authorization: Bearer <access_token>`.
2. WebSocket требует передачи JWT-токена в строке запроса.

---

### Ссылка на репозиторий
[Green Chat на GitHub](https://github.com/POENIXMAN/Green_Chat)