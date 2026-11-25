# Lab 2 — In-Memory RESTful API & Bruno Collection

RESTful API для системи обліку витрат із зберіганням сутностей (`User`, `Category`, `Record`) в оперативній пам'яті (In-Memory) та колекцією запитів у форматі Bruno OpenCollection[cite: 2, 3, 4].

## Запуск сервісу

### Локально (Python)

1. Активуйте віртуальне середовище та встановіть залежності:

```bash
pip install -r requirements.txt
```

2. Запустіть застосунок на порту `8080`:

```bash
python main.py
```

### Через Docker / Docker Compose

```bash
docker compose up --build
```

*(або зберіть і запустіть образ через `Dockerfile` на порту `8080`)*[cite: 2, 3].

## Тестування в Bruno

Колекція запитів розташована в директорії `bruno_collection/`[cite: 2, 4].

1. Відкрийте колекцію `bruno_collection` у клієнті **Bruno**[cite: 2, 3, 4].
2. У правому верхньому куті оберіть середовище **Local** (змінна `baseUrl` має значення `http://localhost:8080`)[cite: 3].
3. Запустіть запити для сутностей `User`, `Category` та `Record`:
   - створення, отримання та видалення користувачів (`/user`, `/users`);
   - створення, отримання та видалення категорій (`/category`);
   - створення, отримання, фільтрація та видалення записів (`/record`);
   - перевірка валідації (`400 Bad Request` при відсутності query-параметрів у `GET /record`) та обробки помилок (`404 Not Found` для неіснуючих ID)[cite: 4, 5, 6].

*ІО-42 Татарчук Володимир*