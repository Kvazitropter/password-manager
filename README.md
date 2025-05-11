# Менеджер Паролей

[![Linting](https://github.com/Kvazitropter/password-manager/actions/workflows/pylint.yml/badge.svg)](https://github.com/Kvazitropter/password-manager/actions/workflows/pylint.yml)
[![Testing](https://github.com/Kvazitropter/password-manager/actions/workflows/pytests.yml/badge.svg)](https://github.com/Kvazitropter/password-manager/actions/workflows/pytests.yml)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Kvazitropter_password-manager&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Kvazitropter_password-manager)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Kvazitropter_password-manager&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Kvazitropter_password-manager)

---

Приложение для хранения паролей в зашифрованном виде.
- Мастер пароль хранится только в рамках одной сессии и нигде не сохраняется.
- Все пароли зашифрованы и хранятся в одном месте.
- Есть встроенная генерация паролей с настройкой параметров.

---

## Как работает шифрование
1. Из мастер-пароля и случайной соли формируется криптографический ключ.
2. Ключ передаётся в симметричный алгоритм шифрования.
4. Каждый пароль шифруется отдельно, с использованием уникальной соли.
5. Зашифрованное значение и соль сохраняются в базе.

---

![Старт](https://i.imgur.com/PGpUdNP.png)

![Вход](https://i.imgur.com/tIXjXan.png)

![Хранилище](https://i.imgur.com/iERI1sw.png)

![Настройки генерации пароля](https://i.imgur.com/R8ke44C.png)

![Просмотр записи](https://i.imgur.com/RENwEQ6.png)

---

# Установка:

```
git clone https://github.com/Kvazitropter/password-manager.git
make setup
make run
make build
```

---
