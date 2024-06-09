### how to run backend

1. install python
2. clone repo and install dependencies
```shell
git clone https://gitlab.com/gmanka/galaxy_backend
cd galaxy_backend
python -m venv .venv
.venb/bin/pip install -U pip
.venv/bin/pip install -U tortoise-orm aiogram fastapi rich
```
3. install autotests dependences
```shell
.venv/bin/pip install ruff pyright
```
4. now you can run code

- run autotests
```shell
tests=true .venv/bin/python galaxy_backend
```
- run api only, no telegram bot
```shell
.venv/bin/python galaxy_backend
```
- run api with telegram bot
```shell
tg_token='7409714466:AAFwNn9FnkA50Vh4vMBavGzB7XRac9YpKMQ' .venv/bin/python galaxy_backend
```
- run api with custom uvicorn setting
```shell
.venv/bin/uvicorn galaxy_backend:app
```

