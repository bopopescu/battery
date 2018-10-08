version1 2018/10/08
before using the system, you should check the things below:
1. ./battery/settings.py   LOGGING level,DEBUG=FALSE,ALLOWED_HOSTS=['*'],DATABASES
2. ./mysocket/db_config.json user,passwd
3. delete battery.log socket.log
4. createsuperuser, makemigrations, migrate

