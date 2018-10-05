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

### Initial setup for Ubuntu

1. Create non-root user:
```
adduser easysport (pass:easysport)
```

2. Give root priveleges
```
usermod -aG sudo easysport
```

3. Login as user @easysport
```
su - easysport
```

TODO: [add nopassword authentication](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04)

### Install docker

[Docker.com](https://docs.docker.com/install/linux/docker-ce/ubuntu/#supported-storage-drivers)
```
sudo usermod -a -G docker $USER
```
then logout and login

### Install docker-compose
[Docs](https://docs.docker.com/compose/django/#connect-the-database)

### Grant priveleges to opt dir
```
sudo chmod 777 /opt  
```

## Migration from 2.0

1. Make fixtures

```
python manage.py dumpdata users -o fixtures/users.json
```

2. Load locally

```angular2html
 new.json
```

3. Loaddata

Zero - new?
First - delete useractivation from users and load users
Second - places
Third - courts
Fourth - games

Migrate old usergameaction.action to usergameaction.status

python manage.py dumpdata --exclude=auth --exclude=contenttypes --exclude=sessions --exclude=notifications --exclude=admin -o fixtures/all.json