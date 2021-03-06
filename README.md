# Отчёт `tcpchat`

### Исходный код приложения
Весь исходный код приложения содержится в папке [`/src`](./src)

### Список используемых библиотек
1. [socket](https://docs.python.org/3/library/socket.html)
1. [select](https://docs.python.org/3/library/select.html)
1. [\_thread](https://docs.python.org/3/library/_thread.html)
1. [syslog](https://docs.python.org/3/library/syslog.html)

### Инструкция по разворачиванию/установке на ОС
Установка приложения:
```bash
$ git clone https://github.com/endygamedev/test-dev-raidix.git
$ cd test-dev-raidix
$ pip3 install -r requirements.txt
$ pip3 install .
```

### Описание параметров утилит с примерами использования

#### Описание параметров
После установки, утилита `tcpchat` сразу же доступна из терминала.

Использование:
```bash
tcpchat <mode> <ip_address> <port>

mode:
  s               Использовать скрипт для запуска сервера.
  c               Использовать скрипт для запуска клиента.
  
ip_address:
  IP адрес, на котором будет открыт сокет (в случае сервера) или к которому нужно подключиться (в случае клиента).
  
  Например: 127.0.0.1
            localhost

port:
  Порт, на котором будет открыт сокет (в случае сервера) или к которому нужно подключиться (в случае клиента).

  Например: 1234
            4321
```

#### Пример использования
Давайте для примера создадим чат из трёх пользователей на `localhost:1234`.

Сначала создаём сервер:
```
$ tcpchat s localhost 1234
```

Затем создаём клиентов.

Клиент 1:
```
$ tcpchat c localhost 1234
```

Клиент 2:
```
$ tcpchat c localhost 1234
```

Клиент 3:
```
$ tcpchat c localhost 1234
```

В окне с запущенным сервером можно видеть состояние сервера и все сообщения пользователей.

В окне с клиентами можно видеть сообщения других пользователей и написать что-то от имени конкретного клиента.

В `tmux` это выглядит следующим образом:
![screenshot](./assets/screen.png)
