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

<table>
  <tr>
    <td><img src="https://i.imgur.com/huciKPu.png" alt="Старт" width="300"/></td>
    <td><img src="https://i.imgur.com/nLh2Glb.png" alt="Вход" width="300"/></td>
  </tr>
  <tr>
    <td><img src="https://i.imgur.com/XlwPSCb.png" alt="Хранилище" width="300"/></td>
    <td>
      <img src="https://i.imgur.com/K8x3WUK.png" alt="Просмотр записи" width="300"/>
      <div style="height: 10px;"></div>
      <img src="https://i.imgur.com/R8ke44C.png" alt="Настройки генерации пароля" width="175"/>
    </td>
  </tr>
</table>

---

# Установка:

1. Установите PostgreSQL
2. Создайте сервер с настройками по умолчанию и паролем xxXX1234
3. Создайте базу данных password-manager
4. Выполните запрос из файла db/sql.txt

```
git clone https://github.com/Kvazitropter/password-manager.git
make setup
make build
```

---
