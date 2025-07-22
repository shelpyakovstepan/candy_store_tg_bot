FROM python:3.12

RUN mkdir /candy_store_tg_bot

WORKDIR /candy_store_tg_bot

RUN pip install poetry

COPY pyproject.toml poetry.lock* README.md ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-root

COPY . .

RUN apt-get update && apt-get install -y dos2unix && \
    dos2unix /candy_store_tg_bot/docker/*.sh && \
    chmod a+x /candy_store_tg_bot/docker/*.sh

CMD ["poetry", "run", "/bin/bash", "-c", "python bot/main.py"]
