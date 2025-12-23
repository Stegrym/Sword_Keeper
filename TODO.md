## Этап 1. Логика (Domain)

1.[X] Определить сущность Entry (service, login, email, password).

2.[ ] Реализовать базовые функции:

    - [X] add_entry()

    - [X] list_entries()

    - [X] search_entry()

    - [ ] delete_entry()

3.[ ] Сделать заглушку хранения (список в памяти или JSON).

4.[ ] Написать простые тесты для этих функций.

### Коммиты:

```
feat(domain): add Entry model

feat(domain): implement add/list/search/delete with in-memory storage

test(domain): add unit tests for use cases
```

___

## Этап 2. Хранилище (Storage)

1.[ ] Создать интерфейс StorageInterface (CRUD методы).

2.[ ] Реализовать JSONStorage (чтение/запись в файл).

3.[ ] Реализовать SQLiteStorage (таблица passwords).

4.[ ] Подключить SQLAlchemy или стандартный sqlite3.

5.[ ] Добавить тесты для CRUD операций.

### Коммиты:

```
feat(storage/json): implement JSONStorage

feat(storage/sqlite): implement SQLiteStorage with CRUD

refactor(domain): inject storage interface into use cases

test(storage): add tests for persistence
___
```

## Этап 3. Интерфейс (UI)

1.[ ] Создать базовое окно Tkinter.

2. [ ] Добавить поля ввода: service, email, password.

3. [ ] Добавить кнопку «Сохранить» → вызывает add_entry().

4. [ ] Добавить поле поиска → вызывает search_entry().

5. [ ] Отобразить список записей.

### Коммиты:

```
feat(ui): add Tkinter form for entry

feat(ui): add save button connected to add_entry

feat(ui): add search field

style(ui): improve layout
```

___

## Этап 4. Тесты и улучшения

1.[ ] Написать тесты для логики и хранилища.

2. [ ] Добавить базовую валидацию email (регулярка).

3. [ ] Добавить возможность удаления записи.

4. [ ] Подготовить README.md с описанием проекта.

### Коммиты:

```
test(domain): extend tests for validation

feat(domain): add email validation

feat(domain): add delete entry

docs: add README with usage instructions
```

___