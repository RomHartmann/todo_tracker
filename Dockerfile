FROM python:3.6

RUN apt-get update \
    && apt-get install -y python-pip

RUN pip install pipenv && mkdir /app

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock

WORKDIR /app
RUN pipenv install --system --deploy --ignore-pipfile
COPY . /app

RUN python manage.py migrate

EXPOSE 8001
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
