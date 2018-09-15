# easysport
Web server and web version

## How to start

```
docker-compose -f local.yml build
docker-compose -f local.yml up
```

## How to execute console in web container

```
docker-compose -f local.yml exex web /bin/sh
```

## Deploy

Проект деплоится на dev.easysport.online
VPS-хостинг на smartape.ru

```
IP-адрес: 188.127.231.216
Пользователь: root
Пароль: 9jFLO8w9oSW4
```

## Migration from 2.0

1. Make fixtures

```
python manage.py dumpdata users -o fixtures/users.json
```

2. Load locally

```angular2html
scp -r root@easysport.online:/opt/sportcourts2/fixtures ~/Dev
```

3. Loaddata

Zero - users
First - places. Rename places app to courts, но нужно перебить адреса и площадки
Secons - sporttypes
Third - courts
Fourth - games/ Only renew existing games
