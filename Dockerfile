FROM python:slim

SHELL [ "bash", "-c" ]

WORKDIR /app

# venv
COPY requirements.txt run ./
RUN ./run createVenvNoCache \
  && rm requirements.txt

# App
COPY ./app .

ENV APP_ROOT=/app

CMD [ "./run" ]
