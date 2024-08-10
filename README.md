# Сервис тестом-тренажером АПО с REST API и Tg-ботом

Сервис с тренажером для подготовки к олимпиадам. Сервис имеет Event-Driven архитектуру
с элементами аспектно-ориентированного программирования

## Требования к сервису

### 1. Сервис должен иметь общую логику для телеграм-бота и для REST API (и иметь возможность легко добавить новую платформу)

Для этого будут реализованы модели данных в `src/models` для общения между слоями, а также для каждой платформы будет
свой Docker контейнер

### 2. У сервиса архитектура должна располагать к свободному добавлению новых фичей и разграничению логики между ними

Поэтому в сервисе есть множество ивентов в `src/events`, такие как: регистрация, тренировка, получение статистики и тд.
В каждом из ивентов будет различная реализация для телеграм бота и для REST API с общим бэкендом. 

### 3. Сервис должен иметь высокую поддерживаемость кода. Код должен быть чистым и понятным

Для простоты сервис будет иметь модульную монолитную архитектуру. В дальнейшем с переходом на микросервисную 
(если будет несколько серверов и нагрузка)

Для чистоты кода использовались аспекты в `src/aspects`, для очистки кода в сервисах и контроллерах от кэширования,
логирования, проверки пользователя в БД и так далее

Для простоты я отказался, например, от `alembic`. Из коробки сервис не работает и требует настройки автоматически
сгенерированного кода, иногда не видит модели ORM и не подключается к БД. 
Для миграций я буду просто каждый раз буду писать SQL код миграций

Также, я разграничил сервисы и репозитории. Благодаря этому можно написать репозитории, 
с продуманной инфраструктурой, работой с сессиями и ORM, чтобы потом в сервисах можно было без проблем
реализовывать бизнес логику

Так на проект проще будет приглашать новичков, для них репозитории будут готовы, по интерфейсу они будут понимать
какие данные требуются и что возвращается

### 4. Сервис должен выдавать большое количество аналитических данных (дальше чем MVP)
Для этого логи сервиса будут сохраняться в `ClickHouse` и визуализироваться в `Graphana`


# Реализация
## Бизнес Логика (25%):
- [x] Регистрация (Bot)
- [ ] Авторизация (API)
- [x] Стартововая страница (Bot) 
- [ ] Тренировка 
- [ ] Личный кабинет
- [ ] Статистика
- [ ] Фильтры
- [ ] Админка:
  - [ ] Рассылка
  - [ ] Экспорт в xlsx

## Инфраструктура (25%)
- [x] Pydantic Схемы
- [x] DI контейнер
- [x] Сервис пользователей 
- [x] Аспекты (Bot) 
- [ ] Сервис статистики
- [ ] Сервис фильтров
- [ ] ORM
- [ ] Реализовать работу с сессиями (транзакции или UoW)
- [ ] Добавить миграции
- [ ] Поднять PostgreSQL
- [ ] Репозиторий для пользователей
- [ ] Поднять MongoDB
- [ ] Репозиторий для статистики
- [ ] Репозиторий для фильтров
- [ ] Поднять Clickhouse
- [ ] Поднять Graphana