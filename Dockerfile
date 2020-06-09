FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt ./

COPY manage.py ./

COPY Makefile ./

RUN make install

COPY . .

RUN make serve-setup

EXPOSE 8000

CMD ["make", "serve"]
