FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app

RUN pip install pipenv
RUN pipenv install --deploy --system

ADD . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]