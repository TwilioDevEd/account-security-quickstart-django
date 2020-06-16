FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . .

RUN python3 manage.py migrate

EXPOSE 8000

CMD ["sh", "-c", "python3 manage.py runserver 0.0.0.0:8000"]
