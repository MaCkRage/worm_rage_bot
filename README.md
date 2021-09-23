# Worm Rage Bot

### This telegram bot is designed to download books for free.

- The bot is free. Please do not use it for commercial purposes
- If you want to expand the bot's functionality, or fix bugs, please fork the repository and unsubscribe about it by email ap9996696048@outlook.com
- Bot link: https://t.me/worm_rage_bot

### Installing:

1) Install Docker and docker-compose.

```bash
sudo apt update; apt upgrade -y; apt install -y curl; curl -sSL https://get.docker.com/ | sh; curl -L https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose
```
Don't forget press CTRL+D to exit from super user account.
2) Apply environment variables:
```bash
cp example.env .env
```
3) Change a random string for SECRET_KEY and POSTGRES_PASSWORD in .env
4) Change TELEGRAM_ACCESS_TOKEN in .env (how to get a token read here)
```bash
https://www.toptal.com/python/telegram-bot-tutorial-python
```
5) Install dependencies:
```bash
pipenv install
pipenv shell
```
6) Up docker-compose, migrate database and create super user:
```
docker-compose up -d
python3 backend/manage.py makemigrations
python3 backend/manage.py migrate
python3 backend/manage.py createsuperuser
```
7) Run bot
```bash
python3 backend/manage.py bot_run
```

8) If you need admin panel:
```bash
python3 backend/manage.py runserver
```
9) Enjoy!